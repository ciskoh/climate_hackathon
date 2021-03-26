# -*- coding: utf-8 -*-

from pathlib import Path
import os
import zipfile
import gdal
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from shutil import rmtree


def create_geoTiff(dst_filepath, fin_array, data0, band_num=1):
    x_pixels = fin_array.shape[1]  # number of pixels in x
    y_pixels = fin_array.shape[0]  # number of pixels in y
    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create(dst_filepath, x_pixels, y_pixels, band_num, gdal.GDT_Float32)
    # create 3d array to avoid errors
    if len(fin_array.shape) < 3:
        fin_array = np.atleast_3d(fin_array)

    for i in range(band_num):
        print(f"adding band {i + 1}")
        image = fin_array[:, :, i]
        dataset.GetRasterBand(i + 1).WriteArray(image)

    # adding GeoTranform and Projection
    geotrans = data0.GetGeoTransform()  # get GeoTranform from existed 'data0'
    proj = data0.GetProjection()  # you can get from a exsited tif or import

    dataset.SetGeoTransform(geotrans)
    dataset.SetProjection(proj)

    dataset.FlushCache()
    dataset = None
    if os.path.exists(dst_filepath):
        print(f" saved geotiff at \n {dst_filepath}")
    return None

# discarded

def crop_centre(img,cropx,cropy):
    if len(img.shape)>2:
        y,x = img.shape[:2]
        startx = x//2-(cropx//2)
        starty = y//2-(cropy//2)
        fin_img = img[starty:starty+cropy,startx:startx+cropx, ::]
    else:
        y, x = img.shape
        startx = x // 2 - (cropx // 2)
        starty = y // 2 - (cropy // 2)
        fin_img = img[starty:starty + cropy, startx:startx + cropx]
    return fin_img

from gdal import Translate
from gdal import TranslateOptions

def resize_with_gdal(geo_dataset_path, resize_dim):
    dest_path = geo_dataset_path.parent / geo_dataset_path.name[:-1]
    geo_obj = gdal.Open(str(geo_dataset_path))
    t_o = {"width": resize_dim[0], "height": resize_dim[1]}
    ds = Translate(str(dest_path), geo_obj, **t_o)
    ds = None

def preprocess_sentinel_images(raw_file_path, dest_path):
    input_filename = str(raw_file_path.name).replace("_sentinel_raw.zip", "")
    unzip_folder = dest_path / "images" / input_filename
    if not os.path.isdir(unzip_folder):
        os.mkdir(unzip_folder)
    print(input_filename, unzip_folder)
    with zipfile.ZipFile(raw_file_path, 'r') as zip_ref:
        zip_ref.extractall(unzip_folder)
    band_list = []
    for band in sorted(os.listdir(unzip_folder)):
        band_dataset = gdal.Open(str(unzip_folder / band))
        band_arr = band_dataset.ReadAsArray()
        # band_arr = crop_centre(band_arr, resize_dim[0], resize_dim[1])
        band_list.append(band_arr)
    band_tuple = tuple(band_list)
    fin_array = np.dstack(band_tuple)

    dst_filepath = str(dest_path / "images" / input_filename) + ".tiff"
    data0 = band_dataset
    create_geoTiff(dst_filepath, fin_array, data0, len(band_list))
    for f in os.listdir(dest_path / "images"):
        if os.path.isdir(dest_path / "images" / f):
            rmtree(dest_path / "images" / f)


