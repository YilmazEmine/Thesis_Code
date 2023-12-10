import cv2
import numpy as np
import csv
import os
def calculate_gcc(image_path):
    img = cv2.imread(image_path)
    # define roi
    roi = (78, 360, 603, 663)
    x, y, w, h = roi
    cropped_image = img[y:y+h, x:x+w]
    b, g, r = cv2.split(cropped_image)
    # Convert to numpy arrays
    r_array = np.array(r, dtype=float)
    g_array = np.array(g, dtype=float)
    b_array = np.array(b, dtype=float)
    # Calculate GGC index
    epsilon = 1e-10
    ggc_index = g_array / (r_array + g_array + b_array + epsilon)
    return np.mean(ggc_index)
# Paths
base_path = 'D:/TEZ/TEZ_01/CORN/PHENOCAM_IMAGES'
csv_file = 'D:/TEZ/TEZ_01/CORN/PHENOCAM_IMAGES/code_phenocam_res.csv'
# Years, stages, and methods to iterate over
years = ['2017', '2018', '2020', '2021']
stages = ['emergence', 'silking', 'dough', 'dent', 'mature', 'harvest']
methods = ['cpr', 'tbm','macd']
# Process each image
for year in years:
    for stage in stages:
        for method in methods:
            folder_path = f'{base_path}/{year}_{stage}_{method}'
            if os.path.exists(folder_path):
                for file in os.listdir(folder_path):
                    if file.endswith('.jpg'):
                        image_path = os.path.join(folder_path, file)
                        mean_ggc = calculate_gcc(image_path)
                        print(year, stage, method, mean_ggc)
                        data_to_write = [year, stage, method, mean_ggc]
                        with open(csv_file, mode='a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(data_to_write)
