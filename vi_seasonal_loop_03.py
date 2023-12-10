from concurrent.futures import ThreadPoolExecutor
import os
import requests
import geopandas as gpd
import pandas as pd
import rasterio
import numpy as np
dest_file = 'D:/TEZ/TEZ_01/CORN/TRAIN/'
sentinelLayerName1 = 'B04'
sentinelLayerName2 = 'B08'
# shp bbox definition #
def calculate_field(shape_name):
    shapefile = f'D:/DATA/corn_field/{shape_name}'
    print (shapefile)
    sf = gpd.read_file(shapefile)
    sf = sf.to_crs(epsg=4326)
    bbox = sf.geometry.total_bounds # BBOX calculated here 
    bir = bbox[0]
    iki = bbox[1]
    uc = bbox[2]
    dort = bbox[3]
    myBbox = str(dort) + "," +str(uc) + ","+  str(iki) + "," + str(bir)
    return myBbox
# date list creation #
def calculate_date(year):
    dates = pd.date_range(start=f'{year}-01-05', end=f'{year}-12-31', freq='5D')
    date_list = dates.to_list()
    return date_list
# sentinel wcs request #
def getSentinelData (sentinelLayerName, date1, myBbox, dest_file, shape_name):
    myBbox = calculate_field(shape_name)
    urlStr1 = "https://services.sentinel-hub.com/ogc/wcs/4a0cfd6b-f48a-458b-8593-b62f04acf80b?SERVICE=WCS&REQUEST=GetCoverage&Coverage="
    urlStr2 = sentinelLayerName + "&format=GeoTiff&CRS=EPSG:4326&" 
    myurl = urlStr1 + urlStr2   + "bbox=" + myBbox
    resXStr = "&RESX="
    resYStr = "&RESY="
    myurl = myurl + resXStr + "1m" + resYStr + "1m" + "&TIME=" + str(date1)
    print(myurl)   
    indir  = requests.get(myurl, allow_redirects=True)
    # Check if the request was successful
    if indir.status_code == 200:
        with open(os.path.join( dest_file + shape_name + '_' + sentinelLayerName + "_" + date1 + ".tiff"),'wb') as file:
            file.write(indir.content)
    else:
        print(f"Request failed with error {indir.status_code}.")
# read rester data from file to calculate msavi and ndvi #
def openRaster(dest_file, shape_name , sentinelLayerName, date1, output):
    with rasterio.open(dest_file  + shape_name + '_' + sentinelLayerName + "_" + date1 + ".tiff" ) as src:
        output = src.read(1, masked = True)
        output = output.astype(float)
        transform = src.transform  
    return output,transform
#calculate index funcions
def calculate_msavi (NIR, RED):
    #(2 * Band 5 + 1 – sqrt ((2 * Band 5 + 1)2 – 8 * (Band 5 – Band 4))) / 2.
    msavi = 0.5 * (((2 * NIR + 1)) - np.sqrt((2 * NIR + 1)**2 - 8 * (NIR - RED)))
    return msavi
def calculate_ndvi (NIR, RED):
    ndvi = (NIR - RED) / (NIR + RED)
    return ndvi
# call for sentinel request, calculate msavi, ndvi, write folder 
def process_date(shape_name, year):
    dates = pd.date_range(start=f'{year}-01-05', end=f'{year}-12-31', freq='5D')
    for single_date in dates:
        print('single_date=',single_date)
        date_str = single_date.strftime('%Y-%m-%d')
        print('date_str=',date_str)
        filename_B08 = dest_file + shape_name + 'B08_' + date_str + '.tiff'
        filename_B04 = dest_file + shape_name + 'B04_' + date_str + '.tiff'
        if os.path.isfile(filename_B08) and os.path.isfile(filename_B04):
            B08, B08_transform = openRaster(dest_file,shape_name , 'B08', date_str, 'B08')
            B04, B04_transform = openRaster(dest_file,shape_name ,'B04', date_str, 'B04')
        else:
            B08 = getSentinelData(sentinelLayerName1, date_str, myBbox, dest_file, shape_name)
            B04 = getSentinelData(sentinelLayerName2, date_str, myBbox, dest_file, shape_name)
            B08, B08_transform = openRaster(dest_file,shape_name  ,'B08', date_str, 'B08')
            B04, B04_transform = openRaster(dest_file,shape_name ,'B04', date_str, 'B04')
        try:
            msavi = calculate_msavi(B08, B04)
            ndvi = calculate_ndvi(B08, B04)
            msavi_filename = f'D:/TEZ/TEZ_01/CORN/TRAIN/MSAVI/{shape_name}msavi_' + date_str + '.tiff'
            ndvi_filename = f'D:/TEZ/TEZ_01/CORN/TRAIN/NDVI/{shape_name}ndvi_' + date_str + '.tiff'
            # Save msavi to a file
            with rasterio.open(msavi_filename, 'w', driver='GTiff', height=msavi.shape[0], width=msavi.shape[1], 
                        count=1, dtype=msavi.dtype, crs='+proj=latlong', transform=B08_transform) as dst:
                dst.write(msavi, 1)
            # Save ndvi to a file
            with rasterio.open(ndvi_filename, 'w', driver='GTiff', height=ndvi.shape[0], width=ndvi.shape[1], 
                        count=1, dtype=ndvi.dtype, crs='+proj=latlong', transform=B08_transform) as dst:
                dst.write(ndvi, 1)
        except ZeroDivisionError:
            print('zero division')
