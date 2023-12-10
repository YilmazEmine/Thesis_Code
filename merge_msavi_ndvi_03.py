from scipy.interpolate import UnivariateSpline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
field_list = ['1','2','3','4','5','6','7','8','9','10','11']
year_list = ['2017', '2018', '2019', '2020', '2021', '2022']
# RMERGE MSAVI AND NDVI # 
for field in field_list:
    for year in year_list:
        # read data
        msavi_file_path = f'D:/TEZ/TEZ_01/CORN/TRAIN/TRAIN_code_to_csv/{field}_{year}_msavi.csv'
        msavi_df = pd.read_csv(msavi_file_path)
        ndvi_file_path = f'D:/TEZ/TEZ_01/CORN/TRAIN/TRAIN_code_to_csv/{field}_{year}_ndvi.csv'
        ndvi_df = pd.read_csv(ndvi_file_path)
        # Convert 'date' to datetime format for both dataframes
        msavi_df['date'] = pd.to_datetime(msavi_df['date'])
        ndvi_df['date'] = pd.to_datetime(ndvi_df['date'])
        # Merge the two dataframes on 'date'
        merged_df = pd.merge(msavi_df, ndvi_df, on='date', how='inner')    
        # Replace 'mean_msavi' values greater than 0.6 with corresponding 'mean_ndvi' values
        merged_df.loc[merged_df['mean_msavi'] > 0.6, 'mean_msavi'] = merged_df.loc[merged_df['mean_msavi'] > 0.6, 'mean_ndvi']
        csv_file = f'D:/TEZ/TEZ_01/CORN/TRAIN/TRAIN_code_to_csv/merged/{field}_{year}_merged.csv'
        merged_df.to_csv(csv_file, index=False)