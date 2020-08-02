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

array = np.array([[10, 11, 12],[13, 14, 15]])

print(array)

target_easy = 11
target_meeep = 11.5

idx_easy = np.abs(array-target_easy).argmin()

print(idx_easy)

idx = np.abs(array-target_meeep).argmin()

print(idx)