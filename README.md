# monitor_for_floods
I haven't made any user interface. Have to install software to run the R code and Python code.

Currently, I set the code to show only those classified as "no flood" because none was classified as "flood" when I tested. Need to train the AI with more photos before changing the setting to show only those classified as "flood".

Steps:
1) Run "v4a - floodRecognitionJpeg - trainModelAndSave.py" to train the AI model and save the model.
2) Run "download_images_periodically.r" which would download the photos every 5 minutes.
3) Run "v4b - floodRecognitionJpeg - loadModelThenTestPeriodically.py" which would classify each photo with "Flood", "No flood" or "Blue image" every 5 minutes.
