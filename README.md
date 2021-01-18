YOPPsiteMIP model evaluation


---------------------------------------------------
Getting started:
        prerequisites: \n
                all contained in this Git repo, use the structure visually detailed in the Dcumentation for Data folder to contain your database of model and observational files. \n
                python 3 \n
                netCDF4 for python \n
                matplotlib \n
                numpy\n
                cftime \n
                datetime \n
                os python \n
                json \n
                
       Note that this code was created and tested in Linux Ubuntu, this code has not been tried in Windows and may need adaptation 
       if it is to be used in Windows.
---------------------------------------------------
How to change settings:

The changable settings for reading and plotting data from netCDF files
are contained in the file "settings.json". Changes to this file must follow 
the following format:

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
     
    The field "plot_name" dictates the name that the saved plot figure will have.
    
    The filed "start_date" sets the start date for the data wanted, this in conjunction with "end_date" dictates which files are retrieved. 
    
    The field "obs_start_date" is used in retrieving the correct observation file and corresponds to the start date mentioned in that observational file.
    
    The fields "height_high" and "height_low" determine the range of height used for filtering the data, height high must always be greater than height low.  
    
    The field "variables" dictates which vatiables are read in and plotted, this must be entered in the form of a python list i.e. [ "variable1", "variable2","etc."]
    
    The field "local" determines weather or not the files should be read in from a local directory or from an external database, currently reading from external database is 
    not supported, hence it should always be set to True, unless this function is implemented. Should be enterd as a bool, either True or False.
    
    The field "single" determines weather or not all files read are treated as singular files with separate timelines or are concatenated into one file with one timeline, see 
    more indeapth description and advice below. Should be enterd as a bool, either True or False.
    
    The field "time_wanted" dictates how many hours of data are retrieved from each file. Input an integer in hours, ex: 24
    
    The fields "path_to_db" and "path_to_fig" dictate the paths to where the database can be found and where the figures should be saved respectively. See above example, 
    these must be changed to reflect your setup.
    
    The field "site" determines the location from which the data is used, ex: Barrow
    
    The field "model_types" specifies which models should be used, this muct be enterd in the form of a python list i.e. ["ifs","slav"]
    
    The field "forcast_time" is used to specify weather forcasts starting at 00 or 12 should be used.
    
    The field "plots" is used to specify which plot types should be made this muct be enterd in the form of a python list i.e. ["timevar"]
    
    The field "colors" is used by scatter to vary the colors used for plotting, there must be enough of them to provide every single plotted file/model with one each. 
    
    The field "single_point" is used to determine if only one point should used when using a model that contains more than one point, the lat and lon fileds are used to       
    select the point used.
    
    
    The plot_type field must contain one of the following types of plots:
        - "scatter"
        - "timevar"
    note that the way the data is read as either a single concatenated string of data from different files (taking 24h from different files within the timeline and creating 
    one dataset)  or different files (taking desired amount of hours from each file and handling them as separate data sets) has an effect on the way the result is formatted. 
    This is set by setting "Single": to either True or False.
    For best results use Single: False when using scatter with multiple models
    And Single: True when using scatter on just one model
    Using Single : True on timevar should give timeline overlap 
        

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

        this should run the program. When the program runs the plot names
        of the created plots should be prnted in the terminal. 


-----------------------------------------------------
Testing:
        All functions provided in these files have been tested for filtering by time and level for scatter plots and timevar plots. The file settings.json 
        contains a few sample plots, two timevar (plot_one, plot_two) one combined one separate for the ifs model, and two scatterplots (plot_three,plot_four) one a single 
        ifs scatter the other a combined with ifs and slav. All the tests were carried out in Linux Ubuntu, this code has not been tried in Windows and may need adaptation 
        if it is to be used in Windows.
       

-----------------------------------------------------
Authors:

        Johanna Tjernström, email: johanna.a.k.tjernstrom@gmail.com

                
 
