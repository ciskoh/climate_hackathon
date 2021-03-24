# -*- coding: utf-8 -*-

from pathlib import Path
import os
import zipfile
import gdal
import numpy as np
import matplotlib.pyplot as plt


def create_geoTiff(dst_filepath, fin_array, data0):
    x_pixels = fin_array.shape[1]  # number of pixels in x
    y_pixels = fin_array.shape[0]  # number of pixels in y
    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create(dst_filepath, x_pixels, y_pixels, 1, gdal.GDT_Float32)
    dataset.GetRasterBand(1).WriteArray(fin_array)

    # follow code is adding GeoTranform and Projection
    geotrans = data0.GetGeoTransform()  # get GeoTranform from existed 'data0'
    proj = data0.GetProjection()  # you can get from a exsited tif or import
    dataset.SetGeoTransform(geotrans)
    dataset.SetProjection(proj)
    dataset.FlushCache()
    dataset = None
    if os.path.exists(dst_filepath):
        print(f" saved geotiff at \n {dst_filepath}")
    return None


def refine_glc(input_file_name=None, refine=60):

    print("preparing global land cover map")
    # find latest file
    if input_file_name == None:
        raw_data_path = Path("..", "..", "data", "raw")
        file_list = [f for f in os.listdir( raw_data_path ) if "global_land_cover" in f and f.endswith(".zip")]
        input_file_name = sorted(file_list, reverse=True)[0]

    # unzip file in raw folder
    input_filepath = raw_data_path / input_file_name
    unzip_folder = raw_data_path / input_file_name.split(".")[-2]
    if not os.path.isdir(unzip_folder):
        os.mkdir(unzip_folder)
        print(input_filepath, unzip_folder)

    with zipfile.ZipFile(input_filepath, 'r') as zip_ref:
        zip_ref.extractall(unzip_folder)

    # mask relevant bands with predict_proba band
    if refine > 0:
        print("refining classification information for ")
        for r,_,fi in os.walk(unzip_folder):
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

        classi_array[proba_array < refine] = -99
        print(np.sum(proba_array<refine) )
        refined_array = np.where(proba_array > refine, classi_array, -99)
        fig, ax = plt.subplots()
        ax.imshow(refined_array)
        print(np.unique(refined_array))

        # save refined array as geotiff
        dst_filepath= Path ("..", "..", "data", "processed" ) / str(input_file_name.split(".")[-2]+".tiff")
        create_geoTiff(str(dst_filepath), refined_array, classi_geofile)



def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """


if __name__ == '__main__':


    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables

    refine_glc()

