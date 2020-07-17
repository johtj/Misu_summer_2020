#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import cftime as cf

def scatter_plot(mod_data,obs_data,settings):
    obs_data = obs_data[0]
    for model in mod_data:
        
        unit_mod = model["time_units"]
        print(unit_mod)
        time_mod = cf.date2num(model["time_str"],unit_mod,calendar="standard")
        time_obs_mod_units = cf.date2num(obs_data["time_str"],unit_mod,calendar="standard")
        
        result_tas = []
        result_time = []
        lower = 0 
        forklist = []
        for ref_time in time_mod:
            hotspot = np.where((time_obs_mod_units==ref_time))[0]
            print(len(hotspot))
            result_tas.append(obs_data["tas_2m"][hotspot])

        # for ref_time in time_mod:
        #     hotspot = np.where((time_obs_mod_units<=ref_time)&(time_obs_mod_units>=lower))[0]
        #     lower = ref_time
        #     index = int(len(hotspot)/2)
        #     result_time.append(hotspot[index])
        # for i in result_time:
        #     forklist.append(obs_data["tas_2m"][i])

        plt.scatter(model["tas"],result_tas)
        
    # path = "/home/jojo161/MISU/job_summer_2020/Figures/"
    # img_name = path + settings["plot_name"] + plot_type +".png"
    # plt.legend()
    # plt.savefig(img_name) 
    plt.show()
    #plt.close() 