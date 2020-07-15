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

obs = nc.Dataset("/home/jojo161/MISU/job_summer_2020/Data/Barrow/obs/utqiagvik_obs_sop1.2jul2019.nc")
obs_ds = [obs]
start_time = "2018-03-31 12:00:00"
end_time = "2018-03-31 23:52:30"
var = [ 
    "tas_2m",
    "tas_10m",
    "tas_20m"
]


def observation_file(obs_ds,start_time,end_time,variables, height_high,height_low):
    
    time_var = obs_ds[0]["time"]
    t = np.array(time_var[:])
    #print(np.shape(t))

    stime_dt = dt.datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S')
    stime_num = cf.date2num(stime_dt,time_var.units,calendar="standard")

    etime_dt = dt.datetime.strptime(end_time,'%Y-%m-%d %H:%M:%S')
    etime_num = cf.date2num(etime_dt,time_var.units,calendar="standard")

    time_index = np.where(((t >= stime_num)&(t<=etime_num)))[0]
    tindex_lo = time_index[0]
    tindex_hi = time_index[-1]
    
    

    
observation_file(obs_ds,start_time,end_time,var,0,100)

