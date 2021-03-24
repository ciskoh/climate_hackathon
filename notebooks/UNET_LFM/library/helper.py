#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np
import os
import cv2
from glob import glob
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from random import sample 
from PIL import Image
from datetime import datetime

# MobileNet imports
from tensorflow.keras.models import Model
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.metrics import Recall, Precision
from tensorflow.keras import backend as K

# U-NET imports
from keras.models import *
from keras.layers import *
from keras.optimizers import *
from keras.callbacks import ModelCheckpoint, LearningRateScheduler

from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import load_model
import time


################ Global parameters used in the App ##########################
IMAGE_SIZE = 256
H = 256
W = 256
BATCH = 4
num_classes = 3
epoch = 5

## Plotting parameters
PLOTTING_WIDTH = 529                                            
PLOTTING_HEIGHT = 1078
########################## Directories#########################
dir = os.getcwd()
parent_dir = os.path.dirname(dir)
 
Directory = parent_dir   
SAVE_FORMAT = 'h5'

##################### HELPER FUNCTIONS############################################################
def Get_prediction_path(path_model, base_file, epoch = None,
                    Animation = False ):
    path_predictions = path_model + "prediction/"
    file_b = base_file.strip(".png")
    if Animation:
        if epoch < 10:
            file_a = "00202_prediction_runMobile1_epoch_000" + str(epoch) +".png"
        elif epoch < 100:
            file_a = "00202_prediction_runMobile1_epoch_00" + str(epoch) +".png"            
        elif epoch < 1000:
            file_a = "00202_prediction_runMobile1_epoch_0" + str(epoch) +".png"
        elif epoch < 10000:
            file_a = "00202_prediction_runMobile1_epoch_" + str(epoch) +".png"
        path_pred = path_animation + file_a
    else:
        file_p = file_b + "_prediction" +".png"
        path_pred = path_predictions + file_p
    return path_pred

def predictions_plots_mc(base_file , PATH_Data , prediction_image_path ):
    # Plotting the results comparison against original data
    mask_fat_color ='firebrick'
    mask_muscle_color ='royalblue'                                                
    contour_fat_color ='white'
    contour_muscle_color ='white'

    # path to file that will be plotted
    file_name, fileext = os.path.splitext(base_file)
    original_path = os.path.join(PATH_Data, "images/", base_file)
    mask_image_path = os.path.join(PATH_Data, "masks/", base_file)
    prediction_image_path = prediction_image_path

    ############## read images as numpy arrays  ############
    original = read_image_PLOTTING(original_path, PLOTTING_WIDTH, PLOTTING_HEIGHT)
    mask_image = mask_to_255(mask_image_path)
    mask_image = create_overlay(mask_image, PLOTTING_WIDTH, PLOTTING_HEIGHT, 
                            color1=mask_fat_color, color2=mask_muscle_color)
   
    mask_area_image = create_overlay(mask_to_255(mask_image_path), PLOTTING_WIDTH, PLOTTING_HEIGHT, 
                            color1=mask_fat_color, color2=mask_muscle_color)

    mask_outline_image = create_overlay(convert_mask_to_outline(mask_image_path, contour_width=6), 
                                    PLOTTING_WIDTH, PLOTTING_HEIGHT, color1=contour_fat_color,
                                        color2=contour_muscle_color)   
    prediction_image = create_overlay(Image.open(prediction_image_path), PLOTTING_WIDTH, PLOTTING_HEIGHT, 
                                  color1=mask_fat_color, color2=mask_muscle_color)   

    
    merged_mask = cv2.addWeighted(mask_area_image, 1, original, 0.6, 0)                             
    # choose level of transparency for first and second picture
    merged_prediction = cv2.addWeighted(prediction_image, 1, original, 0.6, 0)
    merged_prediction_mask = cv2.addWeighted(mask_outline_image, 1, prediction_image, 1, 0)
    merged_image_both = cv2.addWeighted(merged_prediction_mask, 1, original, 0.6, 0)   

