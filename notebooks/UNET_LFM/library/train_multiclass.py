#!/usr/bin/env python
# coding: utf-8

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping

from data_augmentation import load_augmented_x_train_y_train
from metrics import dice_coef, generalized_dice_coef, dice_coef_c1, dice_coef_c2, dice_coef_c3, dice_loss
from src.features.data_preprocessing_multiclass import load_data, tf_dataset
from models import mobile_netv2

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


""" Loading original images and masks """
(train_x, train_y), (valid_x, valid_y), (test_x, test_y) = load_data(path_images = PATH_IMAGES, path_masks = PATH_MASKS,split = 0.1)
print(f"Dataset: Train: {len(train_x)} - Valid: {len(valid_x)} - Test: {len(test_x)}")

    
""" Loading augmented images and masks. """       
train_x, train_y = load_augmented_x_train_y_train(PATH)
print(f"Augmented Images: {len(train_x)} - Augmented Masks: {len(train_y)}")


""" Hyperparameters """
shape = (256, 256, 3)
num_classes = 3
batch_size = 4
epochs = 50
    
""" Model """
METRICS= [dice_coef, dice_coef_c1, dice_coef_c2, dice_coef_c3, generalized_dice_coef]    
        
      
model = mobile_netv2(shape, num_classes)
model.compile(loss=dice_loss, optimizer=tf.keras.optimizers.Adam(1e-4), metrics=METRICS) 

train_dataset = tf_dataset(train_x, train_y, batch=batch_size)
valid_dataset = tf_dataset(valid_x, valid_y, batch=batch_size)

train_steps = len(train_x)//batch_size
valid_steps = len(valid_x)//batch_size

callbacks = [
        ModelCheckpoint(parent_dir + '/models/multiclass.h5',  verbose=1, save_best_only=True),
        ReduceLROnPlateau(monitor="val_loss", patience=3, factor=0.1, verbose=1, min_lr=1e-6),
        EarlyStopping(monitor="val_loss", patience=10, verbose=1)
    ]

model.fit(train_dataset,
        steps_per_epoch=train_steps,
        validation_data=valid_dataset,
        validation_steps=valid_steps,
        epochs=epochs,
        callbacks=callbacks
    )
