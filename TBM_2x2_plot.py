import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
# Define the years to plot
years = [2017, 2018, 2020, 2021]
font_leg = 18
font_title = 22
font_axis = 18
font_axis_label = 20
folder_path = 'D:/TEZ/TEZ_01/CORN/TRAIN/TRAIN_code_to_csv/phenocam_results/'
fig, axs = plt.subplots(4,1, figsize=(15, 18), constrained_layout=True)
axs = axs.flatten()  
for i, year in enumerate(years):
    # Load the data for the current year
    file_path = f"{folder_path}sg_filter_df_{year}_with_predictions.csv"
    data = pd.read_csv(file_path)
    data['date'] = pd.to_datetime(data['date'])
    # Plot the sg_filter_values on the current subplot
    axs[i].plot(data['date'], data['sg_filter_values'], label='Pre-Processed TS VI Data', linewidth=2, color='red')
    # Add scatter plots for pure_msavi and pure_ndvi on the current subplot
    axs[i].scatter(data['date'], data['pure_msavi'], marker='^', color='gray', label='MSAVI')
    axs[i].scatter(data['date'], data['pure_ndvi'], color='gray', label='NDVI')
    # Add vertical lines for cpr on the current subplot
    if 'cpr' in data.columns:
        for cdate in data['date'][data['cpr'].notnull()]:
            axs[i].axvline(cdate, color='black', linestyle='--', label='CPR' if 'CPR' not in [l.get_label() for l in axs[i].lines] else "")
    # Add blue points for rf week with specified customizations on the current subplot
    if 'rf week' in data.columns:
        rf_week_dates = data['date'][data['rf week'].notnull()]
        rf_week_values = data['sg_filter_values'][data['rf week'].notnull()]
        axs[i].scatter(rf_week_dates, rf_week_values, facecolors='white', edgecolors='blue', zorder = 5, linewidth=3, s=200, label='TBM Predicted Dates')
    # Add a gray dashed line for mean_msavi on the current subplot
    axs[i].plot(data['date'], data['mean_msavi'], color='gray', linestyle='--', label='Merged TS VI')
    # Formatting date ticks on the current subplot
    axs[i].xaxis.set_major_locator(mdates.MonthLocator(bymonth=range(1, 13, 2)))
    axs[i].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    # Rotate date labels for better readability
    plt.setp(axs[i].get_xticklabels(),  ha='right')
    # Add grid, legend, and title to each subplot
    axs[i].grid(True)
    #axs[i].legend(fontsize = font_leg)
    axs[i].set_title(f'TBM Estimated Dates {year}', fontsize = font_title)
    # Add x and y-axis labels
    axs[i].set_ylabel('VI Data', fontsize=font_axis_label)
    axs[i].set_xlabel('Date', fontsize=font_axis_label)
    axs[i].xaxis.set_tick_params(labelsize=font_axis)
    axs[i].yaxis.set_tick_params(labelsize=font_axis)
handles_list = []
labels_list = []
# Loop through each axis object to get the handles and labels
for ax in axs.flat:
    handles, labels = ax.get_legend_handles_labels()
    for handle, label in zip(handles, labels):
        # Add the handle and label to the list if the label is not already in the list
        if label not in labels_list:
            handles_list.append(handle)
            labels_list.append(label)
# Adjust the layout
plt.tight_layout()
fig.legend(handles_list, labels_list, loc='upper center', bbox_to_anchor=(0.5, 0), ncol=3, fontsize=font_leg)
save_dir = 'D:/TEZ/TEZ_01/LATEX/METU-Thesis-Template/figures/results/'
#plt.savefig(f"{save_dir}tbm_res.png", bbox_inches='tight')
#plt.savefig(f"{save_dir}tbm_4x1_res.png", bbox_inches='tight')
# Show the plot
plt.show()
