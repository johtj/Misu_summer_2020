#!/usr/bin/env python3
import netCDF4 as nc
import numpy as np
import numpy.ma as npm
import cftime as cf
import datetime as dt
from datetime import timedelta
import os
from matplotlib import pyplot as plt

#barrow_slav-rhmc_2018081400.nc
#barrow_slav-rhmc_2018081500.nc
#barrow_slav-rhmc_2018081600.nc

#start will be 2018 08 14 00:00:00 and end will be 2018 08 16 23:00:00
# take that timespan of each file
mod = nc.Dataset("/home/jojo161/MISU/job_summer_2020/Data/Barrow/slav/00/barrow_slav-rhmc_2018032900.nc")
obs = nc.Dataset("/home/jojo161/MISU/job_summer_2020/Data/Barrow/obs/utqiagvik_obs_sop1.2jul2019.nc")
#mod = nc.Dataset("/home/jojo161/MISU/job_summer_2020/Data/Barrow/ifs/00/barrow_ifs-ecmwf_2018032900.nc")


mod_ta = mod["ta"][:]
print(np.shape(mod_ta))
mod_ta_trans = np.transpose(mod_ta, (0, 3, 1, 2))
print(mod_ta_trans[:,:,0,0])
print(np.shape(mod_ta_trans[:,:,0,0]))
print(np.shape(mod_ta_trans[:,:,0:1,0:1]))
print(mod_ta_trans[0:1,0:1,:,:])
print(mod_ta_trans[0,0,:,:])


