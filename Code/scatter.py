#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import cftime as cf

def scatter_plot(mod_data,obs_data,settings):
    for model in mod_data:
        unit_mod = model["time_units"]

        time_mod_num = cf.date2num(model["time_str"],unit_mod,calendar="standard")
        time_obs_num = cf.date2num(obs_data["time_str"],unit_mod,calendar="standard")
        
        print(obs_data["time_str"][0],obs_data["time_str"][-1])
        print(model["time_str"][0],model["time_str"][-1])
        time_start = time_mod_num[0]
        time_next = time_mod_num[1]
        time_step = int(time_next-time_start)
        obs_var = []
        index_step = time_step

        for i in range(len(time_mod_num)):
            obs_var.append(obs_data["tas_2m"][index_step])
            index_step = index_step + time_step

    plt.scatter(model["tas"],obs_var)
        
    # path = "/home/jojo161/MISU/job_summer_2020/Figures/"
    # img_name = path + settings["plot_name"] + plot_type +".png"
    # plt.legend()
    # plt.savefig(img_name) 
    plt.show()
    #plt.close() 