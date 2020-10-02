
import matplotlib.pyplot as plt 
import cartopy 
import cartopy.crs as ccrs 
import env_methods as em 
import numpy as np 
import geopandas as gpd
import math

#This is a basic method to plot a given 2d numpy array of scalar data, along with it's associated latitude and longitude values.
#Optional parameters to limit the visualization to a rectangle with minimum and maximum longitude and latitude values
def plot_data(lon, lat, data, scalebar, title, lon_min = 0, lon_max = 359, lat_min = -90, lat_max = 90, has_scale_bounds = False, scale_min = 0, scale_max = 0, figsize_x = 20, figsize_y = 15, colormap = "coolwarm"): 
    #make the figure
    fig = plt.figure(figsize = (figsize_x, figsize_y))
    ax = plt.axes(projection = ccrs.PlateCarree(central_longitude = 0))
    ax.coastlines()
    ax.add_feature(cartopy.feature.LAKES, alpha=1)
    ax.add_feature(cartopy.feature.RIVERS, alpha = 1)
    
    #The latitudes break because of how they're set up in the NOAA renalysis data unless you do this
    lat1 = em.find_closest_val(lat_min, lat)
    lat2 = em.find_closest_val(lat_max, lat)
    
    #label axes and the graph
    ax.set_extent((lon_min, lon_max, lat_min, lat_max))
    ax.set_xticks(lon[math.ceil(lon_min / 10) * 10:lon_max][::10], crs = ccrs.PlateCarree())
    ax.set_yticks(lat[math.ceil(lat1 / 10) * 10:lat2][::10], crs = ccrs.PlateCarree())
    plt.xlabel('lon')
    plt.ylabel('lat')
    plt.title(title)
    
    #
    if not has_scale_bounds:
        mesh = plt.pcolormesh(lon[lon_min:lon_max], 
                              lat[lat1:lat2], 
                              data[lat1:lat2, lon_min:lon_max], 
                              cmap=colormap)
    else:
        mesh = plt.pcolormesh(lon[lon_min:lon_max], 
                              lat[lat1:lat2], 
                              data[lat1:lat2, lon_min:lon_max], 
                              cmap=colormap, vmin = scale_min, vmax = scale_max)
    cbar = plt.colorbar(mesh)
    cbar.set_label(scalebar)

#This is a basic method to plot a given collection of vector data (with the x and y componenets given separately) along with associated
#lat and lon values, vectors colored according to magnitude. Optional parameters to limit bounds of visualization, the scale of the vectors, and, since these plot can get
#messy, how many degrees of lat & lon should separate the vectors
def plot_vector_data(lon, lat, x_data, y_data, title, scale_title, 
                     lon_min = 0, lon_max = 359, lat_min = -90, lat_max = 90, detail=3, v_scale = 400, 
                     figsize_x = 20, figsize_y = 15, colormap = "GnBu"):
    #make the figure
    fig = plt.figure(figsize = (figsize_x, figsize_y))
    ax = plt.axes(projection = ccrs.PlateCarree(central_longitude = 0))
    ax.coastlines()
    ax.add_feature(cartopy.feature.LAKES, alpha=1)
    ax.add_feature(cartopy.feature.RIVERS, alpha=1)
    
    lat1 = em.find_closest_val(lat_min, lat)
    lat2 = em.find_closest_val(lat_max, lat)
    
    #set labels and axes up
    ax.set_extent((lon_min, lon_max, lat_min, lat_max))
    ax.set_xticks(lon[math.ceil(lon_min / 10) * 10:lon_max][::10], crs = ccrs.PlateCarree())
    ax.set_yticks(lat[math.ceil(lat1 / 10) * 10:lat2][::10], crs = ccrs.PlateCarree())
    plt.xlabel('lon')
    plt.ylabel('lat')
    plt.title(title)
    
    color = np.hypot(x_data[lat1:lat2, lon_min:lon_max][::detail, ::detail], 
                     y_data[lat1:lat2, lon_min:lon_max][::detail, ::detail])
    v_field = plt.quiver(lon[lon_min:lon_max][::detail], 
                          lat[lat1:lat2][::detail],
                        x_data[lat1:lat2, lon_min:lon_max][::detail, ::detail],
                        y_data[lat1:lat2, lon_min:lon_max][::detail, ::detail], color, cmap=colormap, scale = v_scale)
    scalebar = plt.colorbar(v_field)
    scalebar.set_label(scale_title)
    
    
#This is a basic method to plot a given collection of vector data (with the x and y componenets given separately) along with associated
#lat and lon values. Optional parameters to limit bounds of visualization, and, since these plot can get
#messy, how many degrees should separate the vectors. This plots the data as unit vectors colored corresponding to their magnitude. 
def plot_nvector_data(lon, lat, x_data, y_data, title, scale_title, 
                     lon_min = 0, lon_max = 359, lat_min = -90, lat_max = 90, detail=1, 
                     figsize_x = 20, figsize_y = 15, colormap = "GnBu"):
    fig = plt.figure(figsize = (figsize_x, figsize_y))
    ax = plt.axes(projection = ccrs.PlateCarree(central_longitude = 0))
    ax.coastlines()
    ax.add_feature(cartopy.feature.LAKES, alpha=1)
    ax.add_feature(cartopy.feature.RIVERS, alpha=1)
    
    lat1 = em.find_closest_val(lat_min, lat)
    lat2 = em.find_closest_val(lat_max, lat)
    
    ax.set_extent((lon_min, lon_max, lat_min, lat_max))
    ax.set_xticks(lon[math.ceil(lon_min / 10) * 10:lon_max][::10], crs = ccrs.PlateCarree())
    ax.set_yticks(lat[math.ceil(lat1 / 10) * 10:lat2][::10], crs = ccrs.PlateCarree())
    plt.xlabel('lon')
    plt.ylabel('lat')
    plt.title(title)
    
    color = np.hypot(x_data[lat1:lat2, lon_min:lon_max][::detail, ::detail], 
                     y_data[lat1:lat2, lon_min:lon_max][::detail, ::detail])
    v_field = plt.quiver(lon[lon_min:lon_max][::detail], 
                          lat[lat1:lat2][::detail],
                        np.divide(x_data[lat1:lat2, lon_min:lon_max][::detail, ::detail], color),
                        np.divide(y_data[lat1:lat2, lon_min:lon_max][::detail, ::detail], color), 
                         color, cmap=colormap, scale = 125)
    scalebar = plt.colorbar(v_field)
    scalebar.set_label(scale_title)
    
    