import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import geopy.distance
import plotly.graph_objects as go
import numpy as np
import json


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
        

# Specificaly for substation dataset

def show_map_substation_gradient(df, name_column_value,fig_title, bar_title, name_column_text ='text', scale_reverse = False ):
    val_max = df[name_column_value].max()
    print(val_max)
    fig = go.Figure(data=go.Scattergeo(
            locationmode = 'country names',
            lon = df['lon'],
            lat = df['lat'],
            text = df[name_column_text],
            mode = 'markers',
            marker = dict(
                size = 6,
                opacity = .95,
                reversescale = scale_reverse,
                autocolorscale = False,
                symbol = 'square',
                line = dict(
                    width=1,
                    color='rgba(102, 102, 102)'
                ),
                colorscale = [
                    [0,  'limegreen'],
                    [1-50/val_max,  'gold'],
                    [1, 'crimson']
                ],
                cmin = 0,
                color = df[name_column_value],
                cmax = val_max,
                colorbar=dict(
                    title=dict(
                        text=bar_title
                    )
                )
            )))
    fig.update_geos(fitbounds="locations")

    fig.update_layout(
            title = fig_title,
            width=800,  # Increased width
            height=800,  # Increased height
            autosize = False, 
            margin={"r":0,"t":100,"l":0,"b":0},
            geo = dict(
                scope='europe',
                resolution = 50,
                projection_type='mercator',
                showland = True,
                landcolor = "rgb(173, 217, 240)",
                subunitcolor = "rgb(28, 12, 13)",
                countrycolor = "rgb(28, 12, 13)",
                countrywidth = .25,
                subunitwidth = .25), 
            coloraxis_colorbar=dict(
                x=.1,  # Move colorbar slightly to the right
                y=0.5,  # Center the colorbar vertically
                len=0.75,  # Adjust length of colorbar
                thickness=20,  # Increase thickness
                title=dict(
                    text=name_column_value,
                    side="right"
                ),
                yanchor="middle"
            )
        )

    fig.show()
    
## look into capareseau and return :

def get_closest_post(df,my_GeopointPoste, n_voisins):
    dist = []
    indexes_to_drop = []
    for index, row in df.iterrows():
        longitudes = []
        latitudes = []
        
        lon_poste = row['lon']
        lat_poste = row['lat']
        if pd.isna(lon_poste) or pd.isna(lat_poste):
            indexes_to_drop.append(index)
        else :
            longitudes.append(lon_poste)
            latitudes.append(lat_poste)
            longitudes.append(my_GeopointPoste[1])
            latitudes.append(my_GeopointPoste[0])
            dist.append(length_from_coordinate(latitudes,longitudes)/1000)
    df_res = df.copy()
    df_res.drop(indexes_to_drop, inplace =True)
    df_res['dist_to_my_poste_km'] = dist
    
    df_voisins = df_res.sort_values(by='dist_to_my_poste_km', ascending=True)
    
    return df_voisins.iloc[:n_voisins]
        
        
# Specificaly for data/lignes-aeriennes-rte-nv.csv

def length_from_coordinate(longitudes, latitudes):
    
    total_length = 0

    for i in range(len(longitudes) - 1):
        coords_1 = (latitudes[i],longitudes[i])
        coords_2 = (latitudes[i+1],longitudes[i+1])
        total_length += geopy.distance.geodesic(coords_1, coords_2).m
        
    return total_length
        
        
            
            
# Visualize lines

def show_map_lines(df : pd.DataFrame, light_version : bool):
    
    # Create an empty figure
    fig = go.Figure()

    # Param
    colors_tension = {'400kV' : 'red', '225kV' : 'green',
                    '150kV' : 'blue', '90kV' : 'orange',
                    '63kV' : 'magenta', '45kV' : 'yellow',
                    '<45kV' : 'purple', 'HORS TENSION' : 'black'}
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Parse the JSON string in the 'Geo Shape' column
        try:
            geo_data = json.loads(row['Geo Shape'])
        except json.JSONDecodeError:
            print(f"Error parsing JSON for row {index}. Skipping this row.")
            continue
        line_tension = row['TENSION']

        # Extract coordinates
        if "coordinates" in geo_data and isinstance(geo_data["coordinates"], list):
            longitudes, latitudes = zip(*geo_data["coordinates"])
            
            if light_version:
                longitudes = [longitudes[0], longitudes[-1]]
                latitudes = [latitudes[0], latitudes[-1]]

            # Add a trace for this line
            fig.add_trace(go.Scattermap(
                mode = "lines",
                lon = longitudes,
                lat = latitudes,
                name = f"Line {index}",  # You can replace this with a more meaningful name if available
                line = dict(width = 2),
                marker_color = colors_tension[line_tension]
            ))
        else:
            print(f"No valid coordinates found for row {index}. Skipping this row.")

    # Update the layout
    fig.update_layout(
        geo=dict(
            scope='europe',  # You can change this to a specific country or region
            projection_type='natural earth',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            countrycolor='rgb(204, 204, 204)',
            coastlinecolor='rgb(204, 204, 204)',
            showocean=True,
            oceancolor='rgb(230, 230, 250)',
            center=dict(
                lon=longitudes[0],  # Center on the first longitude
                lat=latitudes[0]    # Center on the first latitude
            ),
        ),
        showlegend=False,
        title='Some lines in France'
        )
    # Show the figure
    fig.show()


# Matrice adjacente 

def distance_matrix_geodesic(x):
    """Compute the distance matrix.

    Returns the matrix of all pair-wise distances.

    Parameters
    ----------
    x : (M, K) array_like
        Matrix of M vectors in 2 dimensions.


    Returns
    -------
    S : (M, M) ndarray
        Matrix containing the distance from every vector in `x` to each other

    """

    x = np.asarray(x)
    m, k = x.shape

    result = np.empty((m,m),dtype=float)
    for i in range(m):
        for j in range(i):
            result[i,j] = geopy.distance.geodesic(x[i],x[j]).m
 
    S = result + result.T
    
    return S