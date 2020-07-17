#!/usr/bin/env python3
import netCDF4 as nc 
import cftime as cf
import numpy as np
import datetime as dt
import os
#this file containes the functions responsible for getting 
#the variable data from the netCDF variables, as well as filtering it by time and height.

#####################################################################
#combines data  from the same variable in different files into into one single variable,
# based on a specific time specification. Does this for an input list of variables.
#it creates a new time array to fit the concatenated variables.
#Returns a dictionary with the variable names as keys and the concatenated variables as values.

def combine_files(data_sets,start_time,time_wanted,variables,height_high,height_low):
    data = {}

    #calculates the index of the last time needed for time filtering purposes
    #also gives the time unit from the first dataset in the list
    index_end,unit = get_time(data_sets,start_time,time_wanted)

    #takes the time data from all the datasets, 
    #converts them to use the same unit as used in the first file
    #thus creating one combined time variable
    total_time = []
    for ds in data_sets:
        time_ds = ds["time"]
        time_num = time_ds[0:index_end]

        #converts the time number to datetime aray, 
        #objects are in the form year-month-day hr:min:sec
        time_str = cf.num2date(time_num,time_ds.units,calendar="standard")
        total_time.append(time_str)

    #makes array of all datetimes 
    total_time = np.concatenate(total_time)

    #adds this new time variable into the dictionary as datetime objects
    #as well as its units.
    data["time_total"] = total_time
    data["time_units"] = unit

    #calculates indecies used for filtering by height
    level,half_level = get_levels(data_sets[0],height_high,height_low)
   
    #goes though each variable in the list and creates a dictionary key for it,
    #assigning the value of the filtered concatinated variable
    for variable in variables:
        total = []
        for dataset in data_sets:
            var = dataset[variable]
            dim = var.dimensions
            value = np.array(var[0:index_end])
            
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

def single_files(data_sets,start_time_str,time_wanted,variables, height_high,height_low):
    variable_sets = []

    end_index,unit = get_time(data_sets,start_time_str,time_wanted)

    #goes through datasets in the data_sets list and creates a dictionary 
    #with wanted variables filtered by height and time
    for ds in data_sets:
        data = {}
        time_in_ds = ds["time"]
        data["time_units"] = time_in_ds.units
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
#handles the reading of data from the observational files into a list of three dictionaries
#one for observational, one for sonde and one for cloud

def observation_files(obs_ds,start_time,end_time, height_high,height_low):
    #first a list of desired variables is created
    variable_lst = [["tas_2m"]]

    #then the timespan index is found so only data over a certain time period 
    #is retrieved
    time_var = obs_ds[0]["time"]
    t = np.array(time_var[:])

    stime_dt = dt.datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S')
    stime_num = cf.date2num(stime_dt,time_var.units,calendar="standard")

    etime_dt = dt.datetime.strptime(end_time,'%Y-%m-%d %H:%M:%S')
    etime_num = cf.date2num(etime_dt,time_var.units,calendar="standard")

    time_index = np.where(((t >= stime_num)&(t<=etime_num)))[0]
    tindex_lo = time_index[0]
    tindex_hi = time_index[-1]
    print("ind: ",tindex_lo,tindex_hi)
    time_str = cf.num2date(t[tindex_lo:tindex_hi],time_var.units,calendar="standard")
    time_units = time_var.units

    variable_sets = []
    #the desired variables for each file are filtered and compiled into a dictionsry
    #which is then added to the variable sets list which is returned
    for obs in obs_ds:
        data = {}
        variables = variable_lst[obs_ds.index(obs)]
        data["time_str"] = time_str
        data["time_units"] = time_units

        for variable in variables:
            data[variable] = obs[variable][tindex_lo:tindex_hi]
        variable_sets.append(data)
    
    return variable_sets

##################################################################################
#handles the retreival of indecies for filtering by height
#both using level and half level

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

#######################################################################################
#handles the retreival of an end time index for filtering by time

def get_time(data_sets,start_time_str,time_wanted):
    time_wanted_min = time_wanted*60
    print(type(data_sets))
    time_var = data_sets[0]["time"]
    time_data = time_var[:]

    start_time_dt = dt.datetime.strptime(start_time_str,'%Y-%m-%d %H:%M:%S')
    start_time_num = cf.date2num(start_time_dt,time_var.units,calendar="standard")

    end_time_num = start_time_num + time_wanted
    end_lst = np.where((time_data<=end_time_num))[-1]
    end_index = end_lst[-1]

    unit = time_var.units

    return end_index,unit