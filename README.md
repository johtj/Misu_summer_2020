Project Title


Getting started
        
        prerequisites
       
---------------------------------------------------
How to change settings:

the following is the format for the settings in the json file:
    {
    "plot_name":"plot_one",
    "start_date": "2018-08-26 00:00:00",
    "end_date": "2018-08-31 23:59:59",
    "obs_start_date":"2018-03-29 00:00:00",
    "height_high": 100, 
    "height_low" : 0,
    "variables" : [
      "tas"
    ],
    "local" : "True",
    "single" : "True",
    "time_wanted": 24,
    "path_to_db" : "/home/jojo161/MISU/job_summer_2020/Data",
    "path_to_fig" : "/home/jojo161/MISU/job_summer_2020/Figures",
    "site" : "Barrow",
    "model_types" : [
      "slav"
    ],
    "forcast_time" : "00",
    "plots" : [
      "timevar"
    ],
    "colors" : [
      "red",
      "blue",
      "green",
      "black",
      "cyan",
      "magenta"
    ],
    "single_point" : "True",
    "lat_ind_hi": 1,
    "lat_ind_lo": 1,
    "lon_ind_hi" : 1,
    "lon_ind_lo" : 2
  }


The changable settings for reading and plotting data from netCDF files
are contained in the file "settings.json". Changes to this file must follow 
the following format:
    
    the plot_type field must contain one of the following types of plots:
        - "scatter"
        - "timevar"
    note that the way the data is read as either a single concatenated string of data from different files (taking 24h from different files within the timeline and creating one dataset)  or different files (taking desired amount of hours from each file and handling them as separate data sets) has an effect on the way the result is formatted. This is set by setting "Single": to either True or False.
    For best results use Single: False when using scatter with multiple models
    And Single: True when using scatter on just one model
    Using Single : True on timevar should give timeline overlap (this function is currently in development)
        

    Dates in "start_time" & "end_time" must be entered on the form:
          YEAR-MONTH-DAY HR:MIN:SEC
          XXXX-XX-XX XX:XX:XX

     Change the paths in "path_to_db" and "path_to_fig" to reflect where you
     have the database files (netcdf files) as well as to where you need you
     figures
    


    Any inputs in the level fields should be integers,
    hence do NOT require "". 
          NOTE! high_level & high_half_level must be GREATER than
          low_level & low_half_level

    Variables wanted should be entered in the form of a python list:
           [
            "variable1",
            "variable2"
           ] 
           NOTE! do not add time to variable list, a time variable is
           created automatically.   

-----------------------------------------------------
Running the code:
        change the relevant settings in the json file.
        in the terminal from the root folder run the command:
        
        python3 Code/main.py

        this should run the program



-----------------------------------------------------
Authors:

        Johanna Tjernström, email: johanna.a.k.tjernstrom@gmail.com

                
 