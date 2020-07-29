#!/usr/bin/env python3
import numpy as np
from timevar import *
from scatter import *

def plot(mod_var,obs_var,settings):
    for plt_type in settings["plots"]:
        if plt_type == "timevar":
            if settings["single"] == "True":
                plot_single(mod_var,settings,plt_type)
            else:
                plot_combined(mod_var,settings)
        elif plt_type == "scatter":
            scatter_plot(mod_var,obs_var,settings,"tas")





