 """ complete function that downloads fdata, preprocess them and runs models.predict_model.py"""

import sys
sys.path.append("..")
import data
import os
from models import predict_model
from models import calc_vegetation_co_metric, calc_soil_co_metric


 def predict_main(aoi_path):
    """this functions trakes as input the json file fr4om frontend and returns the subpolygones with co2 metrcis
    aoi: json file with area of intreste from frontend
    """
    # download images from gee
    data_parent_path = os.path.join("..", "data", "raw")
    dataset_name = data.download_dataset(aoi_path, data_parent_path= data_parent_path, get_sent2=True, get_glc=False, get_ndvi=False)

    # preprocess data (creates dataset folder structure in data/preprocessed
    # from data import make_dataset
    data.make_dataset(dataset_name)

    # predict land cover

    prediction = predict_model(dataset_name)
    # prediction is a json with subpolygones

    # get co2 estimations
    prediction = calc_vegetation_co_metric(prediction) # adds attribute "veg_co2_metric" to predictions
    prediction = calc_soil_co_metric(prediction) # adds attribute "soil_co2_metric" to predictions
    #return prediction

    pass

if __name__ == '__main__':
    import os
    aoi="/home/matt/Dropbox/github/climate_hackathon/data/raw/test_aoi_global.geojson"
    print(os.getcwd())
    predict_main(aoi)