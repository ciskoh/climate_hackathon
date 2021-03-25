# -*- coding: utf-8 -*-

""""Functions to retrieve data from APIs or cloud storage"""

from pathlib import Path
import os
import json
import ee
from geetools import cloud_mask
import requests
from datetime import datetime as dt
import re
import numpy as np


def mask_clouds(ee_img):
    mask_all = cloud_mask.sentinel2()
    masked_ee_img = mask_all(ee_img)
    return masked_ee_img


def get_gee_data(aoi, date_range=["2020-05-01", "2020-07-01"], mode="sentinel_raw",
                 band_names=["B2", "B3", "B4", "B8"]):
    """ download images from google earth engine as zip file

    Parameters
    ----------
    aoi : area of interest as list of [xcoord,ycoord] points
    date_range : list of [start date, end_date] in 'YYYY-MM-DD' format
    mode : 'sentinel_raw' for satellite images, 'global_land_cover' for copernicus glc maps
    band_names : only for mode == sentinel_raw. List of band to keep from the original image defaults to ["B2", "B3", "B4", "B8"]

    Returns None. saves zip file with image in data/raw folder
    """
    # Initialize the Earth Engine module.
    try:
        ee.Initialize()
    except ee.ee_exception.EEException:
        print("MISSING credentials!!!! \n you have to authenticate to Google earth engine with the following account:")
        print("email account: landpro5196@gmail.com")
        print("pw: LandPro2021")
        ee.Authenticate()

    # Area of interest as gee object
    aoi_obj = ee.Geometry.Polygon([aoi])

    print(f"Downloading {mode} image for coordinates {aoi}")
    # date_range as gee object
    start_date = ee.Date(date_range[0])
    end_date = ee.Date(date_range[1])
    if mode == "sentinel_raw":
        # get sentinel collection
        sent2 = ee.ImageCollection(ee.ImageCollection("COPERNICUS/S2_SR"))
        sent_coll = sent2.filterBounds(aoi_obj).filterDate(start_date, end_date)
        # apply cloud removal
        # map function over collection
        cloud_free_coll = sent_coll.map(mask_clouds)
        # merge image using mean
        fin_img = cloud_free_coll.mean().select(band_names)

    # download global land cover
    if mode == "global_land_cover":
        glc = ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V-C3/Global")
        fin_img = ee.Image(glc.toList(10).reverse().get(0)).clip(aoi_obj)

        # download image
    link = fin_img.getDownloadURL({
        'scale': 10,
        'crs': 'EPSG:4326',
        'fileFormat': 'GeoTIFF',
        'region': aoi_obj})
    return link


def download_data_from_link(link, area_name, mode, data_parent_path=None):
    if not data_parent_path:
        data_parent_path = Path("..", "..", "data", "raw")

    response = requests.get(link)
    if not response.status_code == 200:
        print(f"problem retrieving file from the link:\n {link})!")
        return None
    # set output filename

    out_file = data_parent_path / str(area_name + "_" + mode + ".zip")
    with open(out_file, "wb") as f:
        f.write(response.content)
    del response
    if os.path.exists(out_file):
        print(f"COMPLETED! image downloaded as zip file in \n {out_file}")
    return None


def download_dataset(aoi_path, data_parent_path=None, get_glc=True):
    """ Retrieves input and target data from gee
    to train ml model"""
    with open(aoi_path) as f:
        coords = json.load(f)
    coords_list = coords['features']
    print(f" found {len(coords_list)} area of interest")
    # cycle through areas to download all of them
    timestamp = re.sub("[^0-9]", "", dt.now().isoformat())
    for n, c_dict in enumerate(coords_list):
        c = c_dict["geometry"]["coordinates"][0]
        print(f" \n downloading data for area {n}")

        # if neede for area identification add this "_".join([str(abs(round(a[0]*10e2))) + str(abs(round(a[1]*10e2))) for a in c])
        area_name = timestamp + "_" + str(n)

        link = get_gee_data(aoi=c, mode="sentinel_raw")
        download_data_from_link(link, area_name, mode="sentinel_raw", data_parent_path=data_parent_path)
        if get_glc:
            link2 = get_gee_data(aoi=c, mode="global_land_cover")
            download_data_from_link(link2, area_name,mode="global_land_cover", data_parent_path=data_parent_path)

    return timestamp


if __name__ == '__main__':
    aoi_path = Path("..", "..", "data", "raw", "test_aoi_global.geojson")
    download_dataset(aoi_path)
