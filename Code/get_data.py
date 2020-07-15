#!/usr/bin/env python3
import netCDF4 as nc 
import cftime as cf
import numpy as np
import datetime as dt
import os
#this file containes the functions responsible for getting 
#the variable data from the netCDF variables, as well as filtering it by time as well as height.

#####################################################################
#combines data  from the same variable in different files into into one single variable,
# based on a specific time specification. Does this for an input list of variables.
#it creates a new time array to fit the concatenated variables.
#Returns a dictionary with the variable names as keys and the concatenated variables as values.

def combine_files(data_sets,variables,height_high,height_low):
    data = {}
    #takes the time variable and specifed first timevalue from the first file for reference
    start_time_var = data_sets[0]["time"]
    start_time = start_time_var[0]
    time_needed = 24#1380

    #as the start time is defined as the first time
    # the index of the start time will always be zero
    index_start = 0
    
    #calculates the end time by adding the hours passed from the first time to the last
    end_time = start_time + time_needed

    #calculates the index of the endtime
    end_time_str = cf.num2date(end_time,start_time_var.units,calendar="standard")
    print(start_time,cf.num2date(start_time,start_time_var.units,calendar="standard"))
    print(end_time,end_time_str)
    index_end = nc.date2index(end_time_str,start_time_var,calendar="standard")

    #takes the time data from all the datasets, 
    #converts them to use the same unit as used in the first file
    total_time = []
    for ds in data_sets:
        time_ds = ds["time"]
        time_num = time_ds[index_start:index_end]
        #converts the time number to datetime array, 
        #objects are in the form year-month-day hr:min:sec
        time_str = cf.num2date(time_num,time_ds.units,calendar="standard")
        total_time.append(time_str)

    #makes array of all datetimes 
    total_time = np.concatenate(total_time)

    #creates array of datestimes in number form using the units from the first file
    #final_time = cf.date2num(total_time,start_time_var.units,calendar="standard")

    #adds time as key in data dictionary with final_time as its value
    #data["time"] = final_time
    
    data["time_total"] = total_time
    data["time_units"] = start_time_var.units

    level,half_level = get_levels(data_sets[0],height_high,height_low)
   
    #goes though each variable in the list and creates a dictionary key for it,
    #assigning the value of the 
    for variable in variables:
        total = []
        for dataset in data_sets:
            var = dataset[variable]
            dim = var.dimensions
            value = np.array(var[index_start:index_end])
            
            if ("lat" in dim and "lon" in dim) and len(dim) == 4:
                value = np.transpose(value, (0, 3, 1, 2))


            if "half-level" in dim:
                value = value[:,half_level[0]:half_level[1]]
            elif "level" in dim:
                value = value[:,level[0]:level[1]]

            total.append(value)
        
        data[variable] = np.concatenate(total)
    return data

##########################################################################################
#filters variables from single files by time, returns a list of dictionaries.

def single_file(data_sets,start_time_str,time_wanted,variables, height_high,height_low):
    variable_sets = []

    time_var = data_sets[0]["time"]
    time_data = time_var[:]

    start_time_dt = dt.datetime.strptime(start_time_str,'%Y-%m-%d %H:%M:%S')
    start_time_num = cf.date2num(start_time_dt,time_var.units,calendar="standard")

    end_time_num = start_time_num + time_wanted
    end_lst = np.where((time_data<=end_time_num))[-1]
    end_index = end_lst[-1]

    for ds in data_sets:
        data = {}
        time_in_ds = ds["time"]
        data["time_units"] = time_in_ds.units
        data["time"] = time_in_ds[0:end_index]
        data["time_str"] = cf.num2date(time_in_ds[0:end_index],time_in_ds.units,calendar="standard")

        level, half_level = get_levels(ds,height_high,height_low)

        for variable in variables:
            var = ds[variable]
            dim = var.dimensions
            
            value = np.array(ds[variable][0:end_index])

            if ("lat" in dim and "lon" in dim) and len(dim) == 4:
                value = np.transpose(value, (0, 3, 1, 2))

            if "half-level" in dim:
                value = value[:,half_level[0]:half_level[1]]
            elif "level" in dim:
                value = value[:,level[0]:level[1]]  

            data[variable] = value
        variable_sets.append(data)
    return variable_sets

##################################################################################
def get_levels(data_set,height_high,height_low):
    level_var = data_set.variables["zg"]
    half_level_var = data_set.variables["zghalf"]

    dims = level_var.dimensions
    if "lat" in dims:
        goph_level = np.array(level_var[0,0,0,:])
        goph_half_level = np.array(half_level_var[0,0,0,:])
        orog = float(data_set.variables["Orog"][0,0,0])
    else:
        goph_level = np.array(level_var[0,:])
        goph_half_level = np.array(half_level_var[0,:])
        orog = float(data_set.variables["orog"][0])


    goph_level_new = goph_level - orog
    goph_half_level_new = goph_half_level -orog


    indecies_level = np.where((goph_level_new >= int(height_low))&(goph_level_new <= height_high))
    indecies_half_level = np.where((goph_half_level_new >= int(height_low))&(goph_half_level_new <= height_high))
    
    level , half_level = (indecies_level[0][0],indecies_level[0][-1]), (indecies_half_level[0][0],indecies_half_level[0][-1])
    
    return level,half_level    