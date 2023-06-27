#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import xarray as xr
import numpy as np

input_path = "/opt/AQ/UseCase/Cheverly/Data/Input/Satellite/Merra-2"
output_directory = "/opt/AQ/UseCase/Cheverly/Data/Output/Merra-2"

file_list = [filename for filename in os.listdir(input_path) if filename.endswith('.nc') or filename.endswith('.nc4')]

interpolated_files = []  # Track interpolated files

# Prompt the user for the interpolation method
interpolation_method = input("Choose an interpolation method from the following options:\n"
                             "1. linear\n"
                             "2. nearest\n"
                             "3. cubic\n"
                             "4. quadratic\n"
                             "5. slinear\n"
                             "6. polynomial\n"
                             "Enter the number corresponding to the desired method: ")

# Map the user's choice to the corresponding interpolation method
interpolation_methods = {
    '1': 'linear',
    '2': 'nearest',
    '3': 'cubic',
    '4': 'quadratic',
    '5': 'slinear',
    '6': 'polynomial',
    '7': 'spline',
    '8': 'pchip',
    '9': 'akima',
    '10': 'cubicspline',
    '11': 'from_derivatives'
}

chosen_method = interpolation_methods.get(interpolation_method)
if chosen_method is None:
    print("Invalid interpolation method. Exiting...")
    exit(1)

# Create a directory for the chosen interpolation method within the output directory
output_method_directory = os.path.join(output_directory, chosen_method)
os.makedirs(output_method_directory, exist_ok=True)

for filename in file_list:
    file_path = os.path.join(input_path, filename)

    try:
        ds = xr.open_dataset(file_path, engine='h5netcdf')

        # Print latitude and longitude
        print(f"File: {filename}")
        print(f"lat size: {ds['lat'].size}")
        print(f"lon size: {ds['lon'].size}")

        # Check latitude and longitude sizes
        if ds['lat'].size == 1 or ds['lon'].size == 1:
            print(f"Skipping file {filename} due to invalid dimensions")
            continue  # Skip to the next file

        # Perform interpolation on latitude and longitude
        ds_interp = ds.interp(lat=np.arange(ds.lat.min(), ds.lat.max(), 0.1),
                             lon=np.arange(ds.lon.min(), ds.lon.max(), 0.1),
                             method=chosen_method)

        # Save interpolated variables to NetCDF file
        output_filename = f"interpolated_{filename}"
        output_path = os.path.join(output_method_directory, output_filename)

        # Check if the file has already been interpolated
        if output_filename in interpolated_files:
            existing_file_path = os.path.join(output_method_directory, output_filename)
            if os.path.exists(existing_file_path):
                os.remove(existing_file_path)
                print(f"Existing file {output_filename} removed")

        ds_interp.to_netcdf(output_path, format='NETCDF4', engine='h5netcdf')

        print(f"Interpolated variables saved to {output_path}")

        interpolated_files.append(output_filename)

    except Exception as e:
        print(f"Error occurred while processing {filename}: {e}")
        continue  # Skip to the next file if an error occurs
