#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import cftime as cf

def plot_single(data,settings,plot_type):
    time_units = data[0]["time_units"]
    for sets in data:
        time_plt = cf.date2num(sets["time_str"],time_units,calendar="standard")
        for key in sets.keys():
            if "time" not in key:
                plt.plot(time_plt,sets[key],label = key)

    
                    
    plt.xlabel(time_units)
    path = "/home/jojo161/MISU/job_summer_2020/Figures/"
    img_name = path + settings["plot_name"] +"_"+ plot_type +".png"
    plt.legend()
    plt.savefig(img_name) 
    plt.close()  
        
        

def plot_combined(data,settings,plot_type):
    time_num = cf.date2num(data["time_str"],data["time_units"],calendar="standard")
    time_units = data["time_units"]
    for key in data.keys():
        if "time" not in key:
                plt.plot(time_num,data[key],label = key)
        
   
    path = "/home/jojo161/MISU/job_summer_2020/Figures/"
    img_name = path + settings["plot_name"]+"_" + plot_type +".png"
    plt.xlabel(time_units)
    plt.legend()
    plt.savefig(img_name)
    plt.close()