#!/usr/bin/env python3
import json as js

def load_settings(fn):
    try:
        with open(fn) as contents: 
          settings_db =js.load(contents)
 
        return settings_db

    except:
        print("File with filename: ",fn," does not exist")

