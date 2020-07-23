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
#mod = nc.Dataset("/home/jojo161/MISU/job_summer_2020/Data/Barrow/slav/00/barrow_slav-rhmc_2018032900.nc")
obs = nc.Dataset("/home/jojo161/MISU/job_summer_2020/Data/Barrow/obs/utqiagvik_obs_sop1.2jul2019.nc")
mod = nc.Dataset("/home/jojo161/MISU/job_summer_2020/Data/Barrow/ifs/00/barrow_ifs-ecmwf_2018032900.nc")


tas_mod = np.array(mod["tas"][0:95])
time_mod = np.array(mod["time"][0:1400])
unit_mod = mod["time"].units

tas_obs = np.array(obs["tas_2m"][80640:82080])
time_obs_num = np.array(obs["time"][80640:82080])
unit_obs = obs["time"].units

time_obs_str = cf.num2date(time_obs_num,unit_obs,calendar="standard")

time_obs_mod_units = cf.date2num(time_obs_str,unit_mod,calendar="standard")
print(unit_mod)
# for i in range(10):
#     print("obs: ",cf.num2date(time_obs_mod_units[i],unit_mod,calendar="standard"),time_obs_mod_units[i])
#     print("mod: ",cf.num2date(time_mod[i],unit_mod,calendar="standard"),time_mod[i])
#     print("______________________________________________________________")


print(cf.num2date(time_obs_mod_units[-1],unit_mod,calendar="standard"),time_obs_mod_units[-1])
print(cf.num2date(time_mod[-1],unit_mod,calendar="standard"),time_mod[-1])

delta = obs["time"].delta_t.split(" ")[1]
delta_time = dt.datetime.strptime(delta, '%H:%M:%S') - dt.datetime(1900,1,1)
dt_obs = delta_time.total_seconds()


result_tas = []
for ref_time in time_mod:
    match = np.where((time_obs_mod_units==ref_time))[0]
    if len(match) == 0:
       
        higher = ref_time+(1/dt_obs)
        
        lower = ref_time-(1/dt_obs)
    
        matches = np.where((time_obs_mod_units<higher)&(time_obs_mod_units>lower))[0]
        #print(ref_time,matches)
        
        #print(cf.num2date(lowerm,unit_mod,calendar="standard"),cf.num2date(higherm,unit_mod,calendar="standard"),cf.num2date(ref_time,unit_mod,calendar="standard"))
        #tas = [tas_obs[matches[1]],tas_obs[matches[0]]]
        #result_tas.append(np.mean(tas))
    else:
        #print(cf.num2date(match,unit_mod,calendar="standard"),cf.num2date(ref_time,unit_mod,calendar="standard"))
        result_tas.append(tas_obs[match])


# # plt.figure(1)
#plt.scatter(tas_mod,result_tas)
# # plt.xlabel("Model 2m temp /K")
# # plt.ylabel("Observation 2m temp /K")
#plt.show()

