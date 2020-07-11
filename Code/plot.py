#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np

# def choose_plot(plot_type,data):
#     if plot_type = "scatter":
#         scatter(data)
#     elif plot_type = "":

def plot(data):
    for sets in data:
        for variable in sets:
            if variable != "time":
                plt.plot(sets["time"],sets[variable])
        plt.show()