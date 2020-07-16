#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import cftime as cf

# def choose_plot(plot_type,data):
#     if plot_type = "scatter":
#         scatter(data)
#     elif plot_type = "":


def plot(data,settings):
    if settings["single"] == "True":
        plot_single(data,settings)
    else:
        plot_combined(data,settings)



def plot_single(data,settings):
    time_units = data[0]["time_units"]
    for sets in data:
        for key in sets.keys():
            if "time" not in key:
                if len(np.shape(sets[key])) < 4:
                    time_plt = cf.date2num(sets["time_str"],time_units,calendar="standard")
                    plt.plot(time_plt,sets[key],label = key)
                    
                else:
                    plt.plot(sets["time"],sets[key],label = key)

    path = "/home/jojo161/MISU/job_summer_2020/Figures/"
    img_name = path + settings["plot_name"] +".png"
    plt.legend()
    plt.savefig(img_name) 
    plt.close()  
        
        

def plot_combined(data,settings):
    time_num = cf.date2num(data["time_total"],data["time_units"],calendar="standard")
    for key in data.keys():
        if "time" not in key:
            if len(np.shape(data[key])) < 3:
                #if shape is (time,level)
                plt.plot(time_num,data[key],label = key)
            elif len(np.shape(data[key])) < 4:
                #if shape is (time,lat,lon)
                plt.plot(time_num,data[key][:,0,0],label = key)     
            else:
                #if shape is (time,level,lat,lon)
                plt.plot(time_num,data[key][:,:,0,0],label = key)
   
    path = "/home/jojo161/MISU/job_summer_2020/Figures/"
    img_name = path + settings["plot_name"] +".png"
    plt.legend()
    plt.savefig(img_name)
    plt.close()

def scatter_plot(model_data,observation_data,settings):
    #somehow..
    plt.plot(model_data,observation_data)
