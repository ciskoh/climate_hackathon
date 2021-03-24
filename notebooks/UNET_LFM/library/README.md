## Library
Welcome to the library of this project. This folder includes all the needed scripts to execute the models:

## Models
[models.py](#): This script includes all the models. Binary and multiclasss

## Metrics
[metrics.py](#): This script includes all the metrics used for this project.

## Data Augmentation
[data_augmentation.py](#): Run this script to create new augmented data to increase the amount and diversity of data to train the models and saves the new images in predefined folders.
The script performs the following augmentations:
- RandomRotate90
- Rotate
- GridDistortion
- ShiftScaleRotate
- RandomBrightnessContrast
- Crop

If other augmentation techniques are desired, the script can be changed accordingly. Check [Demo](https://albumentations-demo.herokuapp.com) to test the diffrent augmentation approaches.


## Multiclass Model
#### Preprocess
Per default, the script uses the following

- Train/Val/Test-Split = 80% / 10% / 10%
- Height = 256
- Width = 256
- BATCH = 4

#### Train

#### Predict

#### Visualise






