#!/usr/bin/env python
# coding: utf-8

# In[1]:


## for data
import numpy as np
import pandas as pd


# In[2]:


## for plotting
import matplotlib.pyplot as plt
import seaborn as sns


# In[3]:


## for geospatial
import folium
import geopy

import os
import io
from PIL import Image

# In[4]:


## for machine learning
from sklearn import preprocessing, cluster
import scipy
## for deep learning
import minisom


dtf = pd.read_csv('Book1.csv')
# dtf.head()


def price_range():
     x = "price_range"
     ax = dtf[x].value_counts().sort_values().plot(kind="barh")
     totals = []
     for i in ax.patches:
      totals.append(i.get_width())
     total = sum(totals)
     for i in ax.patches:
          ax.text(i.get_width()+.3, i.get_y()+.20, 
          str(round((i.get_width()/total)*100, 2))+'%', 
          fontsize=10, color='black')
     ax.grid(axis="x")
     plt.suptitle(x, fontsize=20)
     # plt.show()
     plt.savefig('F:\SLIIT\Distance\images\graph.png')
     return "img/graph.png"

def get_location():  
     name_en = 'Colombo'
     ## get location
     locator = geopy.geocoders.Nominatim(user_agent="MyCoder")
     location = locator.geocode(name_en)
     print(location)
     ## keep latitude and longitude only
     location = [location.latitude, location.longitude]
     print("[latitude, longitude]:", location)
     return location

def price_priority_map(folder, location):
     if not os.path.exists(folder):
          os.makedirs(folder)
    
     x, y = "latitude", "longitude"
     color = "price_range"
     size = "district_id"
     popup = "name_en"
     data = dtf.copy()

     ## create color column
     lst_colors=["red","green","orange"]
     lst_elements = sorted(list(dtf[color].unique()))
     data["color"] = data[color].apply(lambda x: 
                    lst_colors[lst_elements.index(x)])
     ## create size column (scaled)
     scaler = preprocessing.MinMaxScaler(feature_range=(3,15))
     data["size"] = scaler.fit_transform(
                    data[size].values.reshape(-1,1)).reshape(-1)

     ## initialize the map with the starting location
     map_ = folium.Map(location=location, tiles="cartodbpositron",
                    zoom_start=11)
     ## add points
     data.apply(lambda row: folium.CircleMarker(
               location=[row[x],row[y]], popup=row[popup],
               color=row["color"], fill=True,
               radius=row["size"]).add_to(map_), axis=1)
     ## add html legend
     legend_html = """<div style="position:fixed; bottom:10px; left:10px; border:2px solid black; z-index:9999; font-size:14px;">&nbsp;<b>"""+color+""":</b><br>"""
     for i in lst_elements:
          legend_html = legend_html+"""&nbsp;<i class="fa fa-circle 
          fa-1x" style="color:"""+lst_colors[lst_elements.index(i)]+"""">
          </i>&nbsp;"""+str(i)+"""<br>"""
     legend_html = legend_html+"""</div>"""
     map_.get_root().html.add_child(folium.Element(legend_html))

     ## plot the map
     # img_data = map_._to_png(5)
     # img = Image.open(io.BytesIO(img_data))
     # img.save(os.path.join(folder, 'map.png'))

     # plt.savefig(os.path.join(folder, 'map.png'))
     map_.save(os.path.join(folder, 'map.html'))
     return "img/map.html"

def kmean_cluster():
     k = 7
     model = cluster.KMeans(n_clusters=k, init='k-means++')
     X = dtf[["latitude","longitude"]]
     ## clustering
     dtf_X =X.copy()
     dtf_X["cluster"] = model.fit_predict(X)
     ## find real centroids
     closest, distances = scipy.cluster.vq.vq(model.cluster_centers_, dtf_X.drop('cluster', axis=1).values)
     dtf_X["centroids"] = 0
     for i in closest:
          dtf_X["centroids"].iloc[i] = 1
     ## add clustering info to the original dataset
     dtf[["cluster","centroids"]] = dtf_X[["cluster","centroids"]]
     names = dtf.sample(7)["name_en"]
     return names.values

def best_market_place(folder, location):
     if not os.path.exists(folder):
          os.makedirs(folder)
     x, y = "latitude", "longitude"
     color = "cluster"
     size = "district_id"
     popup = "name_en"
     marker = "centroids"
     data = dtf.copy()
     ## create color column
     lst_elements = sorted(list(dtf[color].unique()))
     
     lst_colors = ['#%06X' % np.random.randint(i, 0xFFFFFF) for i in range(len(lst_elements))] 
     data["color"] = data[color].apply(lambda x: 
                    lst_colors[lst_elements.index(x)])
     ## create size column (scaled)
     scaler = preprocessing.MinMaxScaler(feature_range=(3,15))
     data["size"] = scaler.fit_transform(
                    data[size].values.reshape(-1,1)).reshape(-1)
     ## initialize the map with the starting location
     map_ = folium.Map(location=location, tiles="cartodbpositron",
                    zoom_start=11)
     ## add points
     data.apply(lambda row: folium.CircleMarker(
               location=[row[x],row[y]], popup=row[popup],
               color=row["color"], fill=True,
               radius=row["size"]).add_to(map_), axis=1)
     ## add html legend
     legend_html = """<div style="position:fixed; bottom:10px; left:10px; border:2px solid black; z-index:9999; font-size:14px;">&nbsp;<b>"""+color+""":</b><br>"""
     for i in lst_elements:
          legend_html = legend_html+"""&nbsp;<i class="fa fa-circle 
          fa-1x" style="color:"""+lst_colors[lst_elements.index(i)]+"""">
          </i>&nbsp;"""+str(i)+"""<br>"""
     legend_html = legend_html+"""</div>"""
     map_.get_root().html.add_child(folium.Element(legend_html))
     ## add centroids marker
     lst_elements = sorted(list(dtf[marker].unique()))
     data[data[marker]==1].apply(lambda row: 
               folium.Marker(location=[row[x],row[y]], 
               popup=row[marker], draggable=False,          
               icon=folium.Icon(color="black")).add_to(map_), axis=1)
     ## plot the map
     # map_
     map_.save(os.path.join(folder, 'marketplace.html'))
     return "img/marketplace.html"