############################################### create legend ####################################################

    colors = [mask_fat_color, mask_muscle_color]
    texts = ["Fat tissue", "Muscle tissue"]
    patches = [ mpatches.Patch(color=colors[i], label="{:s}".format(texts[i]) ) for i in range(len(texts)) ]
############### PLOT############################################################################################
    fig, axs = plt.subplots(1, 4, figsize=(20, 8))
    axs[0].set_title("Original")
    axs[0].imshow(original)

    axs[1].set_title("Ground truth")
    axs[1].imshow(merged_mask)
    axs[1].legend(handles=patches, bbox_to_anchor=(0.0, 0.0), loc='lower left', ncol=1 )

    axs[2].set_title("Prediction")
    axs[2].imshow(merged_prediction)
    axs[2].legend(handles=patches, bbox_to_anchor=(0.0, 0.0), loc='lower left', ncol=1 )

    axs[3].set_title("Prediction compared to ground truth")
    axs[3].imshow(merged_image_both)
    axs[3].legend(handles=patches, bbox_to_anchor=(0.0, 0.0), loc='lower left', ncol=1 )

    ########### a closer look ##############
    fig2, axs2 = plt.subplots(1, 2, figsize=(25, 8))
    axs2[0].set_title("Ground truth, cropped")
    axs2[0].imshow(crop_image(merged_mask, (0, 0, PLOTTING_WIDTH, PLOTTING_HEIGHT/3)))          
    # define cropping area (leftuppercorner(x,y), bottomrightcorner(x,y))
    axs2[0].legend(handles=patches, bbox_to_anchor=(0.0, 1), loc='upper left', ncol=1 )

    axs2[1].set_title("Prediction, cropped")
    axs2[1].imshow(crop_image(merged_image_both, (0, 0, PLOTTING_WIDTH, PLOTTING_HEIGHT/3)))
    axs2[1].legend(handles=patches, bbox_to_anchor=(0.0, 1), loc='upper left', ncol=1 )
    return fig, fig2, axs, axs2


def predictions_plots_binary(base_file, PATH_Data , prediction_image_path):
    # https://matplotlib.org/3.1.0/gallery/color/named_colors.html
    # Plotting the results comparison against original data
    mask_fat_color ='red' 
    prediction_fat_color ='red'  
   
    # path to file that will be plotted
    file_name, fileext = os.path.splitext(base_file)
    original_path = os.path.join(PATH_Data, "images/", base_file)
    mask_image_path = os.path.join(PATH_Data, "masks/", base_file)
    prediction_image_path = prediction_image_path   
    ############## read images as numpy arrays  ############
    original = read_image_PLOTTING(original_path, PLOTTING_WIDTH, PLOTTING_HEIGHT)
    
# I think thi is in a helper function.........
    mask_area_image = create_overlay_b_p(convert_mask_to_area(mask_image_path), PLOTTING_WIDTH, PLOTTING_HEIGHT, 
                            color1=mask_fat_color)
    mask_outline_image = create_overlay_b_p(convert_mask_to_outline_b(mask_image_path, contour_width = 6), 
                                    PLOTTING_WIDTH, PLOTTING_HEIGHT, color1='white')
    prediction_image = create_overlay_b_p(Image.open(prediction_image_path), PLOTTING_WIDTH, PLOTTING_HEIGHT, 
                                   color1=prediction_fat_color)
##### create the overlay images  ###########
    merged_mask = cv2.addWeighted(mask_area_image, 1, original, 0.6, 0)                
# choose level of transparency for first and second picture
    merged_prediction = cv2.addWeighted(prediction_image, 1, original, 0.6, 0)
    merged_prediction_mask = cv2.addWeighted(mask_outline_image, 1, prediction_image, 0.6, 0)
    merged_image_both = cv2.addWeighted(merged_prediction_mask, 1, original, 0.6, 0)

############################################### create legend ####################################################

    colors = [mask_fat_color]
    texts = ["Fat tissue"]
    patches = [ mpatches.Patch(color=colors[i], label="{:s}".format(texts[i]) ) for i in range(len(texts)) ]
