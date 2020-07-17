#!/usr/bin/env python3

def filter(data,height,height_high,height_low,lat_lon,lat,lon):
    if height == True:
        level , half_level = get_levels(data["zg"],)
        for key in data.keys():
            #something that checks level or halflevel
            data[key] = data[key][:,level[0], level[1]]

    if lat_lon == True:
        #get index for provided lat & lon
        for key in data.keys():
            data[key] = data[key][:]



    



def get_levels(data_set,height_high,height_low,index_time):
    goph_level = np.array(data_set.variables["zg"][0,:])
    goph_half_level = np.array(data_set.variables["zghalf"][0,:])

    orog = int(data_set.variables["orog"][0])

    goph_level_new = goph_level - orog
    goph_half_level_new = goph_half_level -orog
    
    indecies_level = np.where((goph_level_new >= int(height_low))&(goph_level_new <= height_high))
    indecies_half_level = np.where((goph_half_level_new >= int(height_low))&(goph_half_level_new <= height_high))
   
    level , half_level = (indecies_level[0][0],indecies_level[0][-1]), (indecies_half_level[0][0],indecies_half_level[0][-1])
    return level,half_level      