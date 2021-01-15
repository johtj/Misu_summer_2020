#!/usr/bin/env python3
import netCDF4 as nc 
import cftime as cf
import numpy as np
import datetime as dt
import os
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

def get_time(data_set,time_wanted):
    #creates the time variable 
    time_var = data_set["time"]
    time_data = time_var[:]

    #adapts the time_wanted variable (which is in hours)
    #to the model units if they are in minutes
    
    if "minutes" in time_var.units:
        time_wanted = time_wanted*60

    #makes the start time string into a number using the time units from the 
    #time variable created above
    start_time_num = time_data[0]

    #calculates an end time by adding the time_wanted to the start time number
    end_time_num = start_time_num + time_wanted
    

    #finds the index of where this time occurs in the time array
    end_lst = np.where((time_data<=end_time_num))[-1]
    
    end_index = end_lst[-2]


    unit = time_var.units.replace("minutes","hours").replace("0.0","00")

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

def get_model_groups(model_ds, file_names, settings):
    model_types = settings["model_types"]
    model_ds_sorted = []
    for mt in model_types:
        result = []
        for name in file_names:
            if mt in name:
                result.append(model_ds[file_names.index(name)])
        model_ds_sorted.append(result)

    return model_ds_sorted
