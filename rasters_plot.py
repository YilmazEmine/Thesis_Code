from matplotlib.colors import ListedColormap
import rasterio
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import contextily as ctx
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import numpy as np
from rasterio import open as rasterio_open
datelist = {'cpr':'2017-04-25',
            'tbm': '2017-05-15',
             'macd':'2017-07-04' }
file_path_cpr = f'D:/TEZ/TEZ_01/CORN/phenocam/MSAVI/msavi_{datelist["cpr"]}.tiff'
file_path_tbm = f'D:/TEZ/TEZ_01/CORN/phenocam/MSAVI/msavi_{datelist["tbm"]}.tiff'
file_path_macd = f'D:/TEZ/TEZ_01/CORN/phenocam/MSAVI/msavi_{datelist["macd"]}.tiff'
save_directory = 'D:/TEZ/TEZ_01/plots/iecrs/clusters/'
# Read the raster data
with rasterio.open(file_path_cpr) as src:
    data = src.read(1)
    transform = src.transform
    sample_width = src.width  # Width of the raster in pixels
    sample_height = src.height  # Height of the raster in pixels
    crs = src.crs.to_string()
a = transform.a  # pixel size in the x-direction, longitude
e = transform.e  # pixel size in the y-direction,  latitude
c = transform.c  # x-coordinate of the upper-left corner (longitude)
f = transform.f  # y-coordinate of the upper-left corner (latitude)
sample_transform = {
    'c': c,  # bottom-left corner longitude
    'f': f,  # bottom-left corner latitude
    'a': a,  # pixel size in longitude direction
    'e': e  # pixel size in latitude direction
}
#  extent
bottom_left_lon = sample_transform['c']
bottom_left_lat = sample_transform['f']
top_right_lon = sample_transform['c'] + sample_transform['a'] * sample_width
top_right_lat = sample_transform['f'] + sample_transform['e'] * sample_height
#  figure and axis
fig, ax = plt.subplots(1,1,figsize=(10, 10), subplot_kw={'projection': ccrs.PlateCarree()})
# Plot raster
img_extent = (transform.c, transform.c + transform.a * src.width, 
              transform.f + transform.e * src.height, transform.f)
img = ax.imshow(data, origin="upper", extent=img_extent, cmap='RdYlGn')
# Add colorbar
plt.colorbar(img, ax=ax, label='MSAVI Values')
# Add title and labels
ax.set_title(f"CPR Emerged Date {datelist['cpr']} MSAVI")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
# Add gridlines and labels
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linestyle='--')
gl.xlabels_top = False
gl.ylabels_left = True
gl.ylabels_right = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
# Show plot
#plt.savefig(f"{save_directory}cpr_e_msavi.png")
plt.show()
with rasterio.open(file_path_tbm) as src_c:
    data = src_c.read(1)
    transform = src_c.transform
    crs = src_c.crs.to_string()
#  figure and axis
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': ccrs.PlateCarree()})
# Plot raster
img_extent = (transform.c, transform.c + transform.a * src.width, 
              transform.f + transform.e * src_c.height, transform.f)
img = ax.imshow(data, origin="upper", extent=img_extent, cmap='RdYlGn')
# Add colorbar
plt.colorbar(img, ax=ax, label='Clusters')
# Add title and labels
ax.set_title("MSAVI Emerged Date MSAVI")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
# Add gridlines and labels
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linestyle='--')
gl.xlabels_top = False
gl.ylabels_left = True
gl.ylabels_right = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
# Show plot
#plt.savefig(f"{save_directory}baresoil_cluster.png")
plt.show()
################
with rasterio.open(file_path_macd) as src_c:
    data = src_c.read(1)
    transform = src_c.transform
    crs = src_c.crs.to_string()
#  figure and axis
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': ccrs.PlateCarree()})
# Plot raster
img_extent = (transform.c, transform.c + transform.a * src.width, 
              transform.f + transform.e * src_c.height, transform.f)
img = ax.imshow(data, origin="upper", extent=img_extent, cmap='RdYlGn')
plt.colorbar(img, ax=ax, label='Clusters')
ax.set_title("MSAVI Emerged Date MSAVI")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linestyle='--')
gl.xlabels_top = False
gl.ylabels_left = True
gl.ylabels_right = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
#plt.savefig(f"{save_directory}baresoil_cluster.png")
plt.show()