############### PLOT############################################################################################        
     
    fig, axs = plt.subplots(1, 4, figsize=(20, 8))
    axs[0].set_title("Original")
    axs[0].imshow(original)


    axs[1].set_title("Ground truth")
    axs[1].imshow(merged_mask)
    axs[1].legend(handles=patches, bbox_to_anchor=(0.0, 0.0), loc='lower left', ncol=1 )

    axs[2].set_title("Prediction")
    axs[2].imshow(merged_prediction)
    axs[2].legend(handles=patches, bbox_to_anchor=(0.0, 0.0), loc='lower left', ncol=1 )
    
    axs[3].set_title("Prediction compared to ground truth")
    axs[3].imshow(merged_image_both)
    axs[3].legend(handles=patches, bbox_to_anchor=(0.0, 0.0), loc='lower left', ncol=1 )

    ########### a closer look ##############
    fig2, axs2 = plt.subplots(1, 2, figsize=(25, 8))

    axs2[0].set_title("Ground truth, cropped")
    axs2[0].imshow(crop_image(merged_mask, (0, 0, PLOTTING_WIDTH, PLOTTING_HEIGHT/3)))          
    # define cropping area (leftuppercorner(x,y), bottomrightcorner(x,y))
    axs2[0].legend(handles=patches, bbox_to_anchor=(0.0, 1), loc='upper left', ncol=1 )

    axs2[1].set_title("Prediction, cropped")
    axs2[1].imshow(crop_image(merged_image_both, (0, 0, PLOTTING_WIDTH, PLOTTING_HEIGHT/3)))
    axs2[1].legend(handles=patches, bbox_to_anchor=(0.0, 1), loc='upper left', ncol=1 )
    
    return fig, fig2, axs, axs2


# Plotting
@st.cache
def read_image_PLOTTING(path, width, height):
  ''' reads an image and resizes but WITHOUT normalizing'''
  x = cv2.imread(path, cv2.IMREAD_COLOR)
  x = cv2.cvtColor(x, cv2.COLOR_BGR2BGRA)
  x = cv2.resize(x, (width, height))
  return x



@st.cache
def create_overlay(img, width=256, height=256, color1='red', color2='green'):
  '''createas a RGBA image in form of a numpy array. Loads binary, grayscale 
  or color image and transforms black values to color, and white values to trasparent'''

  img= np.array(img.convert('RGBA')).astype(np.uint8) 
  mask_fat = (img[:,:,2] == 2*255/num_classes)  
  mask_muscle = (img[:,:,2] == 1*255/num_classes)
  img[:,:,3] = 0
  img[:,:,3][np.where(mask_fat| mask_muscle) ] = 255

  R, G, B = np.multiply(mcolors.to_rgb(color1),255).astype(np.uint8)
  img[:,:,0][np.where(mask_fat)] =R
  img[:,:,1][np.where(mask_fat)] =G
  img[:,:,2][np.where(mask_fat)] =B

  R, G, B = np.multiply(mcolors.to_rgb(color2),255).astype(np.uint8)
  img[:,:,0][np.where(mask_muscle)] =R
  img[:,:,1][np.where(mask_muscle)] =G
  img[:,:,2][np.where(mask_muscle)] =B
  return img

def create_overlay_b(img, width=256, height=256, color1='red', color2='green'):
  '''createas a RGBA image in form of a numpy array. Loads binary, grayscale 
  or color image and transforms black values to color, and white values to trasparent'''
