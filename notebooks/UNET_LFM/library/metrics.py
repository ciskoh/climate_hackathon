# -*- coding: utf-8 -*-

import tensorflow as tf
from tensorflow.keras import backend as K

num_classes = 3

def dice_coef(y_true, y_pred, smooth=1e-7):
    y_true = tf.dtypes.cast(y_true, tf.float32)
    intersection = K.sum(y_true * y_pred, axis=(0,1,2))
    union = K.sum(y_true, axis=(0,1,2)) + K.sum(y_pred, axis=(0,1,2))
    dice = K.mean((2. * intersection + smooth)/(union + smooth), axis=0)
    return dice

def dice_coef_for_eval(y_true, y_pred, smooth=1e-7):
    '''applies threshold to y_pred to transform sigmoid values to 0 and 1'''
    binary_threshold = 0.5
    y_true = tf.dtypes.cast(y_true, tf.float32)
    y_pred = K.cast(K.greater(K.clip(y_pred, 0, 1), binary_threshold), K.floatx())
    y_pred = K.cast(K.less(K.clip(y_pred, 0, 1), binary_threshold), K.floatx())
    intersection = K.sum(y_true * y_pred, axis=(0,1,2))
    union = K.sum(y_true, axis=(0,1,2)) + K.sum(y_pred, axis=(0,1,2))
    dice = K.mean((2. * intersection + smooth)/(union + smooth), axis=0)
    return dice

def generalized_dice_coef(y_true, y_pred, ncl = num_classes, smooth=1e-7):
    ''' use this function to over/underemphasize certain classes by multiplying with weight coefficients'''
    weights = [1, 1, 1]
    y_true = tf.dtypes.cast(y_true, tf.float32)
    intersect = y_true*y_pred
    intersect = weights*K.sum(intersect,axis=(0,1,2))
    denom = weights * K.sum(y_true+ y_pred, axis=(0,1,2))
    gdc =  K.mean(2. * intersect / (denom + smooth))
    return gdc

def dice_coef_c1(y_true, y_pred, ncl = num_classes, smooth=1e-7):

    weights=[1.0, 0.00, 0.0]
    y_true = tf.dtypes.cast(y_true, tf.float32)
    intersect = y_true*y_pred
    intersect = weights*K.sum(intersect,axis=(0,1,2))
    intersect = K.sum(intersect)
    denom = weights * K.sum(y_true + y_pred, axis=(0,1,2))
    denom = K.sum(denom)
    gdc =  (2. * intersect / (denom + smooth))
    return gdc

def dice_coef_c2(y_true, y_pred, ncl = num_classes, smooth=1e-7):

    weights=[0.0, 1.0, 0.0]
    y_true = tf.dtypes.cast(y_true, tf.float32)
    intersect = y_true*y_pred
    intersect = weights*K.sum(intersect,axis=(0,1,2))
    intersect = K.sum(intersect)
    denom = weights * K.sum(y_true + y_pred, axis=(0,1,2))
    denom = K.sum(denom)
    gdc =  (2. * intersect / (denom + smooth))
    return gdc

def dice_coef_c3(y_true, y_pred, ncl = num_classes, smooth=1e-7):

    weights=[0.0, 0.0, 1.0]
    y_true = tf.dtypes.cast(y_true, tf.float32)
    intersect = y_true*y_pred
    intersect = weights*K.sum(intersect,axis=(0,1,2))
    intersect = K.sum(intersect)
    denom = weights * K.sum(y_true + y_pred, axis=(0,1,2))
    denom = K.sum(denom)
    gdc =  (2. * intersect / (denom + smooth))
    return gdc

def generalized_dice_loss(y_true, y_pred):
    return 1 - generalized_dice_coef(y_true, y_pred)

def dice_loss(y_true, y_pred):
    return 1 - dice_coef(y_true, y_pred)

def weighted_categorical_crossentropy(y_true, y_pred):
    weights = [0.01, 0.01, 1]
    Kweights = K.constant(weights)
    if not tf.is_tensor(y_pred):
        y_pred = K.constant(y_pred)
    y_true = K.cast(y_true, y_pred.dtype)
    result = K.categorical_crossentropy(y_true, y_pred) * K.sum(y_true * Kweights, axis=-1)
    return result

def binary_dice_coef(y_true, y_pred):
    smooth = 1e-15
    y_true = tf.keras.layers.Flatten()(y_true)
    y_pred = tf.keras.layers.Flatten()(y_pred)
    intersection = tf.reduce_sum(y_true * y_pred)
    return (2. * intersection + smooth) / (tf.reduce_sum(y_true) + tf.reduce_sum(y_pred) + smooth)

def binary_dice_coef_for_eval(y_true, y_pred):
    '''applies threshold to y_pred to transform sigmoid to 0 and 1'''
    smooth = 1e-15
    binary_threshold = 0.5
    y_true = tf.keras.layers.Flatten()(y_true)
    y_pred = tf.keras.layers.Flatten()(y_pred)
    y_pred = K.cast(K.greater(K.clip(y_pred, 0, 1), binary_threshold), K.floatx())
    intersection = tf.reduce_sum(y_true * y_pred)
    return (2. * intersection + smooth) / (tf.reduce_sum(y_true) + tf.reduce_sum(y_pred) + smooth)

def binary_dice_loss(y_true, y_pred):
    return 1.0 - binary_dice_coef(y_true, y_pred)

def dice_coef_metric(y_true, y_pred):
    smooth = 1e-15
    y_true = tf.keras.backend.cast(y_true, dtype="float32")
    y_pred = tf.keras.backend.cast(y_pred, dtype="float32")
    y_pred_b = y_pred > 0.5
    y_pred_b = tf.keras.backend.cast(y_pred_b, dtype="float32")
    elementwise_mult = tf.math.multiply(y_true, y_pred_b)
    intersection = tf.keras.backend.sum(elementwise_mult, axis=[1, 2, 3])
    dice_coef = (2. * intersection + smooth) / (tf.keras.backend.sum(y_true, axis=[1, 2, 3])
                                            + tf.keras.backend.sum(y_pred_b, axis=[1, 2, 3]) + smooth)
    return dice_coef
def dice_coef_loss(y_true, y_pred):
    smooth = 1e-15
    y_true = tf.keras.backend.cast(y_true, dtype="float32")
    y_pred = tf.keras.backend.cast(y_pred, dtype="float32")
    elementwise_mult = tf.math.multiply(y_true, y_pred)
    intersection = tf.keras.backend.sum(elementwise_mult, axis=[1, 2, 3])
    return 1 - (2. * intersection + smooth) / (tf.keras.backend.sum(y_true, axis=[1, 2, 3]) 
                                               + tf.keras.backend.sum(y_pred, axis=[1, 2, 3]) + smooth)