field_list = ['1','2','3','4','5','6','7','8','9','10','11']
year_list = ['2017', '2018', '2019', '2020', '2021', '2022']
# RUN DOWNLOAD DATA # 
for field in field_list:
    for year in year_list:
        print(field)
        print(year)
        f = field + '.shp'
        print(f)
        myBbox = calculate_field(f)
        process_date( f, year)
# CALCULATES MSAVI AND NDVI AND CREATE CSV #
def read_msavi(date_str, dest_file, shape_name):
    try:
        msavi_filename = f'{dest_file}MSAVI/{shape_name}msavi_{date_str}.tiff' 
        print(msavi_filename)
        with rasterio.open(msavi_filename) as msavi:
            MSAVI = msavi.read(1, masked = True)
            #MVI, _ = rasterio.mask.mask(msavi, masking_shp, crop=True) # type: ignore
            MSAVI  = MSAVI.astype(float)
        return MSAVI     
    except FileNotFoundError:
        print('Go back to look msavi calculation loop or look file name')
def read_ndvi(date_str, dest_file, shape_name):
    try:
        ndvi_filename = f'{dest_file}NDVI/{shape_name}ndvi_{date_str}.tiff' 
        print(ndvi_filename)
        with rasterio.open(ndvi_filename) as ndvi:
            NDVI = ndvi.read(1, masked = True)
            NDVI  = NDVI.astype(float)
        return NDVI     
    except FileNotFoundError:
        print('Go back to look ndvi calculation loop or look file name')
### READ msavi FROM FILE AND CALCULATE MEAN AND CREATE mean_msavi_list######
for shape_name in field_list:
    f = shape_name + '.shp'
    for y in year_list:
        date_list = calculate_date(y)
        print(date_list)
        msavi_list = []
        ndvi_list = []
        mean_msavi_list = []
        mean_ndvi_list = []
        for date in date_list:
            date_str = date.strftime('%Y-%m-%d')
            msavi = read_msavi(date_str, dest_file, f)  
            ndvi =  read_ndvi(date_str, dest_file, f)  
            msavi_list.append((date, msavi))
            ndvi_list.append((date, ndvi))
            # Replace zeros with NaNs
            msavi[msavi == 0] = np.nan  
             # Calculate the mean msavi, ignoring NaN values
            mean_msavi = np.nanmean(msavi) 
            mean_msavi_list.append(mean_msavi)
             # Replace zeros with NaNs
            ndvi[ndvi == 0] = np.nan 
            # Calculate the mean msavi, ignoring NaN values
            mean_ndvi = np.nanmean(ndvi)  
            mean_ndvi_list.append(mean_ndvi)
            # Create a pandas dataframe to hold the date and corresponding mean msavi
        print('Mistakes Comes From lengths', len(date_list), len(mean_msavi_list))
        mean_msavi_df = pd.DataFrame({
                'date': date_list,
                'mean_msavi': mean_msavi_list
                })
        mean_ndvi_df = pd.DataFrame({
                'date': date_list,
                'mean_ndvi': mean_ndvi_list
                })
        msavi_csv_path = f'{dest_file}/TRAIN_code_to_csv/{shape_name}_{y}_msavi.csv'
        print('msavi csv path=', msavi_csv_path)
        ndvi_csv_path = f'{dest_file}/TRAIN_code_to_csv/{shape_name}_{y}_ndvi.csv'
        mean_msavi_df.to_csv(msavi_csv_path, index=False)
        mean_ndvi_df.to_csv(ndvi_csv_path, index=False)