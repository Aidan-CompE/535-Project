select_columns.py
This script takes the 10 raw participants data and selects the columns we want to train and experiment on. This includes the headset and controller position and rotation data and the eye gaze data. It takes five minute sessions from each person and creates new processed data and puts the processed CSV files in our correct folder for processed data.

ALSO BE CAREFUL RUNNING ˆˆˆ this script will overwrite the CSV files if ran again and also if we delete a participant from the code, it's not going to automatically delete their data

check_data.py
This script checks that there are no missing values, values are numeric, elapsed timestamps are increasing, there are not any duplicate timestamps, and there are no gaps longer than a second. The data surprisingly passed all these checks making our job much easier.




