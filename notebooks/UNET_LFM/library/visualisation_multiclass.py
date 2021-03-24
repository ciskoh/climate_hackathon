# -*- coding: utf-8 -*-


from PIL import Image
import numpy as np
import cv2
import matplotlib.colors as mcolors


def read_image_plotting(path, width, height):
  ''' reads an image and resizes but WITHOUT normalizing'''
  x = cv2.imread(path, cv2.IMREAD_COLOR)
  x = cv2.cvtColor(x, cv2.COLOR_BGR2BGRA)
  x = cv2.resize(x, (width, height))
  return x

def create_overlay(img, width=256, height=256, color1='red', color2='green'):
    '''createas a RGBA image in form of a numpy array. Loads binary, grayscale 
  or color image and transforms black values to color, and white values to trasparent'''
    img= np.array(img.convert('RGBA')).astype(np.uint8) 
    mask_fat = (img[:,:,2] == 2*255/3)  
    mask_muscle = (img[:,:,2] == 1*255/3)
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

def crop_image(image_array, box):
  ''' crops an image to size of box'''
  cropped_image = Image.fromarray(image_array)
  cropped_image = cropped_image.crop(box) 
  return cropped_image

def convert_mask(path):
  img = Image.open(path)
  img = np.array(img)
  img[np.where(img== 255)] = 4
  img = Image.fromarray(img)                                            
  return img

def read_original_size(image_path):
  x = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
  shape = x.shape
  width = shape[1]
  height = shape[0]
  color_channels = shape [2]
  return width, height, color_channels

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


def read_original_size(image_path):
  x = cv2.imread(image_path, cv2.IMREAD_COLOR)
  shape = x.shape
  width = shape[1]
  height = shape[0]
  color_channels = shape[2]
  return width, height, color_channels

def mask_to_255(path):
  '''converts pixel values from 0-1 to 0-255'''
  img = Image.open(path)
  img = np.array(img)
  img[np.where(img== 4)] = 170 #3 = num_classes
  img[np.where(img== 1)] = 85 #3 = num_classes
  img = Image.fromarray(img)
  return img