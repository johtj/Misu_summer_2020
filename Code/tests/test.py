#!/usr/bin/env python3
import netCDF4 as nc
import numpy as np
import numpy.ma as npm
import cftime as cf
import datetime as dt
import os
from matplotlib import pyplot as plt

#barrow_slav-rhmc_2018081400.nc
#barrow_slav-rhmc_2018081500.nc
#barrow_slav-rhmc_2018081600.nc

#start will be 2018 08 14 00:00:00 and end will be 2018 08 16 23:00:00
# take that timespan of each file
mod = nc.Dataset("/home/jojo161/MISU/job_summer_2020/Data/Barrow/slav/00/barrow_slav-rhmc_2018032900.nc")
obs = nc.Dataset("/home/jojo161/MISU/job_summer_2020/Data/Barrow/obs/utqiagvik_obs_sop1.2jul2019.nc")



tas_mod = np.array(mod["tas"][0:95,0,0])
time_mod = np.array(mod["time"][0:95])
unit_mod = mod["time"].units
tas_obs = np.array(obs["tas_2m"][80640:82080])
time_obs_num = np.array(obs["time"][80640:82080])
unit_obs = obs["time"].units

time_obs_str = cf.num2date(time_obs_num,unit_obs,calendar="standard")
time_obs_mod_units = cf.date2num(time_obs_str,unit_mod,calendar="standard")


result_tas = []
lower = 0 
forklist = []
for ref_time in time_mod:
    hotspot = np.where((time_obs_mod_units==ref_time))
    result_tas.append(tas_obs[hotspot])

plt.figure(1)
plt.scatter(tas_mod,result_tas)
plt.xlabel("Model 2m temp /K")
plt.ylabel("Observation 2m temp /K")



result_tas = []
result_time = []
lower = 0 
forklist = []
for ref_time in time_mod:
    hotspot = np.where((time_obs_mod_units<=ref_time)&(time_obs_mod_units>=lower))[0]
    lower = ref_time
    index = int(len(hotspot)/2)
    result_time.append(hotspot[index])
for i in result_time:
    forklist.append(tas_obs[i])

plt.figure(2)
plt.scatter(tas_mod,forklist)
plt.xlabel("Model 2m temp /K")
plt.ylabel("Observation 2m temp /K")
plt.show()

time_start = time_mod[0]
time_next = time_mod[1]
time_step = time_next-time_start

#then somehow filter the data from obs on the basis of it being every fiftenth point