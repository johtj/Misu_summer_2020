#!/usr/bin/env python3
import netCDF4 as nc 
import cftime as cf
import numpy as np
import datetime as dt
from get_functions import *
#this file containes the functions responsible for getting 
#the variable data from the netCDF variables, as well as filtering it by time and height.

#####################################################################
#combines data  from the same variable in different files into into one single variable,
# based on a specific time specification. Does this for an input list of variables.
#it creates a new time array to fit the concatenated variables.
#Returns a dictionary with the variable names as keys and the concatenated variables as values.

def combine_files(data_sets,settings,target_lat_lon,file_names):
    combined_files = []

    sorted_data_sets = get_model_groups(data_sets,file_names,settings)
    
    count = 0
    for model in sorted_data_sets:
        #gets model name
        name = settings["model_types"][count]
        count = count +1
    
        data = {}
        data["name"] = name
        
        #calculates the index of the last time needed for time filtering purposes
        #also gives the time unit from the first dataset in the list
        index_end,unit = get_time(model[0],settings["time_wanted"])

        #takes the time data from all the datasets, 
        #converts them to use the same unit as used in the first file
        #thus creating one combined time variable
        total_time = []
        for ds in model:
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
        data["time_str"] = total_time
        data["time_units"] = unit

        #calculates indecies used for filtering by height
        try:
            level,half_level = get_levels(model[0],settings["height_high"],settings["height_low"])
        except IndexError:
            print("Index error in get_level: highest height lower than lowest height in model")
            
        index_lat , index_lon, single = get_lat_lon(model[0],target_lat_lon,settings)

        #goes though each variable in the list and creates a dictionary key for it,
        #assigning the value of the filtered concatinated variable
        for variable in settings["variables"]:
            total = []
            for dataset in model:
                var = dataset[variable]
                dim = var.dimensions
        
                value = np.array(var[0:index_end])

                #filters by latitude and longitide
                if "lat" in dim:
                    if single == True:
                        value = value[:,index_lat,index_lon]
                    else:
                        value = value[:,index_lat[0]:index_lat[1],index_lon[0]:index_lon[1]]
                    
            
                #rearanges arrays in the format (time,lat,lon,level) 
                #to the format of (time,level,lat,lon) to match
                #the format of variables in the format of (time,level) that do not contain lat & lon.
                #simplifies future filtering
                if ("lat" in dim and "lon" in dim) and np.shape(value) == 4:
                    value = np.transpose(value, (0, 3, 1, 2))

                

                #filters by half level or level if necessary
                if "half-level" in dim:
                    value = value[:,half_level[0]:half_level[1]]
                elif "level" in dim:
                    value = value[:,level[0]:level[1]]

                total.append(value)
            
            data[variable] = np.concatenate(total)
        
        combined_files.append(data)
    #the output is in the format of a list of dictionaries
    return combined_files

##########################################################################################
#filters variables from single files by time, returns a list of dictionaries.

def single_files(data_sets,settings,target_lat_lon):
    variable_sets = []

    #goes through datasets in the data_sets list and creates a dictionary 
    #with wanted variables filtered by height and time
    for ds in data_sets:

        #calculates the index of the last time needed for time filtering purposes
        end_index = get_time(ds,settings["time_wanted"])[0]
        
        #creates a dictionary to keep the data in 
        data = {}
        
        title = ds.title
        title = title[0:10]
       
        data["name"] = title

        #creates and adds the time units and an array of datetime objects to the dictionary
        time_in_ds = ds["time"]
        data["time_units"] = time_in_ds.units
        #.replace("minutes","hours")
        data["time_str"] = cf.num2date(time_in_ds[0:end_index],time_in_ds.units,calendar="standard")
       
        #gets level and half_level indecies for filtering purposes
        try:
            level, half_level = get_levels(ds,settings["height_high"],settings["height_low"])
        except IndexError:
            print("Index error in get_level: highest height lower than lowest height in model")
            break

        index_lat , index_lon, single = get_lat_lon(data_sets[0],target_lat_lon,settings)

        for variable in settings["variables"]:
            var = ds[variable]
            dim = var.dimensions
            
            value = np.array(ds[variable][0:end_index])

            #filters by latitude and longitide
            if "lat" in dim:
                if single == True:
                    value = value[:,index_lat,index_lon]
                else:
                    value = value[:,index_lat[0]:index_lat[1],index_lon[0]:index_lon[1]]
                    

            #rearanges arrays in the format (time,lat,lon,level) 
            #to the format of (time,level,lat,lon) to match
            #the format of variables in the format of (time,level) that do not contain lat & lon.
            #simplifies future filtering
            if ("lat" in dim and "lon" in dim) and np.shape(value) == 4:
                value = np.transpose(value, (0, 3, 1, 2))

            #filters by level and half level if necessary
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

def observation_files(obs_ds,start_time,end_time, height_high,height_low,hours):
    #first a list of desired variables is created
    variable_lst = [["tas_2m"]]

    #the timespan index is found so only data over a certain time period 
    #is retrieved
    time_var = obs_ds[0]["time"]
    t = np.array(time_var[:])

    stime_dt = dt.datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S')
    stime_num = cf.date2num(stime_dt,time_var.units,calendar="standard")

    etime_dt = dt.datetime.strptime(end_time,'%Y-%m-%d %H:%M:%S')
    etime_num = cf.date2num(etime_dt,time_var.units,calendar="standard")
    etime_num = etime_num+hours


    time_index = np.where(((t >= stime_num)&(t<=etime_num)))[0]
    tindex_lo = time_index[0]
    tindex_hi = time_index[-1]
    
    #variables for time units, and an array of datetime objects are created
    time_str = cf.num2date(t[tindex_lo:tindex_hi],time_var.units,calendar="standard")
    time_units = time_var.units

    variable_sets = []
    #the desired variables for each file are filtered and compiled into a dictionsry
    #which is then added to the variable sets list which is returned
    for obs in obs_ds:
        data = {}
        variables = variable_lst[obs_ds.index(obs)]
        
        #the above defined time units and array, as well as a now specified time step
        #variable are added to the dictionary
        data["time_str"] = time_str
        data["time_units"] = time_units.replace("minutes","hours")
        data["time_delta"] = time_var.delta_t

        for variable in variables:
            #specified variables are added to the dictionary filtered by time
            data[variable] = np.array(obs[variable][tindex_lo:tindex_hi])
        variable_sets.append(data)
    
    return variable_sets

