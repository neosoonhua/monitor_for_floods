20 Jan 2021:

I used the following code to download 50 photos of floods for training.

https://github.com/neosoonhua/monitor_for_floods/blob/main/v2%20-%20downloadImagesOfFloodsForTraining%20-%20webdriver_manager%20requires%20Python%203Point8.py

Still very lousy accuracy. I then searched online and found that it's much more difficult than I thought.

https://www.technologyreview.com/2019/08/30/133206/ai-image-recognition-improves-disaster-response/

https://www.govtech.com/products/Virginia-Researchers-Work-to-Create-AI-Flood-Warning-System.html

-----------------
15 Jan 2021:

I haven't made any user interface. Have to install software to run the R code and Python code.

Currently, I set the code to show only those classified as "no flood" because none was classified as "flood" when I tested. Need to train the AI with more photos before changing the setting to show only those classified as "flood".

Steps:
1) Run "v4a - floodRecognitionJpeg - trainModelAndSave.py" to train the AI model and save the model.
2) Run "download_images_periodically.r" which would download the photos every 5 minutes.
3) Run "v4b - floodRecognitionJpeg - loadModelThenTestPeriodically.py" which would load the model and - every 5 minutes - classify each photo with "Flood", "No flood" or "Blue image".
