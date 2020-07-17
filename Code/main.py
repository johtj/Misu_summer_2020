#!/usr/bin/env python3
#this is the main script for the reading and plotting of model and 
#observational data from netCDF files for the evaluation of model quality.

#functions used in this code are imported from the following files
from get_local_ds import *
from read_settings import *
from get_var_sets import *
from plot import *
from scatter import *


fn = "/home/jojo161/MISU/job_summer_2020/Code/settings.json"

settings_list = load_settings(fn)
for setting in settings_list:   
    if setting["local"] == "True":
        mod_ds, obs_ds = get_local_ds(setting["start_date"],setting["end_date"],setting["path_to_db"],setting["site"],setting["model_types"],setting["forcast_time"])
        filtered_obs_var = observation_files(obs_ds,setting["start_date"],setting["end_date"],setting["height_high"],setting["height_low"])
        filtered_mod_var = []
        if setting["single"] == "True":
            filtered_mod_var = single_files(mod_ds,setting["start_date"],setting["time_wanted"],setting["variables"],setting["height_high"],setting["height_low"])
        else:
            filtered_mod_var = combine_files(mod_ds,setting["variables"],setting["start_date"],setting["time_wanted"],setting["height_high"],setting["height_low"])
        
    #plot(filtered_mod_var,filtered_obs_var[0],setting)
    scatter_plot(filtered_mod_var,filtered_obs_var,setting)

