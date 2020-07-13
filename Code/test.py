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

dims = ds14.dimensions
if "lat" in dims:
    lat = ds14["lat"]
    if len(lat) < 1:
        