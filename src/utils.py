import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import geopy.distance


# for all df
def get_row_with_str(df, name_str):
    res = df[df.apply(lambda row: row.astype(str).str.contains(name_str).any(), axis=1)]
    return res

# specifically for ligne 2019
def scatter_plot(df, colors, X_name, Y_name):

    # Create the plot
    plt.figure(figsize=(12, 8))

    for voltage_level in df['Voltage level (kV)'].unique():
        
        # subset is over different voltage  and exclude short lines
        subset_0 = df[(df['Voltage level (kV)'] == voltage_level)]
        subset = subset_0[subset_0['Length (m)'] > subset_0['Length (m)'].quantile(0.05)]
        
        plt.scatter(subset[X_name], subset[Y_name], 
                    color=colors[str(voltage_level)], 
                    label=f'Voltage Level: {voltage_level}', 
                    s=50, alpha=0.7)

    # Customize the plot
    plt.title(f'{X_name} vs {Y_name}', fontsize=16)
    plt.xlabel(X_name, fontsize=12)
    plt.ylabel(Y_name, fontsize=12)
    plt.xticks(rotation=90, ha='right')

    # Add legend without a color bar
    plt.legend(title='Voltage Levels')
    plt.tight_layout()

    # Display the plot
    plt.show()
    
def hist_plot_1(df, list_col):
    col_name = list_col[0]
    col_name_title = list_col[1]
    # Create the plot
    for voltage_level in df['Voltage level (kV)'].unique():
    
        # subset is over different voltage  and exclude short lines
        subset_0 = df[(df['Voltage level (kV)'] == voltage_level)].copy()
        subset = subset_0[subset_0['Length (m)'] > subset_0['Length (m)'].quantile(0.05)].copy()
        subset.reset_index(drop=True, inplace=True)
        subset[col_name_title] = subset[col_name] / subset['Length (m)'] * 1000
        
        plt.figure(figsize=(12, 8))
        ax = sns.histplot(data = subset, x = col_name_title, kde = True, bins=200)
        
        # Get the histogram data
        hist_data = ax.patches
        
        # Find the bin with the highest count
        max_count_patch = max(hist_data, key=lambda p: p.get_height())
        max_count = max_count_patch.get_height()
        max_count_bin = max_count_patch.get_x() + max_count_patch.get_width() / 2

        # Add a vertical line at the most frequent value
        plt.axvline(max_count_bin, color='red', linestyle='dashed', linewidth=2)
        
        # Add text annotation
        plt.text(max_count_bin, max_count, f'Most frequent: {max_count_bin:.3f}', 
            horizontalalignment='right', verticalalignment='bottom')

        # Customize the plot
        plt.title(f'Histplot {col_name} / length for voltage {voltage_level} kV', fontsize=16)
        plt.xlabel(col_name_title, fontsize=12)
        plt.ylabel('Occurence', fontsize=12)
        plt.xticks(rotation=30, ha='right')
        plt.tight_layout()

        # Display the plot
        plt.show()
        
def hist_plot_2(df, Y_name):
    
    for voltage_level in df['Voltage level (kV)'].unique():
        
        # subset is over different voltage  and exclude short lines
        subset_0 = df[(df['Voltage level (kV)'] == voltage_level)].copy()
        subset = subset_0[subset_0['Length (m)'] > subset_0['Length (m)'].quantile(0.05)].copy()
        subset.reset_index(drop=True, inplace=True)

        
        plt.figure(figsize=(12, 8))
        ax = sns.histplot(data = subset, x = Y_name, kde = True, bins=100)
        
        # Get the histogram data
        hist_data = ax.patches
        
        # Find the bin with the highest count
        max_count_patch = max(hist_data, key=lambda p: p.get_height())
        max_count = max_count_patch.get_height()
        max_count_bin = max_count_patch.get_x() + max_count_patch.get_width() / 2

        # Add a vertical line at the most frequent value
        plt.axvline(max_count_bin, color='red', linestyle='dashed', linewidth=2)
        
        # Add text annotation
        plt.text(max_count_bin, max_count, f'Most frequent: {max_count_bin:.3f}', 
            horizontalalignment='right', verticalalignment='bottom')

        # Customize the plot
        plt.title(f'Histplot {Y_name} for voltage {voltage_level} kV', fontsize=16)
        plt.xlabel(Y_name, fontsize=12)
        plt.ylabel('Occurence', fontsize=12)
        plt.xticks(rotation=30, ha='right')
        plt.tight_layout()

        # Display the plot
        plt.show()
        
        
# Specificaly for data/lignes-aeriennes-rte-nv.csv

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth's surface.
    Inputs are in decimal degrees.
    """
    R = 6371e3  # Radius of Earth in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # Distance in meters


def length_from_coordinate(longitudes, latitudes):
    
    total_length = 0

    for i in range(len(longitudes) - 1):
        coords_1 = (latitudes[i],longitudes[i])
        coords_2 = (latitudes[i+1],longitudes[i+1])
        total_length += geopy.distance.geodesic(coords_1, coords_2).m
        
    return total_length
        