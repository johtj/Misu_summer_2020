#!/usr/bin/env python3
#this is the main script for the reading and plotting of model and 
#observational data from netCDF files for the evaluation of model quality.

#functions used in this code are imported from the following files
from get_local_ds import *
from read_settings import *
from get_var_sets import *
from plot import *
from scatter import *

#this is the path to the location of the settings file, change this as approprsiate 
#before using the code
fn = "/home/jojo161/MISU/job_summer_2020/Code/settings.json"

#first the settings are loaded
settings_list = load_settings(fn)

#as multiple runs with different settings can be read from the same settings file
#these different settings are looped.

for setting in settings_list: 
    print(setting["plot_name"])  
    if setting["local"] == "True":
        #takes the files from a specified local directory, see get_local_ds.py
        mod_ds, obs_ds, file_names = get_local_ds(setting["start_date"],setting["end_date"],setting["path_to_db"],setting["site"],setting["model_types"],setting["forcast_time"])
        
        #takes the latitude and longitude from the first observational file to use in filtering
        #in single_files() and combined_files()
        target_lat_lon = (obs_ds[0]["lat"],obs_ds[0]["lon"])

        #observational files are always handled the same way, here the required data is 
        #retrieved and filtered, see get_var_sets.py
        filtered_obs_var = observation_files(obs_ds,setting["obs_start_date"],setting["end_date"],setting["height_high"],setting["height_low"],setting["time_wanted"])
        filtered_mod_var = []
        
        
        if setting["single"] == "True":
            #handles the files as single entities, retrieves data and filters it, see get_var_sets.py
            filtered_mod_var = single_files(mod_ds,setting,target_lat_lon)
        else:
            #combines multiple files into one set of data and filters it, see get_var_sets.py
            filtered_mod_var = combine_files(mod_ds,setting,target_lat_lon,file_names)
            

            
    
    #plots the data retreived above, see plot.py
    plot(filtered_mod_var,filtered_obs_var[0],setting)
    

