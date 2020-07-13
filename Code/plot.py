#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np

# def choose_plot(plot_type,data):
#     if plot_type = "scatter":
#         scatter(data)
#     elif plot_type = "":

def plot(data,settings):
    #for sets in data:
        for key in data.keys():
            if key != "time":
                if len(np.shape(data[key])) < 4:
                    plt.plot(data["time"],data[key][:,0,0],label = key)
                    
                else:
                    plt.plot(data["time"],data[key][:,:,0,0],label = key)

        plt.legend()
        plt.show()
        