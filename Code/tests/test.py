#!/usr/bin/env python3
import netCDF4 as nc
import numpy as np
import numpy.ma as npm
import cftime as cf
import datetime as dt
import os

#barrow_slav-rhmc_2018081400.nc
#barrow_slav-rhmc_2018081500.nc
#barrow_slav-rhmc_2018081600.nc

#start will be 2018 08 14 00:00:00 and end will be 2018 08 16 23:00:00
# take that timespan of each file

#ds14 = nc.Dataset("/home/jojo161/MISU/job_summer_2020/Barrow_slav/barrow_slav-rhmc_2018081400.nc")
#ds15 = nc.Dataset("/home/jojo161/MISU/job_summer_2020/Barrow_slav/barrow_slav-rhmc_2018081500.nc")
#ds16 = nc.Dataset("/home/jojo161/MISU/job_summer_2020/Barrow_slav/barrow_slav-rhmc_2018081600.nc")
#datasets = [ds14]
#variables = ["ta","tas","ts"]
#test_time = dt.datetime.strptime("2018081400",'%Y%m%d%H')

start_date = "2018-03-29 00:00:00"
end_date = "2018-03-31 00:00:00"
#print(start_date)
paths = ["/home/jojo161/MISU/job_summer_2020/Sodankyla_ifs/00/"]
obs = "/home/jojo161/MISU/job_summer_2020/utqiagvik_obs_sop1.2jul2019.nc"

read = nc.Dataset(obs)
print(read)