#  img = img.resize((width, height), resample = Image.NEAREST)
#    y_pred = cv2.resize(y_pred, (PLOTTING_WIDTH,PLOTTING_HEIGHT), interpolation = cv2.NEAREST) 
  img = cv2.resize(img, (width, height), interpolation = cv2.INTER_NEAREST) 
  img= np.array(img.convert('RGBA')).astype(np.uint8) 
  mask_fat = (img[:,:,2] == 4)  
  mask_muscle = (img[:,:,2] == 1)
  img[:,:,3] = 0
  img[:,:,3][np.where(mask_fat| mask_muscle) ] = 255

  R, G, B = np.multiply(mcolors.to_rgb(color1),255).astype(np.uint8)
  img[:,:,0][np.where(mask_fat)] =R
  img[:,:,1][np.where(mask_fat)] =G
  img[:,:,2][np.where(mask_fat)] =B

  R, G, B = np.multiply(mcolors.to_rgb(color2),255).astype(np.uint8)
  img[:,:,0][np.where(mask_muscle)] =R
  img[:,:,1][np.where(mask_muscle)] =G
  img[:,:,2][np.where(mask_muscle)] =B
  return img


def create_overlay_b_p(img, width=256, height=256, color1='red', color2='green'):
  '''createas a RGBA image in form of a numpy array. Loads binary, grayscale 
  or color image and transforms black values to color, and white values to trasparent'''
  img = img.resize((width, height), resample = Image.NEAREST)
#    y_pred = cv2.resize(y_pred, (PLOTTING_WIDTH,PLOTTING_HEIGHT), interpolation = cv2.NEAREST) 
#  img = cv2.resize(img, (width, height), interpolation = cv2.INTER_NEAREST) 
  img= np.array(img.convert('RGBA')).astype(np.uint8) 
  mask_fat = (img[:,:,2] == 4)  
  mask_muscle = (img[:,:,2] == 1)
  img[:,:,3] = 0
  img[:,:,3][np.where(mask_fat| mask_muscle) ] = 255

  R, G, B = np.multiply(mcolors.to_rgb(color1),255).astype(np.uint8)
  img[:,:,0][np.where(mask_fat)] =R
  img[:,:,1][np.where(mask_fat)] =G
  img[:,:,2][np.where(mask_fat)] =B

  R, G, B = np.multiply(mcolors.to_rgb(color2),255).astype(np.uint8)
  img[:,:,0][np.where(mask_muscle)] =R
  img[:,:,1][np.where(mask_muscle)] =G
  img[:,:,2][np.where(mask_muscle)] =B
  return img


@st.cache
def crop_image(image_array, box):
  ''' crops an image to size of box'''
  cropped_image = Image.fromarray(image_array)
  cropped_image = cropped_image.crop(box) 
  return cropped_image

@st.cache
def mask_to_255(path):
  '''converts pixel values from 0-1 to 0-255'''
  img = Image.open(path)
  img = np.array(img)
  img[np.where(img== 4)] = 2*255/num_classes
  img[np.where(img== 1)] = 1*255/num_classes
  img = Image.fromarray(img)
  return img

def convert_mask_to_area(path):
  img = Image.open(path)
  img = np.array(img)
  img[np.where(img== 255)] = 4
  img = Image.fromarray(img)                                            
  return img


def convert_mask_to_outline(path, contour_width=6):

    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    thresh1 = img.copy()
    thresh1[np.where(thresh1 == 4)] = 0
    contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_contours = np.zeros(img.shape)
    img_contours = cv2.drawContours(img_contours, contours, -1, (85,85,85), contour_width)

    thresh2 = img.copy()
    thresh2[np.where(thresh1 == 1)] = 0
    contours, hierarchy = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_contours2 = cv2.drawContours(img_contours, contours, -1, (170,170,170), contour_width)  
    
    img = Image.fromarray(img_contours2)                                            
    return img


def convert_mask_to_outline_b(path, contour_width=6):
  # img = Image.open(path)
  # img = img.filter(ImageFilter.FIND_EDGES)
  #img = np.array(img)
  img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
  ret, thresh = cv2.threshold(img, 127, 255, 0)
  contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  img_contours = np.zeros(img.shape)
  cv2.drawContours(img_contours, contours, -1, (4,4,4), contour_width)
  #img[np.where(img== 255)] = 4
  img = Image.fromarray(img_contours)                                            
  return img


@st.cache
def load_model(path_model, SAVE_FORMAT, custom_metrics):
    reloaded_model = tf.keras.models.load_model(path_model+ 'model.' + SAVE_FORMAT, custom_objects=custom_metrics, compile=True)
    return reloaded_model


