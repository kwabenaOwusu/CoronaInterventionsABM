#!/usr/bin/env python
# coding: utf-8


### import  modules
import osmnx as ox
import networkx as nx
import pandas as pd
import geopandas as gpd
import numpy
import pylab
import random
import csv 
import math
import matplotlib.pyplot as plt
from matplotlib import gridspec
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
plt.rcParams.update({'figure.max_open_warning': 0})
#get_ipython().run_line_magic('matplotlib', 'inline')
#import contextily as ctx
#import mplleaflet
from pyproj import CRS
import os
from shapely.geometry import Point, LineString, Polygon, MultiPoint
from shapely.ops import nearest_points

ox.config(log_console=True, use_cache=True)
ox.__version__


### get the graph of the street
place_name = 'Dakar, Senegal'
G = ox.graph_from_place(place_name,which_result=3) 
G_proj = ox.project_graph(G, to_crs= CRS("EPSG:3857"))
nodes_proj, edges_proj = ox.graph_to_gdfs(G_proj)
ox.save_graph_shapefile(G_proj, filename='graph')

#retrieve saved graph and use (if necessary)
edges_saved = "data/graph/edges/edges.shp"
nodes_saved = "data/graph/nodes/nodes.shp"
edges_proj = gpd.read_file(edges_saved)
nodes_proj = gpd.read_file(nodes_saved)


###get boundary of study area
boundary = ox.gdf_from_place(place_name,which_result=3)
boundary_proj = boundary.to_crs(edges_proj.crs)
ox.save_gdf_shapefile(boundary_proj, filename='boundary')

boundary_saved = "data/boundary/boundary.shp"
boundary_proj = gpd.read_file(boundary_saved)


###points-of-interest of study area

### hospitals
hospitals = ox.pois_from_place(place_name,which_result=3 ,amenities=['hospital'])[['osmid', 
                                                                 'geometry', 
                                                                   'amenity', 
                                                                  'name',
                                                                   'element_type']] 

hospitals=hospitals[hospitals.element_type=='way' ]
hospitals_proj = hospitals.to_crs(edges_proj.crs)
ox.save_gdf_shapefile(hospitals_proj, filename='hospitals')
hospitals_saved = "data/hospitals/hospitals.shp"
hospitals_proj = gpd.read_file(hospitals_saved)
hospitals_proj['centroid']= hospitals_proj.centroid



###schools
schools = ox.pois_from_place(place_name,which_result=3, amenities=['school'])[['osmid', 
                                                                   'geometry', 
                                                                   'amenity', 
                                                                   'name',
                                                                   'element_type']] 

schools=schools[schools.element_type=='way' ]
schools_proj = schools.to_crs(edges_proj.crs)
ox.save_gdf_shapefile(schools_proj, filename='schools')
schools_saved = "data/schools/schools.shp"
schools_proj = gpd.read_file(schools_saved)
schools_proj['centroid']= schools_proj.centroid


###place of worship 
place_worship = ox.pois_from_place(place_name,which_result=3 ,amenities=['place_of_worship'] )[['osmid', 
                                                                   'geometry', 
                                                                   'amenity', 
                                                                   'name',
                                                                   'element_type']] 

place_worship=place_worship[place_worship.element_type=='way' ]
place_worship_proj = place_worship.to_crs(edges_proj.crs)
ox.save_gdf_shapefile(place_worship_proj, filename='place_worship')
place_worship_saved = "data/place_worship/place_worship.shp"
place_worship_proj = gpd.read_file(place_worship_saved)
place_worship_proj['centroid']= place_worship_proj.centroid


### market / shopping centers
marketplaces = ox.pois_from_place(place_name,which_result=3, amenities=['marketplace'] )[['osmid', 
                                                                   'geometry', 
                                                                   'amenity', 
                                                                   'name',
                                                                   'element_type']] 

marketplaces=marketplaces[marketplaces.element_type=='way' ]
marketplaces_proj = marketplaces.to_crs(edges_proj.crs)
ox.save_gdf_shapefile(marketplaces_proj, filename='marketplaces')
marketplaces_saved = "data/marketplaces/marketplaces.shp"
marketplaces_proj = gpd.read_file(marketplaces_saved)
marketplaces_proj['centroid']= marketplaces_proj.centroid



