#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import cftime as cf
import datetime as dt

#this file contains the function responsible for creating a scatter plot with the 
#modeldata on the x axis and observational data on the y-axis.
#as the observational data containes more datapoints than the model data, a 
#selection of points from obs are chosen so they can be plotted against each other. 

def scatter_plot(mod_data,obs_data,settings,var_name):
    #time_plt,units,calentime_plt,units,calendar="standard")[-1])dar="standard")[-1])
    #time string for observational data obtained
    obs_time_str = obs_data["time_str"]

    #time step calculated for the observational data
    obs_delta = obs_data["time_delta"].split(" ")[1]
    obs_delta_diff = dt.datetime.strptime(obs_delta, '%H:%M:%S') - dt.datetime(1900,1,1)
    dt_obs_hr = obs_delta_diff.total_seconds()/(60*2)

    var_obs = obs_data[var_name+"_2m"] #because the var names for tas vary between obs & mod
    #var_obs = obs_data[var_name] is the correct way, if the var names are constant across models and observations
    # line can be commented out or changed to fit other relevant variables.

    #creates a list of colors to use for different models if more than one is used
    colors = settings["colors"]
    color_index = 0

    
    
    for model in mod_data:
        
        color = colors[color_index]
       
        #converts the observational data timestring to numbers using the units 
        #of the model 
        obs_time_num = cf.date2num(obs_time_str,model["time_units"],calendar="standard")
        time_mod = cf.date2num(model["time_str"],model["time_units"],calendar="standard")
        
        tas_obs_res = []
        var_mod_res = []
        #time_check = [] used to check if the time selection is done correctly
    
        var_mod = model[var_name]

        
        #loops the model's time array and looks for a match in the observational data time array
        for reference in time_mod:

            match_initial = np.where(reference==obs_time_num)[0]
            #looks for an identical match between the time arrays

            if len(match_initial) == 0:
                #if no match is found the timestep from the observation (as calculated above)
                #is added to/subtracted from the reference time (from the model time array)
                #to create a reference interval

                ref_high = reference+dt_obs_hr
                ref_low = reference-dt_obs_hr

                #matches are then searched for in this interval
                matches_spec = np.where((ref_high >= obs_time_num)&(ref_low <= obs_time_num))[0]
                
            
                
                #if more than one match is found in the interval
                #the earlier of the two (low) is chosen as the representative value
                #the value from the desired variable
                # at this time index is then added to the results list
                
               
                if(len(matches_spec) != 0):
                    tas_obs_res.append(var_obs[matches_spec[0]])
                    var_mod_res.append(var_mod[np.where((reference == time_mod))[0][0]])
                
                    
                
                    
                    

                #time_check.append(obs_time_num[matches_spec[0]]) used to check if time selection is accurate

        
            else:
                #if the match is found initially the value from that time index is
                #added to the results list from the desited variable
                tas_obs_res.append(var_obs[match_initial][0])
                var_mod_res.append(var_mod[np.where((reference == time_mod))[0][0]])

                #time_check.append(obs_time_num[match_initial[0]]) used to check if time selection is accurate

        if settings["single"] != "True":
            name = model["name"]
            plt.scatter(var_mod_res,tas_obs_res,c=color, label = name )
            plt.legend()

        else:
            plt.scatter(var_mod_res,tas_obs_res,c = color)
        
        
        

        #plt.scatter(time_check,time_mod) used to check if time selection is accurate, if this
        #produces a/or something close to a  1to1 line plot then the time selection is accurate

        #changes the color for the next model
        color_index = color_index + 1

    #creates path to where the image should be saved,
    # change this in the json file according to where you want your figures saved.   
    path = settings["path_to_fig"]
    img_name = path+"/" + settings["plot_name"] +".png"

    #sets the x and y labels
    plt.xlabel("tas from model")
    plt.ylabel("tas from observation")

    #saves the figure at the location specified above, use plt.show()
    #if you wish to see the figure directly or go to the save location to see
    #the finished figure
    plt.savefig(img_name) 
    plt.close() 