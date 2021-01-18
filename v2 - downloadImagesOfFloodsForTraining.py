# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 19:42:20 2021

Source: https://www.analyticsvidhya.com/blog/2020/08/web-scraping-selenium-with-python/

@author: p1p29
"""
#Step 1 – Import all required libraries

import os
from selenium import webdriver
import time
from PIL import Image
import io
import requests
from webdriver_manager.chrome import ChromeDriverManager
#from webdriver_manager.firefox import GeckoDriverManager

os.chdir('C:/Users/p1p29/Monitor for floods')

#Step 2 – Install Chrome Driver

#Install driver
opts=webdriver.ChromeOptions()
opts.headless=True

driver = webdriver.Chrome(ChromeDriverManager().install() ,options=opts)
#driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

#In this step, we’re installing a Chrome driver and using a headless browser for web scraping.

#Step 3 – Specify search URL

search_url = "https://www.google.com.sg"
driver.get(search_url.format(q='Car'))

#I’ve used this specific URL to scrape copyright-free images.
 
#Step 4 –  Write a function to take the cursor to the end of the page

def scroll_to_end(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)#sleep_between_interactions

#This snippet of code will scroll down the page

#Step5. Write a function to get URL of each Image

#no license issues

def getImageUrls(name,totalImgs,driver):
    
    search_url = "https://www.google.com/search?q={q}&tbm=isch&tbs=sur%3Afc&hl=en&ved=0CAIQpwVqFwoTCKCa1c6s4-oCFQAAAAAdAAAAABAC&biw=1251&bih=568"
    driver.get(search_url.format(q=name))
    img_urls = set()
    img_count = 0
    results_start = 0  
    
    while(img_count<totalImgs): #Extract actual images now
        
        scroll_to_end(driver)
        
        thumbnail_results = driver.find_elements_by_xpath("//img[contains(@class,'Q4LuWd')]")
        totalResults=len(thumbnail_results)
        print(f"Found: {totalResults} search results. Extracting links from {results_start}:{totalResults}")
        
        for img in thumbnail_results[results_start:totalResults]:
            
            img.click()
            time.sleep(2)
            actual_images = driver.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'https' in actual_image.get_attribute('src'):
                    img_urls.add(actual_image.get_attribute('src'))
            
            img_count=len(img_urls)
            
            if img_count >= totalImgs:
                print(f"Found: {img_count} image links")
                break
            else:
                print("Found:", img_count, ". Looking for more image links...")                
                load_more_button = driver.find_element_by_css_selector(".mye4qd")
                driver.execute_script("document.querySelector('.mye4qd').click();")
                results_start = len(thumbnail_results)
    return img_urls

#This function would return a list of URLs for each category (e.g. Cars, horses, etc.)

#Step 6: Write a function to download each Image

def downloadImages(folder_path,file_name,url):
    try:
        image_content = requests.get(url).content
    except Exception as e:
        print(f"ERROR - COULD NOT DOWNLOAD {url} - {e}")
    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
       
        file_path = os.path.join(folder_path, file_name)
        
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SAVED - {url} - AT: {file_path}")
    except Exception as e:
        print(f"ERROR - COULD NOT SAVE {url} - {e}")

#This snippet of code will download the image from each URL.
 
#Step7: – Write a function to save each Image in the Destination directory

def saveInDestFolder(searchNames,destDir,totalImgs,driver):
    for name in list(searchNames):
        path=os.path.join(destDir,name)
        if not os.path.isdir(path):
            os.mkdir(path)
        print('Current Path',path)
        totalLinks=getImageUrls(name,totalImgs,driver)
        print('totalLinks',totalLinks)

        if totalLinks is None:
            print('images not found for :',name)
            continue
        else:
            for i, link in enumerate(totalLinks):
                file_name = str(1000+i)+".jpeg"
                downloadImages(path,file_name,link)
            
searchNames=['Flood'] 
destDir='./Train/'
totalImgs=50

saveInDestFolder(searchNames,destDir,totalImgs,driver)