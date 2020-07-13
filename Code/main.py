#!/usr/bin/env python3

from get_data import *
from read_settings import *
from plot import *
import netCDF4 as nc

fn = "/home/jojo161/MISU/job_summer_2020/settings.json"

settings_list = load(fn)
for setting in settings_list:
    if setting["local"] == "True":
        ds_list = get_dataset(setting["file_names"])

        if setting["single"] == "True":
            data = single_file(ds_list,setting["start_time"],setting["end_time"],setting["variables"],setting["height_high"],setting["height_low"])
        else:
            print("in comb")
            data = combine_files(ds_list,setting["variables"],setting["height_high"],setting["height_low"])
    
    plot(data,setting)

