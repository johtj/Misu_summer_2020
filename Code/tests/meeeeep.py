#!/usr/bin/env python3
import netCDF4 as nc
import numpy as np
import numpy.ma as npm
import cftime as cf
import datetime as dt
from datetime import timedelta
import os
from matplotlib import pyplot as plt
obs = nc.Dataset("/home/jojo161/MISU/job_summer_2020/Data/Barrow/obs/utqiagvik_obs_sop1.2jul2019.nc")
mod = nc.Dataset("/home/jojo161/MISU/job_summer_2020/Data/Barrow/ifs/00/barrow_ifs-ecmwf_2018032900.nc")

#find the start to end date array for the model and observation data, also their units
time_mod = np.array(mod["time"][0:191])
unit_mod = mod["time"].units

time_obs_num = np.array(obs["time"][80640:82080])
unit_obs = obs["time"].units
print(unit_mod)
#########################################################################################
#creates the tas variable for the model and observational data

tas_obs = obs["tas_2m"][:]
tas_mod = mod["tas"][0:191]
#########################################################################################
#convert the observation time data to use the units of the model
str_obs = cf.num2date(time_obs_num,unit_obs,calendar="standard")

obs_using_mod_units = cf.date2num(str_obs,unit_mod,calendar="standard")

print("model start date: ",cf.num2date(time_mod[0],unit_mod,calendar="standard"),time_mod[0])
print("obs start date: ",cf.num2date(obs_using_mod_units[0],unit_mod,calendar="standard"),obs_using_mod_units[0])
print("model end date: ",cf.num2date(time_mod[-1],unit_mod,calendar="standard"),time_mod[-1])
print("obs end date: ",cf.num2date(obs_using_mod_units[-1],unit_mod,calendar="standard"),obs_using_mod_units[-1])
print("______________________________________________________________________")
###########################################################################################
#find the timestep of the model

delta = obs["time"].delta_t
print("time step for model: ",delta)
delta_time = delta.split(" ")[1]
delta_time_diff = dt.datetime.strptime(delta_time, '%H:%M:%S') - dt.datetime(1900,1,1)
dt_obs_min = delta_time_diff.total_seconds()/60
dt_obs_hr = dt_obs_min/60
print("total hours in delta: ",dt_obs_hr)
print("_______________________________________________________________________")

############################################################################################
#organize time between model and observation data
tas_obs_res = []
time_check = []
for reference in time_mod:
    match_initial = np.where(reference==obs_using_mod_units)[0]
    if len(match_initial) == 0:
        ref_high = reference+dt_obs_hr
        ref_low = reference-dt_obs_hr

        matches_spec = np.where((ref_high >= obs_using_mod_units)&(ref_low <= obs_using_mod_units))[0]
        #choose the earlier of the two (low) as the representative value

        time_check.append(obs_using_mod_units[matches_spec[0]])
        tas_obs_res.append(tas_obs[matches_spec[0]])

        
    else:
        time_check.append(obs_using_mod_units[match_initial])
        tas_obs_res.append(tas_obs[match_initial])
print(len(time_mod),len(tas_mod))
print(len(time_check),len(tas_obs_res))

plt.figure(1)
plt.scatter(time_mod,tas_obs_res)
plt.xlabel("time from model (hrs from 2018-03-29 00:00:00)")
plt.ylabel("tas selection from obs")

plt.figure(2)
plt.scatter(tas_mod,tas_obs_res)
plt.xlabel("tas from model")
plt.ylabel("tas from observation")

plt.figure(3)
plt.scatter(time_mod,tas_mod)
plt.xlabel("time from model (hrs from 2018-03-29 00:00:00)")
plt.ylabel("tas from model")

plt.figure(4)
plt.scatter(time_check,time_mod)
plt.xlabel("time obs")
plt.ylabel("time mod")
plt.show()