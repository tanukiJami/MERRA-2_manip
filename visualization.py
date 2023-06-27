#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cf
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.colors as colors


# In[ ]:


#FOR VARIABLES WITH 3 DIMENSIONS

def base_map(bounds: dict = {}, padding: float = 0.5) -> plt.axes:
    '''
    Creates map with bounds and padding
    '''
    fig = plt.figure(figsize=(15, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())

    if bounds:
        bounds = (bounds['min_lon'] - padding,
                  bounds['max_lon'] + padding,
                  bounds['min_lat'] - padding,
                  bounds['max_lat'] + padding)
    else:
        bounds = (-180, 180, -90, 90)
    ax.set_extent(bounds, ccrs.PlateCarree())

    ax.add_feature(cf.LAND)
    ax.add_feature(cf.OCEAN)
    ax.coastlines('10m')
    ax.add_feature(cf.STATES, zorder=100)

    countries = cf.NaturalEarthFeature(
        category='cultural', name='admin_0_countries', scale='10m', facecolor='none')
    ax.add_feature(countries, zorder=100)

    gl = ax.gridlines(crs=ccrs.PlateCarree(), linewidth=1, color='black',
                      alpha=0.25, linestyle='--', draw_labels=True, zorder=90)
    gl.top_labels = False  # Use .top_labels instead of .xlabels_top
    gl.left_labels = True
    gl.right_labels = False
    gl.xlines = True
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    return ax


def map_data(data: xr.DataArray, title: str, lat: xr.DataArray, lon: xr.DataArray, cmap='jet', cb_label='', log_scale=False):
    '''
    Plots data on map
    '''

    bounds = {
        'min_lat': lat.min(),
        'max_lat': lat.max(),
        'min_lon': lon.min(),
        'max_lon': lon.max()
    }
    ax = base_map(bounds)
    if log_scale:
        mesh = ax.pcolormesh(lon, lat, data, norm=colors.LogNorm(), cmap=cmap, alpha=0.75)
    else:
        mesh = ax.pcolormesh(lon, lat, data, cmap=cmap, alpha=0.75)
    cb = plt.colorbar(mesh, shrink=0.6, location='bottom')
    cb.set_label(cb_label)
    plt.title(title)
    plt.show()

# Specify the directory where the netCDF files are located
#data_dir = '/opt/AQ/UseCase/Cheverly/Data/Input/Satellite/Merra-2'
data_dir = '/opt/AQ/UseCase/Cheverly/Data/Output/Merra-2'

# Get a list of netCDF files in the directory
file_list = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith('.nc')]

# Check if there are any netCDF files
if len(file_list) == 0:
    print("No netCDF files found in the specified directory.")
    exit()

# Read the first netCDF file in the list
file_path = file_list[0]
dataset = xr.open_dataset(file_path)

# Print the variables in the netCDF file
print("Variables in the netCDF file:")
for var in dataset.variables:
    print(var + ":", dataset[var].shape)

# Let the user choose the variable to plot
print("Choose a variable to plot:")
variable_name = input("Enter the name of the variable: ")

# Check if the chosen variable exists in the dataset
if variable_name not in dataset.variables:
    print("Variable not found in the dataset.")
    exit()

# Retrieve the variable data and dimensions
variable = dataset[variable_name]
time = variable['time']
lat = variable['lat']
lon = variable['lon']

# Plot the chosen variable for each timestamp
for i in range(len(time)):
    title = f"{variable_name} at timestamp {i+1}"
    map_data(variable[i], title, lat, lon)

# Close the netCDF dataset
dataset.close()


# In[ ]:


#FOR VARIABLES WITH 4 DIMENSIONS

def base_map(bounds: dict = {}, padding: float = 0.5) -> plt.axes:
    '''
    Creates map with bounds and padding
    '''
    fig = plt.figure(figsize=(15, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())

    if bounds:
        bounds = (bounds['min_lon'] - padding,
                  bounds['max_lon'] + padding,
                  bounds['min_lat'] - padding,
                  bounds['max_lat'] + padding)
    else:
        bounds = (-180, 180, -90, 90)
    ax.set_extent(bounds, ccrs.PlateCarree())

    ax.add_feature(cf.LAND)
    ax.add_feature(cf.OCEAN)
    ax.coastlines('10m')
    ax.add_feature(cf.STATES, zorder=100)

    countries = cf.NaturalEarthFeature(
        category='cultural', name='admin_0_countries', scale='10m', facecolor='none')
    ax.add_feature(countries, zorder=100)

    gl = ax.gridlines(crs=ccrs.PlateCarree(), linewidth=1, color='black',
                      alpha=0.25, linestyle='--', draw_labels=True, zorder=90)
    gl.top_labels = False  # Updated attribute
    gl.left_labels = True
    gl.right_labels = False
    gl.xlines = True
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    return ax

def map_data(data: xr.DataArray, title: str, lat: xr.DataArray, lon: xr.DataArray, cmap='jet', cb_label='', log_scale=False):
    '''
    Plots data on map
    '''
    bounds = {
        'min_lat': lat.min(),
        'max_lat': lat.max(),
        'min_lon': lon.min(),
        'max_lon': lon.max()
    }
    ax = base_map(bounds)

    if log_scale:
        mesh = ax.pcolormesh(lon.values, lat.values, data.squeeze(), norm=colors.LogNorm(), cmap=cmap, alpha=0.75)
    else:
        mesh = ax.pcolormesh(lon.values, lat.values, data.squeeze(), cmap=cmap, alpha=0.75)

    cb = plt.colorbar(mesh, shrink=0.6, location='bottom')
    cb.set_label(cb_label)

    plt.title(title)
    plt.show()

# Specify the directory path for netCDF files
directory = '/directory/to/interpolated/files'

# Get a list of netCDF files in the directory
file_list = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.nc')]

# Check if any netCDF files are found
if len(file_list) == 0:
    print("No netCDF files found in the specified directory.")
    exit()

# Read the first netCDF file in the list
file_path = file_list[0]
dataset = xr.open_dataset(file_path)

# Print the variables in the netCDF file
print("Variables in the netCDF file:")
for var in dataset.variables:
    print(var + ":", dataset[var].shape)

# Let the user choose the variable to plot
variable_name = input("Enter the variable name to plot: ")

# Check if the chosen variable exists in the dataset
if variable_name not in dataset.variables:
    print("Variable not found in the netCDF file.")
    exit()

# Get the variable data
variable = dataset[variable_name]
time = dataset['time']
lat = dataset['lat']
lon = dataset['lon']
elevation = dataset['lev']

# Plot the chosen variable for each timestamp and elevation
for i in range(len(time)):
    for j in range(len(elevation)):
        title = f"{variable_name} at timestamp {i+1}, elevation {j+1}"
        map_data(variable[i, j], title, lat, lon)

# Close the netCDF dataset
dataset.close()


# In[ ]:




