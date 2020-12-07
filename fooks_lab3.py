#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# import packages
import fiona
import random
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# define function
def makepoint (xmin, xmax, ymin, ymax):
    """
    this is my attempt at making a function but I couldn't get it to work in this code
    if it did work, the function would create a random point within four given limits
    """
    x = random.uniform(xmin, xmax)
    y = random.uniform(ymin, ymax)
    p = Point(x,y)
    return p

# set up files
geopackage = "lab3.gpkg"
layers = fiona.listlayers(geopackage)
ssurgo = [f for f in layers if f.startswith('s')]
watersheds = [f for f in layers if f.startswith('w')]

# part 1
random.seed(0)
sample_points = {'pointID': [], 'geometry':[], 'hucID':[]}
for w in watersheds:
    watershed_output = gpd.read_file("lab3.gpkg", layer = w)
    huclist = [f for f in watershed_output.columns if 'HUC' in f][0]
    for idx, row in watershed_output.iterrows():
        bounds = row['geometry'].bounds
        n = (int(round((row['Shape_Area']/1000000)*0.05)))
        i = int(0)
        while i < n:
            x = random.uniform(bounds[0], bounds[2])
            y = random.uniform(bounds[1], bounds[3])
            #this would be where the function went if it worked
            #makepoint(bounds[0], bounds[2], bounds[1], bounds[3])
            p = Point(x,y)
            if row['geometry'].contains(p):
                sample_points['geometry'].append(p)
                sample_points['pointID'].append(row[huclist][0:8])
                sample_points['hucID'].append(huclist)
                i = i+1

# part 2
crs = {'init': 'epsg:4326'}
df = gpd.GeoDataFrame(sample_points, crs=crs)
df.groupby(by='pointID').count()
ssurgo_output = gpd.read_file("lab3.gpkg", layer='ssurgo_mapunits_lab3')
ssurgo_output.crs=crs
join_final = gpd.sjoin(df, ssurgo_output, how="left", op="within")
join_final.groupby(by=['hucID', 'pointID']).mean()


# In[ ]:




