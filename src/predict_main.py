 ### complete function that downloads fdata, preprocess them and runs models.predict_model.py


def predict_main(aoi):
    """this functions trakes as input the json file fr4om frontend and returns the subpolygones with co2 metrcis
    aoi: json file with area of intreste from frontend
    """
    # download images from gee
    from data import retrieve_data
    dataset_name = retrieve_data(aoi)

    # preprocess data (creates dataset folder structure in data/preprocessed
    from data import make_dataset
    make_dataset(dataset_name)

    # predict land cover
    from models import predict_model
    prediction = predict_model(dataset_name)
    # prediction is a json with subpolygones

    # get co2 estimations
    from models import calc_vegetation_co_metric, calc_soil_co_metric
    prediction = calc vegetation_co_metric(prediction) # adds attribute "veg_co2_metric" to predictions
    prediction = calc_soil_co_metric(prediction) # adds attribute "veg_co2_metric" to predictions
    return prediction

    pass