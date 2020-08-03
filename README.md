Project Title


Getting started
        
        prerequisites
       
---------------------------------------------------
How to change settings:

the following is the format for the settings in the json file:
    {
    "plot_name":"plot_one",
    "start_date": "2018-03-29 00:00:00",
    "end_date": "2018-03-30 23:59:59",
    "height_high": 100, 
    "height_low" : 0,
    "variables" : [
      "ta",
      "tas",
      "ts"
    ],
    "local" : "True",
    "single" : "True",
    "time_wanted": 48,
    "path_to_db" : "/home/jojo161/MISU/job_summer_2020/Data",
    "site" : "Barrow",
    "model_types" : [
      "ifs",
      "slav"
    ],
    "forcast_time" : "00",
    "plots" : [
      "timevar",
      "scatter"
    ],
    "colors" : [
      "red",
      "blue"
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
        

    Dates in "start_time" & "end_time" must be entered on the form:
          YEAR-MONTH-DAY HR:MIN:SEC
          XXXX-XX-XX XX:XX:XX


    Filenames should be entered in the form of a python list:
          [
            "filename.nc",
            "next_filename.nc"
          ]
          The files must be netCDF files.


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



-----------------------------------------------------
Authors:

        Johanna Tjernström, email: johanna.a.k.tjernstrom@gmail.com

                
 