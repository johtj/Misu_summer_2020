#!/usr/bin/env python3
import os
import datetime as dt
import netCDF4 as nc

#this file contains the function responsible for locating 
# and reading data from netCDF files from a local database
# it produces a list of datasets lists for each modeltype 
# and one for the observation data

def get_local_ds(start_date,end_date,path_to_db,site,model_types,forcast_time):

    #initialization of needed variables and two empty lists for the results
    start_date = dt.datetime.strptime(start_date,'%Y-%m-%d %H:%M:%S')
    end_date = dt.datetime.strptime(end_date,'%Y-%m-%d %H:%M:%S')
    obs_ds = []
    obs_file_types = ["smthn_obs","smthn_sond","smthn_cloud"]
    model_ds = []

    #First handle obs files, the names will be constant for the three types,
    #control of which paths that are created i.e if all or only specified files
    #are seleced will be added, as of now one hard coded option is available.

    #for type_name in obs_file_types:
       #probably adding some form of if to filter which pathnames are made.
        #obs_fname = path_to_db + "/"+site+"/obs/"+type_name
    obs_ds.append(nc.Dataset("/home/jojo161/MISU/job_summer_2020/Data/Barrow/obs/utqiagvik_obs_sop1.2jul2019.nc"))

    #then read in the apropriate model data files, this is done by providing a directory,
    #site , model type and forcast time, and timespan, the apropriate files are then 
    #retreieved from that directory and stored as datasets.

    for model_type in model_types:
        #creat path to relevant directory for the site and model type specified
        dir_path = path_to_db + "/"+ site+"/"+model_type+"/"+forcast_time

        #create a list of the files sorted by the date included in 
        # their name in ascendig order
        file_lst = sorted(os.listdir(dir_path))

        index = []
        #sort by time, find index of first and last file
        for fname in file_lst:
            time = fname.split("_")[-1].split(".")[0]
            dt_time = dt.datetime.strptime(time,'%Y%m%d%H')
            if dt_time == start_date or dt_time == end_date:
                index.append(file_lst.index(fname))

        #retreieve relevant files, add pathname to them and create datasets
        if len(index) == 1:
            files = file_lst[index[0]]
            files_path = [dir_path+"/"+files]
        else:
            files = file_lst[index[0]:index[1]+1]
            files_path = [dir_path+"/"+name for name in files]

        print("files",files)
        
        model_ds = [nc.Dataset(f_path) for f_path in files_path]

    #two lists of datasets are returned, one for model data one for observation data  
    print("len ds",len(model_ds)) 
    return model_ds, obs_ds


