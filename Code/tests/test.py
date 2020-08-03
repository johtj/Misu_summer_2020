#!/usr/bin/env python3
import netCDF4 as nc
import numpy as np
import numpy.ma as npm
import cftime as cf
import datetime as dt
from datetime import timedelta
from matplotlib import pyplot as plt

#barrow_slav-rhmc_2018081400.nc
#barrow_slav-rhmc_2018081500.nc
#barrow_slav-rhmc_2018081600.nc

#start will be 2018 08 14 00:00:00 and end will be 2018 08 16 23:00:00
# take that timespan of each file
mod1 = nc.Dataset("/home/jojo161/MISU/job_summer_2020/Data/Barrow/slav/00/barrow_slav-rhmc_2018032900.nc")
obs = nc.Dataset("/home/jojo161/MISU/job_summer_2020/Data/Barrow/obs/utqiagvik_obs_sop1.2jul2019.nc")
mod2 = nc.Dataset("/home/jojo161/MISU/job_summer_2020/Data/Barrow/ifs/00/barrow_ifs-ecmwf_2018032900.nc")

mod_ds = [mod1,mod2]
mod_types = ["slav","ifs"]
file_names = ['/home/jojo161/MISU/job_summer_2020/Data/Barrow/slav/00/barrow_slav-rhmc_2018032900.nc', '/home/jojo161/MISU/job_summer_2020/Data/Barrow/ifs/00/barrow_ifs-ecmwf_2018032900.nc']
time = mod2["time"]
time_var = time[0:25]

units = time.units
time_str = cf.num2date(time_var,units,calendar="standard")
print(time_str[0],time_str[-1])
print(units)
units = units.replace("minutes","hours")
time_num = cf.date2num(time_str,units,calendar="standard")
print(time_num[0],time_num[-1])
time_str_again = cf.num2date(time_num,units,calendar="standard")
print(time_str_again[0],time_str_again[-1])
print(units)