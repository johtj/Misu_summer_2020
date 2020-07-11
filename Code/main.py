#!/usr/bin/env python3

from reading_files import *
from read_settings import *
from plot import *
import netCDF4 as nc

fn = "/home/jojo161/MISU/job_summer_2020/settings.json"

settings_list = load(fn)
for setting in settings_list:
    data =[]
    filenames = setting["file_names"]
    for filename in filenames:
        data.append(get_data(setting["variables"],filename, setting["start_time"],setting["end_time"],setting["height_high"],setting["height_low"]))
        print("hi")
        plot(data)

