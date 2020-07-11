#!/usr/bin/env python3
import netCDF4 as nc
import numpy as np
import numpy.ma as npm
import cftime as cf
import datetime as dt

#get data handles the retrieval of data taking list of str variable names and a str file_name,
#opens netCDF file with specified filename,
#returns a dict with variable names as keys containing the data'

def get_data(variables, file_name,start_time, end_time,height_high, height_low):
    #try:
    ds = nc.Dataset(file_name)
    data = {}
    timespan, index = get_time_span(ds,start_time,end_time)
    data["time"] = timespan
    level , half_level = get_levels(ds,height_high,height_low,index)
    print(level,half_level)
    for variable in variables:
        if variable not in data.keys():
            ret_variable = retrieve_variable(variable,ds,index)
            filtered = filter_by_height(ds[variable],level,half_level,ret_variable)
            data[variable] = np.array(filtered)
    return data
    # except:
    #      print("Data could not be retrieved, check format of input variables") #add, see readme for format details
        
# retrieves data from netCDF variables basded on 
def retrieve_variable(variable_name, data_set,index):
    if len(index) == 1:
        variable = data_set[variable_name][index]
    else:
        variable = data_set[variable_name][index[0]:index[1]]
    return variable

#takes str input time values on the format Y-M-D H:M:S and returnes timespan from 
#defined netCDF file's time data
#returnes this time span in number values, not dates
def get_time_span(data_set,start_time, end_time):
    time = data_set.variables["time"]
    time_num = time[:]
    if start_time == end_time or end_time == "":
        start_time = dt.datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S')
        index = nc.date2index(start_time,time,calendar="standard")
        time_span = time_num[index]
        
    else:
        print(start_time)
        start_time = dt.datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S')
        end_time = dt.datetime.strptime(end_time,'%Y-%m-%d %H:%M:%S')
        index_start = nc.date2index(start_time,time,calendar="standard")
        index_end = nc.date2index(end_time,time,calendar="standard")
        time_span = time_num[index_start:index_end]
        index = (index_start,index_end)
    return time_span, index

def filter_by_height(header, level_val, half_level_val,variable):
    dims = header.get_dims()
    names = []
    for i in range(len(dims)):
        names.append(dims[i].name)
    
    if "half_level" in names:
        if len(half_level_val) == 1:
            variable = variable[:, half_level_val]
        else: 
            variable = variable[:, half_level_val[0]:half_level_val[1]]
            
    elif "level" in names:
        if len(level_val) == 1:
            variable = variable[:,level_val]
        else:
            variable = variable[:,level_val[0]:level_val[1]]

    else:
        variable = variable

    return variable


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




        






