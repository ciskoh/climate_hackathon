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

def mask_clouds(ee_img):
    mask_all = cloud_mask.sentinel2()
    masked_ee_img = mask_all(ee_img)
    return masked_ee_img

def get_gee_data(aoi, date_range=["2020-05-01", "2020-07-01"], mode="sentinel_raw", band_names=["B2", "B3", "B4", "B8"]):
    """download images from google earth engine as zip file
    aoi : area of interest as json file
    date_range : list of [start date, end_date] in 'YYYY-MM-DD' format
    mode : 'sentinel_raw' for satellite images, 'global_land_cover' for copernicus glc maps
    band_names : only for mode == sentinel_raw. List of band to keep from the original image defaults to ["B2", "B3", "B4", "B8"]
    Returns None. saves zip file with image in data/raw folder """
    # Initialize the Earth Engine module.
    try:
        ee.Initialize()
    except ee.ee_exception.EEException:
        print("MISSING credentials!!!! \n you have to authenticate to Google earth engine with the following account:")
        print("email account: landpro5196@gmail.com")
        print("pw: LandPro2021")
        ee.Authenticate()

    # Area of interest as gee object
    coords_list = coords['features'][0]["geometry"]["coordinates"][0][0]
    aoi_obj = ee.Geometry.Polygon(coords_list)

    print(f"Downloading {mode} image for coordinates {coords_list}")
    # date_range as gee object
    start_date = ee.Date(date_range[0])
    end_date = ee.Date(date_range[1])
    if mode == "sentinel_raw":
        # get sentinel collection
        sent2 = ee.ImageCollection(ee.ImageCollection("COPERNICUS/S2_SR"))
        sent_coll = sent2.filterBounds(aoi_obj).filterDate(start_date,end_date)
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
    response = requests.get(link)
    if not response.status_code == 200:
        print(f"problem retrieving file from the link:\n {link})!")
        return None
    # set output filename
    timestamp = re.sub("[^0-9]", "", dt.now().isoformat())
    out_file = Path("..", "..", "data", "raw", mode + timestamp + ".zip")
    with open(out_file, "wb") as f:
        f.write(response.content)
    del response
    if os.path.exists(out_file):
        print(f"COMPLETED! image downloaded as zip file in \n {out_file}")

if __name__ == '__main__':
    data_path = Path("..", "..", "data", "raw", "test_aoi_valencia.geojson")
    with open(data_path) as f:
        coords = json.load(f)
    print("testing sentinel_raw....")
    get_gee_data(aoi=coords)
    print("testing global land cover...")
    get_gee_data(aoi=coords, mode="global_land_cover")