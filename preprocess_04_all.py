from scipy.interpolate import UnivariateSpline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
from scipy.signal import savgol_filter, medfilt
from scipy.optimize import curve_fit
from scipy.stats import linregress
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
def preprocess(df, field ,year):
    # Convert 'date' column to DateTime format, if it exists
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    # Check for missing values and forward fill if any
    if df.isnull().sum().any():
        df.fillna(method='ffill', inplace=True)
    # Sort the DataFrame by date
    df = df.sort_values('date')
    # Extract mean_msavi and date for plotting and filtering
    x_data = np.arange(len(df))
    y_data = df['mean_msavi'].values
    # Step 1: Median Filter
    kernel_size_median = 5  # Three-day temporal moving window as per paper
    median_spline_filter = medfilt(y_data, kernel_size=kernel_size_median)
    # Step 2: Savitzky-Golay (SG) Filter
    window_length_sg = 11
    polyorder_sg = 2
    sg_filter = savgol_filter(median_spline_filter, window_length=window_length_sg, polyorder=polyorder_sg)
    sg_filter_df = pd.DataFrame({
    'date': df['date'],
    'sg_filter_values': sg_filter
        })
    filtered_file = f'D:/TEZ/TEZ_01/CORN/TRAIN/TRAIN_code_to_csv/med_sg_filter/{field}_{year}.csv'
    sg_filter_df.to_csv(filtered_file, index=False)
# Loop through the years
field_list = ['1','2','3','4','5','6','7','8','9','10','11']
year_list = ['2017', '2018', '2019', '2020', '2021', '2022']
# MERGE MSAVI AND NDVI # 
for field in field_list:
    for year in year_list:
        msavi_file_path = f'D:/TEZ/TEZ_01/CORN/TRAIN/TRAIN_code_to_csv/merged/{field}_{year}_merged.csv'
        df = pd.read_csv(msavi_file_path)
        preprocess( df, field, year)