def preprocess_glc(raw_file_path, dest_path, scalar_pixels=True, refine=0):
    """opens GLC map and masks uncertain pixels saving them in ../data/processed"""
    print("preparing global land cover map")
    input_filename = str(raw_file_path.name).replace("_global_land_cover.zip", "")
    unzip_folder = dest_path / input_filename
    # unzip file in raw folder

    if not os.path.isdir(unzip_folder):
        os.mkdir(unzip_folder)
        print(raw_file_path, unzip_folder)

    with zipfile.ZipFile(raw_file_path, 'r') as zip_ref:
        zip_ref.extractall(unzip_folder)

    # mask relevant bands with predict_proba band

    for r, _, fi in os.walk(unzip_folder):
        for f in fi:
            if "proba" in f:
                pred_proba_path = Path(r) / f
                print("found proba")
            elif "classification.tif" in f:
                classi_path = Path(r) / f
                print("found discrete_classification")
        # import arrays
        proba_array = gdal.Open(str(pred_proba_path)).ReadAsArray()
        classi_geofile = gdal.Open(str(classi_path))
        classi_array = classi_geofile.ReadAsArray()

        if refine > 0:
            print("refining classification information for glc")
            classi_array[proba_array < refine] = 0
            print(np.sum(proba_array < refine))
            classi_array = np.where(proba_array > refine, classi_array, -99)

        # save refined array as geotiff
        dst_file_path = str(dest_path / input_filename) + ".tiff"
        create_geoTiff(str(dst_file_path), classi_array, classi_geofile)
        for f in os.listdir(dest_path):
            if os.path.isdir(dest_path / f):
                rmtree(dest_path / f)


def make_dataset(dataset_name, parent_data_path=None, resize_dim = [256,256]):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    if parent_data_path == None:
        parent_data_path = Path("..", "..", "data", "raw")
    # get all data belonging to a dataset
    images_file_list = sorted(
        [f for f in os.listdir(parent_data_path) if dataset_name in f and f.endswith("sentinel_raw.zip")])
    masks_file_list = sorted(
        [f for f in os.listdir(parent_data_path) if dataset_name in f and f.endswith("global_land_cover.zip")])

    # prepare destination folder
    parent_dest_path = Path("..", "..", "data", "processed")
    dest_path = parent_dest_path / dataset_name
    if not os.path.isdir(dest_path):
        os.mkdir(dest_path)
        os.mkdir(dest_path / "images")
        os.mkdir(dest_path / "masks")
        os.mkdir(dest_path / "predictions")

    # preprocess  sentinel images
    for img in images_file_list:
        preprocess_sentinel_images(parent_data_path / img, dest_path)
    # preprocess glc images as masks
    for img in masks_file_list:
        print("dest path:", dest_path)
        preprocess_glc(parent_data_path / img, dest_path / "masks", refine=0)
    if resize_dim:
        for f in os.listdir(dest_path / "images"):
            path_to_image = dest_path / "images" / f
            resize_with_gdal(path_to_image, resize_dim)
            path_to_image.unlink()

        for f in os.listdir(dest_path / "masks"):
            path_to_image = dest_path / "masks" / f
            resize_with_gdal(path_to_image, resize_dim)
            path_to_image.unlink()

if __name__ == '__main__':
    dataset_name = "20210325175353219035"

    make_dataset(dataset_name)
    # not used in this stub but often useful for finding various files

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables

    # refine_glc()

    # path_to_img = Path("..", "..", "data", "processed", "20210324225635924767", "images", "20210324225635924767_0.tiff")
    # my_img_array = gdal.Open(str(path_to_img)).ReadAsArray()
    # my_img_array = np.swapaxes(my_img_array, 0, 2).copy()
    # new_array = crop_centre(my_img_array, 256, 256)
    # print(my_img_array.shape, new_array.shape)
    # fig, axs = plt.subplots(ncols=2, nrows=1)
    # axs[0].imshow(my_img_array)
    # axs[1].imshow(new_array)
    # fig.show()

    path_to_img = Path("/home/matt/Dropbox/github/climate_hackathon/data/processed/20210325175353219035/masks/20210325175353219035_0.tiff")
    dest_path = path_to_img.parent / path_to_img.name[:-1]

    geo_obj = gdal.Open(str(path_to_img))
    t_o = {"width": 256, "height": 256}
    ds = Translate(str(dest_path), geo_obj, **t_o)
    ds = None
