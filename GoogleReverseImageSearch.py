# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 20:01:56 2021

Source: https://stackoverflow.com/questions/23270175/google-reverse-image-search-using-post-request

@author: p1p29
"""
import requests
import webbrowser
from keras.preprocessing.image import ImageDataGenerator

check_datagen = ImageDataGenerator(rescale=1./255)
check_generator = check_datagen.flow_from_directory(
        "Check", 
        target_size=(150, 150),
        batch_size=2,
        class_mode='binary',
        shuffle=False)

"""Files in './Check/images/' would be checked. It is important to respect the logic of the data generator, so the subfolder /images/ is required."""
for filename in check_generator.filenames:
    filePath = 'Check/' + filename
    searchUrl = 'http://www.google.com.sg/searchbyimage/upload'
    multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
    response = requests.post(searchUrl, files=multipart, allow_redirects=False)
    fetchUrl = response.headers['Location']
    webbrowser.open(fetchUrl)
