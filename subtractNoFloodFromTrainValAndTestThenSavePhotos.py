# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 21:29:10 2021

Sources:
https://towardsdatascience.com/image-recognition-with-machine-learning-on-python-convolutional-neural-network-363073020588

https://stackoverflow.com/questions/52270177/how-to-use-predict-generator-on-new-images-keras/55991598#55991598

https://datascience.stackexchange.com/questions/65979/what-is-the-correct-way-to-call-keras-flow-from-directory-method

https://github.com/Bixi81/Python-ml/blob/master/keras_pretrained_imagerec_multiclass.py

@author: p1p29
"""
import tensorflow as tf # towardsdatascience.com wrote "tensorflow 2.0" but it has no keras even after I installed keras again. I then installed Tensorflow 1.14. Still no keras. I then installed keras. Still no keras. I restarted Spyder and had keras!
tf.__version__
import numpy as np
from numpy import asarray
import PIL
PIL.__version__
from PIL import Image
from keras.preprocessing.image import ImageDataGenerator
import os

seed=0
np.random.seed(seed) # fix random seed
#tf.random.set_seed(seed) #Tensorflow Version 1.14 has no attribute 'set_seed'. "conda install -c conda-forge tensorflow=2.0" in Anaconda Prompt seemed to work but "tf.__version__" in Spyder still gives '1.14.0' and 'set_seed()' still does not work.

################################################ DIR with training images
base_dir = './'
# Number training images
ntrain = 16
# Number validation images
nval  = 12
#Number of images for testing
ntest = 2
# Batch size
batch_size = 2 #20
# Number of classes (for training, output layer)
nclasses = 2
# input image dimensions
img_rows, img_cols = 640, 480 # number of pixels
# resized image dimensions
resized_img_rows, resized_img_cols = 640, 480 # number of pixels
nclasses = 2 # "0" for no flood, "1" for flood and "2" for the blue "image temporarily unavailable".
###############################################

"""Have to first run up to "second_filenames=second_generator.filenames" to make sure the order in first_filenames matches that in second_filenames."""

set = "Test" #"Train", "Val" or "Test"
n_images = ntest #ntrain, nval or ntest

#def subtractNoFlood(set, n_images):
first_dir = os.path.join(base_dir, set)
second_dir = os.path.join(base_dir, set+'2')

# Data generators
first_datagen = ImageDataGenerator(
      rescale=1./255,
      rotation_range=40,
      width_shift_range=0.2,
      height_shift_range=0.2,
      shear_range=0.2,
      zoom_range=0.2,
      horizontal_flip=True,
      fill_mode='nearest')

first_generator = first_datagen.flow_from_directory(
        # This is the target directory
        first_dir,
        # All images will be resized to 150x150
        target_size=(150, 150),
        batch_size=batch_size,
        # Since we use categorical_crossentropy loss, we need binary labels
        class_mode='categorical')

second_datagen = ImageDataGenerator(
      rescale=1./255,
      rotation_range=40,
      width_shift_range=0.2,
      height_shift_range=0.2,
      shear_range=0.2,
      zoom_range=0.2,
      horizontal_flip=True,
      fill_mode='nearest')

second_generator = second_datagen.flow_from_directory(
        # This is the target directory
        second_dir,
        # All images will be resized to 150x150
        target_size=(150, 150),
        batch_size=batch_size,
        # Since we use categorical_crossentropy loss, we need binary labels
        class_mode='categorical')
###############################################

# Get filenames (set shuffle=false in generator is important)
first_filenames=first_generator.filenames
second_filenames=second_generator.filenames

#X for images, Y for the digit in the image
X_first = np.ones(shape=(n_images,img_cols,img_rows))
X_first *= 255
#Before, I used "X_second = X_first" and "X_difference = X_first". The moment X_first changed, X_second and X_difference changed with it in the same way. Weird.
X_second = np.ones(shape=(n_images,img_cols,img_rows))
X_second *= 128
X_difference = np.ones(shape=(n_images,img_cols,img_rows))
X_difference *= 64

for i in range(0, n_images):
    print(first_filenames[i])
    img = Image.open(first_dir + '/' + first_filenames[i])
    img = img.convert('L') #'L' for greyscale. 'P' for colour.
    img = img.resize((resized_img_rows, resized_img_cols))
    #img.save("img.png")
    X_first[i] = img
    numpydata = asarray(img) 
    pilImage = Image.fromarray(numpydata) 
    pilImage.show()

    print(second_filenames[i])
    img2 = Image.open(second_dir + '/' + second_filenames[i])
    img2 = img2.convert('L')
    img2 = img2.resize((resized_img_rows, resized_img_cols))
    #img.save("img.png")
    X_second[i] = img2
    numpydata2 = asarray(img2) 
    pilImage2 = Image.fromarray(numpydata2) 
    pilImage2.show()

    X_difference[i] = X_first[i] - X_second[i]
    pilImage_difference = Image.fromarray(X_difference[i]) 
    pilImage_difference.show()
    if pilImage_difference.mode != 'RGB':
        pilImage_difference = pilImage_difference.convert('RGB')
    pilImage_difference.save(set + '_subtracted/' + first_filenames[i])

"""subtractNoFlood(set="Train", n_images=ntrain)
subtractNoFlood(set="Val", n_images=nval)
subtractNoFlood(set="Test", n_images=ntest)"""
