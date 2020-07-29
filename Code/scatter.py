#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import cftime as cf
import datetime as dt

def scatter_plot(mod_data,obs_data,settings,var_name):
    
    obs_time_str = obs_data["time_str"]

    obs_delta = obs_data["time_delta"].split(" ")[1]
    obs_delta_diff = dt.datetime.strptime(obs_delta, '%H:%M:%S') - dt.datetime(1900,1,1)
    dt_obs_hr = obs_delta_diff.total_seconds()/(60*2)

    var_obs = obs_data[var_name+"_2m"] #because the var names for tas vary between obs & mod

    colors = settings["colors"]
    color_index = 0
    for model in mod_data:
        color = colors[color_index]
        print(color)
        obs_time_num = cf.date2num(obs_time_str,model["time_units"],calendar="standard")
        time_mod = cf.date2num(model["time_str"],model["time_units"],calendar="standard")

        tas_obs_res = []
        time_check = []

        var_mod = model[var_name]

        for reference in time_mod:
            match_initial = np.where(reference==obs_time_num)[0]
            if len(match_initial) == 0:
                ref_high = reference+dt_obs_hr
                ref_low = reference-dt_obs_hr

                matches_spec = np.where((ref_high >= obs_time_num)&(ref_low <= obs_time_num))[0]
                #choose the earlier of the two (low) as the representative value

                time_check.append(obs_time_num[matches_spec[0]])
                tas_obs_res.append(var_obs[matches_spec[0]])

        
            else:
                time_check.append(obs_time_num[match_initial[0]])
                tas_obs_res.append(var_obs[match_initial][0])

        print(len(time_mod),len(var_mod))
        print(len(time_check),len(tas_obs_res))
        
        
    
        try:
            plt.scatter(var_mod,tas_obs_res,c = color)
        except:
            plt.scatter(var_mod[:,0,0],tas_obs_res,c = color)
        color_index = color_index + 1
        #plt.scatter(time_check,time_mod)
        
    path = "/home/jojo161/MISU/job_summer_2020/Figures/"
    img_name = path + settings["plot_name"] +".png"
    plt.xlabel("tas from model")
    plt.ylabel("tas from observation")
    plt.savefig(img_name) 
    #plt.show()
    plt.close() 