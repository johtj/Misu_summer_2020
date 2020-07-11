#!/usr/bin/env python3
import netCDF4 as nc
import numpy as np
import numpy.ma as npm
import cftime as cf
import datetime as dt

#barrow_slav-rhmc_2018081400.nc
#barrow_slav-rhmc_2018081500.nc
#barrow_slav-rhmc_2018081600.nc

#start will be 2018 08 14 00:00:00 and end will be 2018 08 16 23:00:00
# take that timespan of each file

ds14 = nc.Dataset("/home/jojo161/MISU/job_summer_2020/Barrow_slav/barrow_slav-rhmc_2018081400.nc")
ds15 = nc.Dataset("/home/jojo161/MISU/job_summer_2020/Barrow_slav/barrow_slav-rhmc_2018081500.nc")
ds16 = nc.Dataset("/home/jojo161/MISU/job_summer_2020/Barrow_slav/barrow_slav-rhmc_2018081600.nc")
datasets = [ds14]
variables = ["ta","tas","ts"]

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

hi = combine_files(datasets,variables,60)

for key in hi.keys():
    print(np.shape(hi[key]))