#!/usr/bin/env python3
import json as js

#this file contains the function responsible for loading the settings 
#from the file settings.json. If you can't get this function to work for you make sure
#that either the settings.json file is in the same directory as this code, or include
#the full path when providing the filename.
def load_settings(fn):
    try:
        with open(fn) as contents: 
          settings_db =js.load(contents)
 
        return settings_db

    except:
        print("File with filename: ",fn," does not exist")

