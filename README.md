climate_hackathon
==============================

our entry for the cool farm alliance challenge


## environment
create environment with conda :

`conda create --name myenv --file environment.yml`
`conda activate myenv`

## django backend setup
Create postgres database
`make create_postgress`

Run Backend
`make init`
# Introduction


# Main blocks

1. Retrieve satellite images

Multispectral images are retrieved using Google earth engine thorugh a python script. The following functions allow to download relevant data given a geojson with coordinates of the area of interest:
- Downloading data
    data.download_dataset(aoi)
- Preprocess images
    data.make_dataset(dataset name)
 
2. Detect land cover and segment

    models.predict_model()

3. Calculate co2 metrics
    
4. User interaction (frontend & backend)



## download sentinel images

*download images from google earth engine as zip file
    aoi : area of interest as json file
    date_range : list of [start date, end_date] in 'YYYY-MM-DD' format
    mode : sentinel_raw is the only implemented for now
    band_names : list of band to keep from the original image defaults to ["B2", "B3", "B4", "B8"]
    Returns None. saves zip file with image in data/raw folder 
    import data*

    image = data.get_gee_data()


Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