@st.cache
def load_history(path_model, SAVE_FORMAT):
    # reload training history
    Full_history = np.load(path_model+'/Training_history.npy',allow_pickle='TRUE').item()
    return Full_history

   
# Plot full training history
def training_history_plot(Full_history, coeff_name):
    fig, axs = plt.subplots(1, 2, figsize = (15, 4))
    training_loss = Full_history['loss']
    validation_loss = Full_history['val_loss']
    training_accuracy = Full_history[coeff_name]
    validation_accuracy = Full_history[('val_'+ coeff_name)]
    epoch_count = range(1, len(training_loss) + 1)
    axs[0].plot(epoch_count, training_loss, 'r--')
    axs[0].plot(epoch_count, validation_loss, 'b-')
    axs[0].legend(['Training Loss', 'Validation Loss'])
    axs[1].plot(epoch_count, training_accuracy, 'r--')
    axs[1].plot(epoch_count, validation_accuracy, 'b-')
    axs[1].legend(['Dice Coef training', 'Dice Coef validation'])
    return fig, axs

def predict_plot_multiclass(uploaded_file, W, H, PLOTTING_WIDTH,PLOTTING_HEIGHT, num_classes, model):        
    # Convert the file to an open cv image        
    file_bytes = np.asarray(bytearray(uploaded_file.read()))
    opencv_image = cv2.imdecode(file_bytes, 1)
    x = cv2.resize(opencv_image, (W, H))
    x = x / 255.0
    x = x.astype(np.float32)  
    y_pred = model.predict(np.expand_dims(x, axis=0))[0]
    y_pred = np.argmax(y_pred, axis=-1)
    y_pred = np.expand_dims(y_pred, axis=-1)
    y_pred = y_pred* (255/num_classes)
    y_pred = np.concatenate([y_pred, y_pred, y_pred], axis=2) 
    y_pred = y_pred.astype(np.uint8)
    y_pred = cv2.resize(y_pred, (PLOTTING_WIDTH,PLOTTING_HEIGHT), interpolation = cv2.INTER_NEAREST) 
    mask_fat_color ='red' 
    mask_muscle_color ='blue' # choose a predefined matplotlib color https://matplotlib.org/3.1.0/gallery/color/named_colors.html
    prediction_fat_color ='red'  
    prediction_muscle_color ='blue' 
    color1='red'
    color2='blue'       
    img = Image.fromarray(y_pred)
    img = np.array(img.convert('RGBA')).astype(np.uint8)

    mask_fat = (img[:,:,2] == 2*255/num_classes)
    mask_fat = (img[:,:,2] == 2*255/num_classes)  
    mask_muscle = (img[:,:,2] == 1*255/num_classes)
    img[:,:,3] = 0
    img[:,:,3][np.where(mask_fat| mask_muscle) ] = 255

    R, G, B = np.multiply(mcolors.to_rgb(color1),255).astype(np.uint8)
    img[:,:,0][np.where(mask_fat)] =R
    img[:,:,1][np.where(mask_fat)] =G
    img[:,:,2][np.where(mask_fat)] =B

    R, G, B = np.multiply(mcolors.to_rgb(color2),255).astype(np.uint8)
    img[:,:,0][np.where(mask_muscle)] =R
    img[:,:,1][np.where(mask_muscle)] =G
    img[:,:,2][np.where(mask_muscle)] =B               
    original = cv2.resize(opencv_image, (PLOTTING_WIDTH, PLOTTING_HEIGHT)) 
    original = cv2.cvtColor(original, cv2.COLOR_BGR2BGRA)
###########         ##### create the overlay images  ###########  
#     # choose level of transparency for first and second picture
    merged_prediction = cv2.addWeighted(original, 0.7, img, 0.3, 0)

############################################### create legend ####################################################

    colors = [mask_fat_color, mask_muscle_color]
    texts = ["Fat tissue", "Muscle tissue"]
    patches = [ mpatches.Patch(color=colors[i], label="{:s}".format(texts[i]) ) for i in range(len(texts)) ]
