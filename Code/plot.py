#!/usr/bin/env python3
import numpy as np
from timevar import *
from scatter import *

#this file contains the function responsible for callling the plot functions 
#according to instructions taken from settings.json
#functions called in this file can be found in timevar.py and scatter.py as are imported above

def plot(mod_var,obs_var,settings):

    #loops for each of the plot types specified, calls the apropriate
    #function for plotting each type.
    for plt_type in settings["plots"]:
        if plt_type == "timevar":
            if settings["single"] == "True":
                plot_single(mod_var,settings,plt_type)
            else:
                plot_combined(mod_var[0],settings,plt_type)
        elif plt_type == "scatter":
            scatter_plot(mod_var,obs_var,settings,"tas")





