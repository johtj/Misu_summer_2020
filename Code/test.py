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

hours = 72
minutes = hours*60
time_var = ds14["time"] 

time_test = dt.datetime.strptime("2018-08-17 12:00:00",'%Y-%m-%d %H:%M:%S')
time_test_num = cf.date2num(time_test,time_var.units,calendar="standard")
print(time_test)
time_teest2 = time_test_num + 72*60
print(cf.num2date(time_teest2,time_var.units,calendar="standard"))
