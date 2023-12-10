import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
# years to plot
years = [2017, 2018, 2020, 2021]
folder_path = 'D:/TEZ/TEZ_01/DATA/code_to_csv/macd_results/'
save_dir = 'D:/TEZ/TEZ_01/LATEX/METU-Thesis-Template/figures/results/'
font_leg = 18
font_title = 22
font_axis = 18
font_axis_label = 20
fig, axs = plt.subplots(4,1, figsize=(15, 20))
axs = axs.flatten() # for 4x1 plot 
# Loop through each year and create a subplot for each
for i, year in enumerate(years):
    # Calculate the row and column index for the current subplot
    row_idx = i // 2
    col_idx = i % 2
    prediction = f"{folder_path}/macd_res_{year}.csv"
    data = pd.read_csv(prediction)
    #ax = axs[row_idx, col_idx]  # for 2x2 plot
    ax = axs[i] # for 4x1 plot
    ax.plot(data['date'], data['macd'], label='MACD', linewidth=2, color='red')
    # Check 'signal_line' and 'macd_div' columns exist before plotting them
    if 'signal_line' in data.columns:
        ax.plot(data['date'], data['signal_line'], label='Signal Line',  color='orange')
    if 'macd_div' in data.columns:
        ax.plot(data['date'], data['macd_div'], label='MACD Divergence', color='purple')
    # Check 'macd week' and 'cpr' columns exist before adding circles
    if 'macd week' in data.columns:
        for week in data[data['macd week'].notna()]['date']:
            macd_value = data.loc[data['date'] == week, 'macd'].values[0]
            ax.scatter(week, macd_value, s=200, facecolors='none', edgecolors='green', 
                       label='Predicted Dates', zorder=10, alpha=1, linewidths=3, linestyle='-')
    if 'cpr' in data.columns:
        for week in data[data['cpr'].notna()]['date']:
            macd_value = data.loc[data['date'] == week, 'macd'].values[0]
            ax.axvline(week, color='black', linestyle='--', linewidth=2, alpha=1, label='CPR Dates')
    ax.set_ylabel('MACD Analysis', fontsize=font_axis_label)
    ax.set_title(f'MACD Estimated Dates {year}', fontsize=font_title)
    ax.grid(True)
    # Add secondary y-axis for 'mean_msavi' as dashed line graph
    ax2 = ax.twinx()
    # Add scatter plot for 'pure_msavi' and 'pure_ndvi' columns with gray color
    ax2.scatter(data['date'], data['pure_msavi'], marker='^', color='gray', alpha=0.5, label='MSAVI')
    ax2.scatter(data['date'], data['pure_ndvi'], marker='o', color='gray', alpha=0.5, label='NDVI')
    ax2.plot(data['date'], data['mean_msavi'], color='gray', alpha=0.5, linestyle='--', label='Merged TS VI')
    ax2.plot(data['date'], data['sg_filter_values'], color='gray', alpha=0.5, linestyle='-', label='Pre-Processed TS VI Data')
    ax2.set_ylabel('VI Data', fontsize=font_axis_label)
    ax2.tick_params(axis='y', labelcolor='black') 
    #ax2.legend(fontsize=font_leg, loc='upper left')
    # Remove duplicate labels
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.set_xlabel('Date', fontsize=font_axis_label)
    for label in ax.get_xticklabels():
        #label.set_rotation(45)
        label.set_fontsize(14)
    for label in ax.get_yticklabels():
        label.set_fontsize(14)
    ax.yaxis.label.set_size(14)
    ax2.yaxis.label.set_size(14)
    ax.xaxis.set_tick_params(labelsize=font_axis)
    ax.yaxis.set_tick_params(labelsize=font_axis)
    ax2.yaxis.set_tick_params(labelsize=font_axis)
for ax in axs.flat:
    # Set the locator for major ticks to show every week
    ax.xaxis.set_major_locator(ticker.MultipleLocator(12))
# Create an empty list to collect handles and labels
handles_list = []
labels_list = []
# Loop through each axis object to get the handles and labels
for ax in axs.flat:
    handles, labels = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    for handle, label,handle2, label2 in zip(handles, labels, handles2, labels2):
        # Add the handle and label to the list if the label is not already in the list
        if label not in labels_list:
            handles_list.append(handle)
            labels_list.append(label)
            handles_list.append(handle2)
            labels_list.append(label2)
# Create a single legend for the figure with the collected handles and labels
fig.legend(handles_list, labels_list, loc='upper center', bbox_to_anchor=(0.5, 0), ncol=4, fontsize=font_leg)
plt.tight_layout()
# Adjust the layout
#plt.suptitle('MACD Estimated Dates', fontsize=16)
#plt.savefig(f'{save_dir}macd_res.png', bbox_inches='tight')
#plt.savefig(f'{save_dir}macd_4x1_res.png', bbox_inches='tight')
plt.show()