############### PLOT############################################################################################
#         ########  plot  #########

    fig_5, axs5 = plt.subplots(1,2, figsize=(20, 20))
    axs5[0].set_title("Original", fontsize=30)
    axs5[0].imshow(original)
    axs5[1].set_title("Prediction", fontsize=30)
    axs5[1].imshow(merged_prediction)
    axs5[1].legend(handles=patches, bbox_to_anchor=(0.0, 0.0), loc='lower left', ncol=1, fontsize=30)
    return fig_5, axs5



def predict_plot_binary(uploaded_file, W, H, PLOTTING_WIDTH,PLOTTING_HEIGHT, num_classes, model):              
    binary_threshold = 0.5
    
    file_bytes = np.asarray(bytearray(uploaded_file.read()))
    opencv_image = cv2.imdecode(file_bytes, 1)
# Read the file to predict
    x = cv2.resize(opencv_image, (W, H))
    x = x / 255.0
    x = x.astype(np.float32)  
# Make the prediction
    y_pred = model.predict(np.expand_dims(x, axis=0))[0]     
    y_pred[np.where(y_pred> binary_threshold)] = 4 
    y_pred[np.where(y_pred <= binary_threshold)] = 0
    y_pred = y_pred.astype(np.uint8)
    y_pred = np.concatenate([y_pred, y_pred, y_pred], axis=2)                                 # create 3 equal channels for RGB
    y_pred = cv2.resize(y_pred, (PLOTTING_WIDTH,PLOTTING_HEIGHT), interpolation = cv2.INTER_NEAREST) 

# Convert to plot
    mask_fat_color ='red' 
    mask_muscle_color ='blue' # choose a predefined matplotlib color https://matplotlib.org/3.1.0/gallery/color/named_colors.html
    prediction_fat_color ='red'  
    prediction_muscle_color ='blue' 
    color1='red'
    color2='blue'    
    
    img = Image.fromarray(y_pred)
    img = np.array(img.convert('RGBA')).astype(np.uint8)
    
    mask_fat = (img[:,:,2] == 4)  
    mask_muscle = (img[:,:,2] == 1)
    img[:,:,3] = 0
    img[:,:,3][np.where(mask_fat| mask_muscle) ] = 255

    R, G, B = np.multiply(mcolors.to_rgb(color1),255).astype(np.uint8)
    img[:,:,0][np.where(mask_fat)] =R
    img[:,:,1][np.where(mask_fat)] =G
    img[:,:,2][np.where(mask_fat)] =B

    R, G, B = np.multiply(mcolors.to_rgb(color2),255).astype(np.uint8)
    img[:,:,0][np.where(mask_muscle)] =R
    img[:,:,1][np.where(mask_muscle)] =G
    img[:,:,2][np.where(mask_muscle)] =B
    
    original = cv2.resize(opencv_image, (PLOTTING_WIDTH, PLOTTING_HEIGHT)) 
    original = cv2.cvtColor(original, cv2.COLOR_BGR2BGRA)
###########         ##### create the overlay images  ###########  
 # choose level of transparency for first and second picture
    merged_prediction = cv2.addWeighted(img, 1, original, 0.6, 0)
    
############################################### create legend ####################################################

    colors = [mask_fat_color]
    texts = ["Fat tissue"]
    patches = [ mpatches.Patch(color=colors[i], label="{:s}".format(texts[i]) ) for i in range(len(texts)) ]
############### PLOT############################################################################################   

#         ########  plot  #########
    fig, axs = plt.subplots(1,2, figsize=(20, 20))
    axs[0].set_title("Original", fontsize=30)
    axs[0].imshow(original)
    axs[1].set_title("Prediction", fontsize=30)
    axs[1].imshow(merged_prediction)
    axs[1].legend(handles=patches, bbox_to_anchor=(0.0, 0.0), loc='lower left', ncol=1, fontsize=30 )
    return fig, axs


