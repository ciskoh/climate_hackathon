""" modules to download data and preprocess it"""

# download data
from .retrieve_data import download_dataset
# preprocess data
from .make_dataset import make_dataset

def create_and_preprocess_dataset(aoi_path):
    dataset_name = download_dataset(aoi_path)
    make_dataset(dataset_name)
    print(f"dataset {dataset_name} downloaded and preprocessed")

