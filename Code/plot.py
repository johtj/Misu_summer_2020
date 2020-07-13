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
        print("in single")
        plot_single(data,settings)
    else:
        plot_combined(data,settings)



def plot_single(data,settings):
    time_units = data[-1]["time_units"]
    for sets in data:
        for key in sets.keys():
            print(key)
            if "time" not in key:
                if len(np.shape(sets[key])) < 4:
                    time_plt = cf.date2num(sets["time_str"],time_units,calendar="standard")
                    plt.plot(time_plt,sets[key],label = key)
                    
                else:
                    plt.plot(sets["time"],sets[key],label = key)
    

    plt.legend()
    plt.show()
    #plt.savefig("/home/jojo161/MISU/job_summer_2020/Figures/single_plot.png") 
    plt.close()  
        
        

def plot_combined(data,settings):
    for key in data.keys():
            if key != "time":
                if len(np.shape(data[key])) < 4:
                    plt.plot(data["time"],data[key][:,0,0],label = key)
                    
                else:
                    plt.plot(data["time"],data[key][:,:,0,0],label = key)

    plt.legend()
    plt.savefig("/home/jojo161/MISU/job_summer_2020/Figures/combined_plot.png")
    plt.close()