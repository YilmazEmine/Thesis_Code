1. vi_seasonal_loop --> Download sentinel satellite data with wcs requeest and calculate MSAVI and NDVI
2. merge_msavi_ndvi_03 --> merge msavi and ndvi depending on a threshold
3. preprocess_04_all --> apply median filter and savitzky-golay filter to merged vi data
4. TBM_2x2_plot, MACD_2X2_Plot --> plot the estimated phenological dates and cpr dates with vi data
5. gcc_calculation --> green chromatic coordinate calculation for phenocam images
6. rasters_plot --> plot raster data code example for further use
