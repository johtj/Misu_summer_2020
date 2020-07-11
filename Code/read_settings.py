#!/usr/bin/env python3
import json as js

def load(fn):
    try:
        with open(fn) as contents: 
          settings_db =js.load(contents)
 
        return settings_db

    except:
        print("File with filename: ",fn," does not exist")

def handle_height(setting):
    high_level = setting["high_level"]
    low_level = setting["low_level"]
    high_half_level = setting["high_half_level"]
    low_half_level = setting["low_half_level"]
    if high_level != low_level:
      level = (int(low_level),int(high_level))
    else:
      level = int(high_level)

    if high_half_level != low_half_level:
      half_level = (int(low_half_level),int(high_half_level))
    else:
      half_level = (int(high_half_level))

    return level,half_level
    