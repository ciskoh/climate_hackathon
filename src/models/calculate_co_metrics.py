
### Functions to add metrics of soil and vegeation co2

import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import rasterio
from rasterio import plot
from rasterio.plot import show
from rasterio.mask import mask
import os


# needed files
# soil_co2_estimate for europe

src = rasterio.open('soc_europe_250m.tif')

def calc_soil_co_metric(aoi):
    """calculates the soil co2 metric using soc_europe map and the given subpolygones
    aoi is a json file with multiple polygones
    returns updated aoi with co2 estimates for each polygone as attributes
    """
    masked, mask_transform = mask(dataset=src, shapes=gdf.geometry, crop=True)
    show(masked, transform=mask_transform)

    profile = src.meta
    WIDTH = masked.shape[2]  ## get the dimensions of the image we are writting out
    HEIGHT = masked.shape[1]
    profile.update(driver='GTiff', transform=mask_transform, height=HEIGHT, width=WIDTH)
    print(profile)  ## check on the updated profile

