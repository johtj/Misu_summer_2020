#!/usr/bin/env python3
import netCDF4 as nc 
import cftime as cf
import numpy as np
import datetime as dt
#this file containes the functions responsible for getting 
#the variable data from the netCDF variables, as well as filtering it by time

#####################################################################
#takes a list of filenames and returnes a list of datasets 
# from which variable data can be retrived.
def get_dataset(file_names):
    data_sets = []
    for fn in file_names:
        data_sets.append(nc.Dataset(fn))
    return data_sets

#####################################################################
#combines data  from the same variable in different files into into one single variable,
# based on a specific time specification. Does this for an input list of variables.
#it creates a new time array to fit the concatenated variables.
#Returns a dictionary with the variable names as keys and the concatenated variables as values.

def combine_files(data_sets,variables,time_needed):
    data = {}
    #takes the time variable and specifed first timevalue from the first file for reference
    start_time_var = data_sets[0]["time"]
    start_time = start_time_var[0]

    #finds index of the start time
    start_time_str = cf.num2date(start_time,start_time_var.units,calendar="standard")
    index_start = nc.date2index(start_time_str,start_time_var,calendar="standard")

    #calculates the end time by adding the hours passed from the first time to the last
    end_time = start_time + time_needed

    #calculates the index of the endtime
    end_time_str = cf.num2date(end_time,start_time_var.units,calendar="standard")
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
    final_time = cf.date2num(total_time,start_time_var.units,calendar="standard")

    #adds time as key in data dictionary with final_time as its value
    data["time"] = final_time

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

            total.append(value)
        data[variable] = np.concatenate(total)
    return data

##########################################################################################
#filters variables from single files by time, returns a list of dictionaries.

def single_file(data_sets,start_time,end_time,variables):
    variable_sets = []
    for ds in data_sets:
        data = {}
        time_var = ds["time"]
        if start_time == end_time:
            start_time = dt.datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S')
            index = nc.date2index(start_time,time_var,calendar="standard")
        else:
            start_time = dt.datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S')
            index_start = nc.date2index(start_time,time_var,calendar="standard")

            end_time = dt.datetime.strptime(end_time,'%Y-%m-%d %H:%M:%S')
            index_end = nc.date2index(end_time,time_var,calendar="standard")

            index = (index_start,index_end)

        for variable in variables:
            var = ds[variable]
            dim = var.dimensions
            
            if len(index) == 1:
                value = np.array(ds[variable][index])
            else:
                value = np.array(ds[variable][index[0]:index[1]])

            if ("lat" in dim and "lon" in dim) and len(dim) == 4:
                value = np.transpose(value, (0, 3, 1, 2))
                
            data[variable] = value
        variable_sets.append(data)
    return variable_sets

##################################################################################
def get_levels(data_set,height_high,height_low,index_time):
    goph_level = np.array(data_set.variables["zg"][0,:])
    goph_half_level = np.array(data_set.variables["zghalf"][0,:])

    orog = int(data_set.variables["orog"][0])

    goph_level_new = goph_level - orog
    goph_half_level_new = goph_half_level -orog
    
    indecies_level = np.where((goph_level_new >= int(height_low))&(goph_level_new <= height_high))
    indecies_half_level = np.where((goph_half_level_new >= int(height_low))&(goph_half_level_new <= height_high))
   
    level , half_level = (indecies_level[0][0],indecies_level[0][-1]), (indecies_half_level[0][0],indecies_half_level[0][-1])
    return level,half_level    