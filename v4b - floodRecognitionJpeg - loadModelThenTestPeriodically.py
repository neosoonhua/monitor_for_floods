# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 06:56:48 2021

Source of code below for testing: https://stackoverflow.com/questions/52270177/how-to-use-predict-generator-on-new-images-keras/55991598#55991598

@author: p1p29
"""
import numpy as np
import pandas as pd
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
import os
import time
import datetime

# Load model
model = load_model('C:/Users/p1p29/Monitor for floods/Model/keras_multiclass_flickr_model_with_target_size_at_150_by_150.hdf5')

#Images are stored in C:/Users/p1p29/Monitor for floods/Test/images/. The data generator will only look for images in subfolders of C:/Users/p1p29/Monitor for floods/Test (as specified in test_generator). 
"""It is important to respect the logic of the data generator, so the subfolder /images/ is required."""
#Each subfolder in C:/Users/p1p29/Monitor for floods/Test is interpreted as one class by the generator. Here, the generator will report Found x images belonging to 1 classes (since there is only one subfolder). If we make predictions, classes (as detected by the generator) are not relevant.

while True:
    test_datagen = ImageDataGenerator(rescale=1./255)
    test_generator = test_datagen.flow_from_directory(
            "C:/Users/p1p29/Monitor for floods/Test", 
            target_size=(150, 150),
            batch_size=2,
            class_mode='binary',
            shuffle=False)
    
    # Predict from generator (returns probabilities)
    pred=model.predict_generator(test_generator, steps=len(test_generator), verbose=1)
    
    # Get classes by np.round
    cl = np.round(pred)
    # Get filenames (set shuffle=false in generator is important)
    filenames=test_generator.filenames
    
    # Data frame
    results=pd.DataFrame({"file":filenames,"pr":pred[:,0], "class":cl[:,0]})
    
    # Data generators
    train_datagen = ImageDataGenerator(
          rescale=1./255,
          rotation_range=40,
          width_shift_range=0.2,
          height_shift_range=0.2,
          shear_range=0.2,
          zoom_range=0.2,
          horizontal_flip=True,
          fill_mode='nearest')
    
    base_dir = 'C:/Users/p1p29/Monitor for floods'
    train_dir = os.path.join(base_dir, 'Train')
    batch_size = 2 #20
    train_generator = train_datagen.flow_from_directory(
            # This is the target directory
            train_dir,
            # All images will be resized to 150x150
            target_size=(150, 150),
            batch_size=batch_size,
            # Since we use categorical_crossentropy loss, we need binary labels
            class_mode='categorical')
    
    labels = (train_generator.class_indices)
    labels = dict((v,k) for k,v in labels.items())
    
    predicted_class_indices=np.argmax(pred,axis=1)
    predictions = [labels[k] for k in predicted_class_indices]
    
    for i in range(len(predictions)):
        if predictions[i] == "No_flood":
            print(filenames[i] + ": No flood")
            
    print("Downloaded CCTV images at about:")
    print(datetime.datetime.now())

    time.sleep(29) #Pause for 300 seconds. "http://pub.cloudapp.net/CCTVS/" updates the CCTV images every 5 minutes. My machine takes about 4 minutes 31 seconds to run these code.

