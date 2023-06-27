#!/usr/bin/env python
# coding: utf-8

# In[181]:


import os
import xarray as xr
import numpy as np


# In[178]:


#Input path (non-interpolated files)
input_path =  '/opt/AQ/UseCase/Cheverly/Data/Input/Satellite/Merra-2' 


# In[182]:


#Input path (inteprolated files)
input_path = '/opt/AQ/UseCase/Cheverly/Data/Output/Merra-2'


# In[183]:


#Aquire names for the input files
file_list = [filename for filename in os.listdir(input_path) if filename.endswith('.nc')]


# In[184]:


#Read one NetCDF file to determine the structure (ideally run every time, however it may not be necessary)
example_file = file_list[0]
example_file_path = os.path.join(input_path, example_file)
ds_sample = xr.open_dataset(example_file_path, engine='netcdf4')

#Get the variable names and their shapes from the sample file
variables = list(ds_sample.variables)
variable_shapes = {var: ds_sample[var].shape for var in variables}

#Print the variables and their shapes in the sample file
for var in variables:
    shape = variable_shapes[var]
    print(f"{var}: {shape}")


# In[ ]:




