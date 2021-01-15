#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import cftime as cf
import matplotlib.ticker as tick

#purpose to plot models for set timespan with differnt starting points so they overlap
def plot_single(data,settings,plot_type):
    units = data[0]["time_units"]
    for sets in data:
        time_plt = cf.date2num(sets["time_str"],units,calendar="standard")
        for key in sets.keys():
            if "name" not in key:
                if "time" not in key:
                    plt.plot(time_plt,sets[key],label = key +" " +sets["name"])
                
        
    
                    
    plt.xlabel(units)
    path = settings["path_to_fig"]
    img_name = path+"/" + settings["plot_name"] +".png"
    plt.legend()
    plt.savefig(img_name) 
    plt.close()  
        
        
#create one connected line from start time based on selected hours 
def plot_combined(data,settings,plot_type):
    for model in data:
        time_num = cf.date2num(model["time_str"],model["time_units"],calendar="standard")
        time_units = model["time_units"]
        for key in model.keys():
            if "name" not in key:
                if "time" not in key:
                    plt.plot(time_num,model[key],label = key+" "+model["name"])
        
   
    path = settings["path_to_fig"]
    img_name = path+"/" + settings["plot_name"] +".png"
    plt.legend()
    plt.savefig(img_name)
    plt.close()