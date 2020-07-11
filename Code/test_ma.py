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

# ta_var = datasets[0]["ta"]
# dimensions = ta_var.dimensions
# if "lat" in dimensions or "lon" in dimensions:
#     columns = [0,2,1]
#     print(np.shape(ta_var))
#     ta_var = np.transpose(ta_var, (0, 3, 1, 2))
#     print(np.shape(ta_var))

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
        


listsss = single_file(datasets,"2018-08-14 00:15:00","2018-08-14 01:00:00",variables)


# thing = listsss[0]
# print(thing["ta"][:,0,0,0:10])
#######################################################
# def get_data(variables, file_name,start_time, end_time,height_high, height_low):
#     #try:
#     ds = nc.Dataset(file_name)
#     data = {}
#     timespan, index = get_time_span(ds,start_time,end_time)
#     data["time"] = timespan
#     level , half_level = get_levels(ds,height_high,height_low,index)
#     print(level,half_level)
#     for variable in variables:
#         if variable not in data.keys():
#             ret_variable = retrieve_variable(variable,ds,index)
#             filtered = filter_by_height(ds[variable],level,half_level,ret_variable)
#             data[variable] = np.array(filtered)
#     return data
#     # except:
#     #      print("Data could not be retrieved, check format of input variables") #add, see readme for format details


