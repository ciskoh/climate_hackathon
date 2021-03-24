# -*- coding: utf-8 -*-

import os
import numpy as np
import tensorflow as tf
from tqdm import tqdm
import cv2


from data_preprocessing_multiclass import load_data, tf_dataset, read_image
from metrics import dice_coef, generalized_dice_coef, dice_coef_c1, dice_coef_c2, dice_coef_c3, generalized_dice_loss, dice_loss, weighted_categorical_crossentropy

H = 256
W = 256
num_classes = 3

if __name__ == "__main__":
    """ Seeding """
    np.random.seed(42)
    tf.random.set_seed(42)


""" Paths """
dir = os.getcwd()
parent_dir = os.path.dirname(dir)

PATH = parent_dir + '/data/Sentinel'                             
PATH_IMAGES = PATH + '/images/'
PATH_MASKS = PATH + '/masks/'
PATH_PREDICTIONS = PATH + '/predictions' 

import sys
sys.path.append(parent_dir)

""" Data """
(train_x, train_y), (valid_x, valid_y), (test_x, test_y) = load_data(path_images = PATH_IMAGES, path_masks = PATH_MASKS,split = 0.1)
print(f"Dataset: Train: {len(train_x)} - Valid: {len(valid_x)} - Test: {len(test_x)}")

""" Model """
#load pretrained mobile_net or unet to predict on test data
#load mobilenet: mobile_net_multiclass.h5
#load unet: unet_large_multiclass.h5

### This are not provided but they can be in this structure 
### One very important issue is that the any custom metrics used during training  has to be reloaded as shown below.


model = tf.keras.models.load_model(parent_dir + '/models/mobilenet_multiclass.h5',
                                            custom_objects={"dice_loss": dice_loss,
                                                            "dice_coef": dice_coef,
                                                            "generalized_dice_coef" : generalized_dice_coef,
                                                            "dice_coef_c1":dice_coef_c1,
                                                            "dice_coef_c2":dice_coef_c2,
                                                            "dice_coef_c3":dice_coef_c3,
                                                            },compile=True)
                                            


""" Saving the masks """

PLOTTING_WIDTH= 529
PLOTTING_HEIGHT= 1078
SAVE_PATH = os.path.join(PATH, 'predictions/') 

for file_path in tqdm(test_x):
    
    file_name = os.path.basename(file_path)
    file_name, fileext = os.path.splitext(file_name)
  
    img = read_image(file_path)                           
    img = model.predict(np.expand_dims(img, axis=0))[0]                           
    img = np.argmax(img, axis=-1)                                                 
    img = np.expand_dims(img, axis=-1)
    img = img * (255/num_classes)                                                 
    img = np.concatenate([img, img, img], axis=2)                                 
    img = img.astype(np.uint8)
    img = cv2.resize(img, (PLOTTING_WIDTH,PLOTTING_HEIGHT), interpolation = cv2.INTER_NEAREST)                                      

result_filepath = os.path.join(SAVE_PATH,"%s_prediction%s" % (file_name, fileext)) 
                    
cv2.imwrite(result_filepath, img)
    file_name = os.path.basename(file_path)
    file_name, fileext = os.path.splitext(file_name)
  
    img = read_image(file_path)                           
    img = model.predict(np.expand_dims(img, axis=0))[0]                           
    img = np.argmax(img, axis=-1)                                                 
    img = np.expand_dims(img, axis=-1)
    img = img * (255/num_classes)                                                 
    img = np.concatenate([img, img, img], axis=2)                                 
    img = img.astype(np.uint8)
    img = cv2.resize(img, (PLOTTING_WIDTH,PLOTTING_HEIGHT), interpolation = cv2.INTER_NEAREST)                                      

result_filepath = os.path.join(SAVE_PATH,"%s_prediction%s" % (file_name, fileext)) 
                    
cv2.imwrite(result_filepath, img)