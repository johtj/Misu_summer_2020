#!/usr/bin/env python3
import os
import datetime as dt

#input data will be read from settings.json as follows

start_date = "2018-03-29 00:00:00"
end_date = "2018-03-30 00:00:00"
site = "Sodankyla"
model_types = ["ifs","slav"]
path_to_db = "/home/jojo161/MISU/job_summer_2020/Data"
forcast_time = "00"

################### function start #####################################
#first initialization of needed variables and two empty lists for the results
start_date = dt.datetime.strptime(start_date,'%Y-%m-%d %H:%M:%S')
end_date = dt.datetime.strptime(end_date,'%Y-%m-%d %H:%M:%S')
obs_file_names = []
obs_file_types = ["smthn_obs","smthn_sond","smthn_cloud"]
model_file_names = []

#First handle obs files, the names will be constant for the three types,
#control of which paths that are created i.e if all or only specified files
#are seleced tbd.
for type_name in obs_file_types:
    #probably adding some form of if to filter which pathnames are made.
    obs_file_names.append(path_to_db + "/"+site+"/obs/"+type_name)


for model_type in model_types:
    #creat path to relevant directory for the site and model type specified
    dir_path = path_to_db + "/"+ site+"/"+model_type+"/"+forcast_time

    #create a list of the files sorted by the date included in 
    # their name in ascendig order
    file_lst = sorted(os.listdir(dir_path))

    index = []
    for fname in file_lst:
        time = fname.split("_")[-1].split(".")[0]
        dt_time = dt.datetime.strptime(time,'%Y%m%d%H')
        if dt_time == start_date or dt_time == end_date:
            index.append(file_lst.index(fname))
    
    model_file_names.append(file_lst[index[0]:index[1]+1])

#return model_file_names, obs_filenames


