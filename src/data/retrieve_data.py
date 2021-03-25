# -*- coding: utf-8 -*-

""""Functions to retrieve data from APIs or cloud storage"""

from pathlib import Path
import os
import json
import ee
from geetools import cloud_mask
import requests
from datetime import datetime as dt, timedelta
import re
import numpy as np


def mask_clouds(ee_img):
    mask_all = cloud_mask.sentinel2()
    masked_ee_img = mask_all(ee_img)
    return masked_ee_img

def aggregate_ndvi(date_list, ndvi_coll):
    def simple_aggregate(end_date):
        end_date = ee.Date(end_date)
        begin_date = ee.Date(end_date).advance(-1, "month")
        filt_coll = ndvi_coll.filterDate(begin_date, end_date)
        return filt_coll.mean().set({"system:time_start": begin_date.millis(), "system:time_end": end_date.millis()})

    merged_ndvi_list = date_list.map(simple_aggregate)
    return merged_ndvi_list

def get_gee_data(aoi, date_range=["2020-05-01", "2020-07-01"], mode="sentinel_raw",
                 band_names=["B2", "B3", "B4", "B8"]):
    """ download images from google earth engine as zip file

    Parameters
    ----------
    aoi : area of interest as list of [xcoord,ycoord] points
    date_range : list of [start date, end_date] in 'YYYY-MM-DD' format
    mode : 'sentinel_raw' for satellite images, 'global_land_cover' for copernicus glc maps, 'ndvi' for vegetation time series
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

    # download ndvi time series
    if mode == "ndvi":
        end_date = dt.now()
        start_date = end_date - timedelta(days=365)
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        print(start_date_str, end_date_str)

        # get ndvi collection
        sent2 = ee.ImageCollection(ee.ImageCollection("COPERNICUS/S2_SR"))
        sent_coll = sent2.filterBounds(aoi_obj).filterDate(start_date, end_date)
        sent_coll = sent_coll.filterMetadata("CLOUDY_PIXEL_PERCENTAGE", "less_than", 30)
        cloud_free_coll = sent_coll.map(mask_clouds)
        ndvi_coll = cloud_free_coll.map(
                            lambda img: img.normalizedDifference(["B8", "B4"])\
                                   .clip(aoi_obj)\
                                   .set("system:time_start", img.get("system:time_start"))
                                   )
        # get list of dates 12 month
        start_date = ee.Date(ee.List(ndvi_coll.get("date_range")).get(0))
        end_date = ee.Date(ee.List(ndvi_coll.get("date_range")).get(1))
        diff = end_date.difference(start_date, "month").round()
        date_seq = ee.List.sequence(1, diff, 1).map(lambda delay: start_date.advance(delay, "month") )
        print(date_seq.getInfo())
        # aggregate monthly ndvi

        monthly_ndvi_list = aggregate_ndvi(date_seq, ndvi_coll)

        fin_img = ee.ImageCollection.fromImages(monthly_ndvi_list).toBands()
        print(fin_img.getInfo())

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
        print(f"COMPLETED! image downloaded as zip file in \n {out_file}\n")
    return None


def download_dataset(aoi_path, data_parent_path=None, get_sent2=True, get_glc=True, get_ndvi=True):
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

        # if needed for area identification add this "_".join([str(abs(round(a[0]*10e2))) + str(abs(round(a[1]*10e2))) for a in c])
        area_name = timestamp + "_" + str(n)
        if get_sent2:
            link = get_gee_data(aoi=c, mode="sentinel_raw")
            download_data_from_link(link, area_name, mode="sentinel_raw", data_parent_path=data_parent_path)
        if get_glc:
            link2 = get_gee_data(aoi=c, mode="global_land_cover")
            download_data_from_link(link2, area_name,mode="global_land_cover", data_parent_path=data_parent_path)
        if get_ndvi:
            link3 = get_gee_data(aoi=c, mode="ndvi")
            download_data_from_link(link3, area_name, mode="ndvi", data_parent_path=data_parent_path)
    return timestamp


if __name__ == '__main__':
    aoi_path = Path("..", "..", "data", "raw", "test_aoi_global.geojson")
    download_dataset(aoi_path)
