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

def combine_files(data_sets,settings,target_lat_lon):
    data = {}

    #calculates the index of the last time needed for time filtering purposes
    #also gives the time unit from the first dataset in the list
    index_end,unit = get_time(data_sets[0],settings["start_date"],settings["time_wanted"])

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
    data["time_str"] = total_time
    data["time_units"] = unit

    #calculates indecies used for filtering by height
    try:
        level,half_level = get_levels(data_sets[0],settings["height_high"],settings["height_low"])
    except IndexError:
        print("Index error in get_level: highest height lower than lowest height in model")
           
    index_lat , index_lon, single = get_lat_lon(data_sets[0],target_lat_lon,settings)

    #goes though each variable in the list and creates a dictionary key for it,
    #assigning the value of the filtered concatinated variable
    for variable in settings["variables"]:
        total = []
        for dataset in data_sets:
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
    #the output needs to be a list due to the fact that the output of
    #single_files() is a list and the two need to utilize the same functions
    datalst = [data]
    return datalst

##########################################################################################
#filters variables from single files by time, returns a list of dictionaries.

def single_files(data_sets,settings,target_lat_lon):
    variable_sets = []

    #calculates the index of the last time needed for time filtering purposes
    end_index = get_time(data_sets[0],settings["start_date"],settings["time_wanted"])[0]

    #goes through datasets in the data_sets list and creates a dictionary 
    #with wanted variables filtered by height and time
    for ds in data_sets:

        #creates a dictionary to keep the data in 
        data = {}

        #creates and adds the time units and an array of datetime objects to the dictionary
        time_in_ds = ds["time"]
        data["time_units"] = time_in_ds.units
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

def observation_files(obs_ds,start_time,end_time, height_high,height_low):
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
        data["time_units"] = time_units
        data["time_delta"] = time_var.delta_t

        for variable in variables:
            #specified variables are added to the dictionary filtered by time
            data[variable] = np.array(obs[variable][tindex_lo:tindex_hi])
        variable_sets.append(data)
    
    return variable_sets

##################################################################################
#handles the retreival of indecies for filtering by height
#both using level and half level

def get_levels(data_set,height_high,height_low):

    #retrievs the geopotential height on levels and half levels
    level_var = data_set.variables["zg"]
    half_level_var = data_set.variables["zghalf"]

    #retrieves the surface altitude in the apropriate way depending upon the 
    #exsitance of lat and lon in the variable.
    dims = level_var.dimensions
    if "lat" in dims:
        goph_level = np.array(level_var[0,0,0,:])
        goph_half_level = np.array(half_level_var[0,0,0,:])
        orog = float(data_set.variables["Orog"][0,0,0])
    else:
        goph_level = np.array(level_var[0,:])
        goph_half_level = np.array(half_level_var[0,:])
        orog = float(data_set.variables["orog"][0])

    #gets heights by subtracting the surface height from the geopotenital height
    goph_level_new = goph_level - orog
    goph_half_level_new = goph_half_level -orog

    #finds the indecies that lie within the height bounds specified in settings.json
    indecies_level = np.where((goph_level_new >= int(height_low))&(goph_level_new <= height_high))
    indecies_half_level = np.where((goph_half_level_new >= int(height_low))&(goph_half_level_new <= height_high))
    
    #takes the highest and lowest of these indecies and creates 
    #one tuple with the ranges for level and one for half level
    level , half_level = (indecies_level[0][0],indecies_level[0][-1]), (indecies_half_level[0][0],indecies_half_level[0][-1])
    
    return level,half_level    

#######################################################################################
#handles the retreival of an end time index for filtering by time

def get_time(data_set,start_time_str,time_wanted):
    #creates the time variable 
    time_var = data_set["time"]
    time_data = time_var[:]

    #adapts the time_wanted variable (which is in hours)
    #to the model units if they are in minutes
    if "minutes" in time_var.units:
        time_wanted = time_wanted*60

    #makes the start time string into a number using the time units from the 
    #time variable created above
    start_time_dt = dt.datetime.strptime(start_time_str,'%Y-%m-%d %H:%M:%S')
    start_time_num = cf.date2num(start_time_dt,time_var.units,calendar="standard")

    #calculates an end time by adding the time_wanted to the start time number
    end_time_num = start_time_num + time_wanted

    #finds the index of where this time occurs in the time array
    end_lst = np.where((time_data<=end_time_num))[-1]
    end_index = end_lst[-1]

    unit = time_var.units

    #returns this index as well as the time units used to calculate it
    return end_index,unit

############################################################################################
#this function handles the selection of latitude and longtude indecies for filtering 
#purposes

def get_lat_lon(data_set,target, settings):
    data_lat = np.array(data_set["lat"])
    data_lon = np.array(data_set["lon"])

    if len(data_lon) == 1 or len(data_lat) == 1:
        #if there is only one latitude and longitude in the dataset
        #that lat & lon are selected
        lat_ind = 0
        lon_ind = 0
        single = True
    else:
        #if there are multiple lat & lon points
        if settings["single_point"] == "True":
            #if single point set to True in settings.json the closest value to 
            #the lat & lon in the observational file is found and that index is recorded
            lat_ind = np.abs(data_lat-target[0]).argmin()
            lon_ind = np.abs(data_lon-target[1]).argmin()
            single = True
        else: 
            #if single point isn't set to True in settings.json the index ranges are
            #taken from settings.json
            lat_ind = (settings["lat_ind_lo"],settings["lat_ind_hi"])
            lon_ind = (settings["lon_ind_lo"],settings["lon_ind_hi"])
            single = False

    #in the first to cases the output will be integers representing the index of the value
    #in the last the output will be a tuple with the index range for the values wanted
    return lat_ind,lon_ind,single