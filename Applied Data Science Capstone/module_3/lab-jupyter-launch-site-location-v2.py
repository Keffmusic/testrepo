# Databricks notebook source
# MAGIC %md
# MAGIC <p style="text-align:center">
# MAGIC     <a href="https://skills.network" target="_blank">
# MAGIC     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/assets/logos/SN_web_lightmode.png" width="200" alt="Skills Network Logo">
# MAGIC     </a>
# MAGIC </p>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # **Launch Sites Locations Analysis with Folium**
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Estimated time needed: **40** minutes
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC The launch success rate may depend on many factors such as payload mass, orbit type, and so on. It may also depend on the location and proximities of a launch site, i.e., the initial position of rocket trajectories. Finding an optimal location for building a launch site certainly involves many factors and hopefully we could discover some of the factors by analyzing the existing launch site locations.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC In the previous exploratory data analysis labs, you have visualized the SpaceX launch dataset using `matplotlib` and `seaborn` and discovered some preliminary correlations between the launch site and success rates. In this lab, you will be performing more interactive visual analytics using `Folium`.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Objectives
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC This lab contains the following tasks:
# MAGIC - **TASK 1:** Mark all launch sites on a map
# MAGIC - **TASK 2:** Mark the success/failed launches for each site on the map
# MAGIC - **TASK 3:** Calculate the distances between a launch site to its proximities
# MAGIC
# MAGIC After completed the above tasks, you should be able to find some geographical patterns about launch sites.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Let's first import required Python packages for this lab:
# MAGIC

# COMMAND ----------

!pip3 install folium
!pip3 install wget
#!pip3 install pandas

# COMMAND ----------

import folium
import wget
import pandas as pd

# COMMAND ----------

# Import folium MarkerCluster plugin
from folium.plugins import MarkerCluster
# Import folium MousePosition plugin
from folium.plugins import MousePosition
# Import folium DivIcon plugin
from folium.features import DivIcon

# COMMAND ----------

# MAGIC %md
# MAGIC If you need to refresh your memory about folium, you may download and refer to this previous folium lab:
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC [Generating Maps with Python](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/DV0101EN-3-5-1-Generating-Maps-in-Python-py-v2.0.ipynb)
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 1: Mark all launch sites on a map
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC First, let's try to add each site's location on a map using site's latitude and longitude coordinates
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC The following dataset with the name `spacex_launch_geo.csv` is an augmented dataset with latitude and longitude added for each site. 
# MAGIC

# COMMAND ----------

# Download and read the `spacex_launch_geo.csv`
spacex_csv_file = wget.download('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv')
spacex_df=pd.read_csv(spacex_csv_file)

# COMMAND ----------

# MAGIC %md
# MAGIC Now, you can take a look at what are the coordinates for each site.
# MAGIC

# COMMAND ----------

# Select relevant sub-columns: `Launch Site`, `Lat(Latitude)`, `Long(Longitude)`, `class`
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]
launch_sites_df

# COMMAND ----------

# MAGIC %md
# MAGIC Above coordinates are just plain numbers that can not give you any intuitive insights about where are those launch sites. If you are very good at geography, you can interpret those numbers directly in your mind. If not, that's fine too. Let's visualize those locations by pinning them on a map.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC We first need to create a folium `Map` object, with an initial center location to be NASA Johnson Space Center at Houston, Texas.
# MAGIC

# COMMAND ----------

# Start location is NASA Johnson Space Center
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=10)

# COMMAND ----------

# MAGIC %md
# MAGIC We could use `folium.Circle` to add a highlighted circle area with a text label on a specific coordinate. For example, 
# MAGIC

# COMMAND ----------

# Create a blue circle at NASA Johnson Space Center's coordinate with a popup label showing its name
circle = folium.Circle(nasa_coordinate, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('NASA Johnson Space Center'))
# Create a blue circle at NASA Johnson Space Center's coordinate with a icon showing its name
marker = folium.map.Marker(
    nasa_coordinate,
    # Create an icon as a text label
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'NASA JSC',
        )
    )
site_map.add_child(circle)
site_map.add_child(marker)

# COMMAND ----------

# MAGIC %md
# MAGIC and you should find a small yellow circle near the city of Houston and you can zoom-in to see a larger circle. 
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Now, let's add a circle for each launch site in data frame `launch_sites`
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC _TODO:_  Create and add `folium.Circle` and `folium.Marker` for each launch site on the site map
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC An example of folium.Circle:
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC `folium.Circle(coordinate, radius=1000, color='#000000', fill=True).add_child(folium.Popup(...))`
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC An example of folium.Marker:
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC `folium.map.Marker(coordinate, icon=DivIcon(icon_size=(20,20),icon_anchor=(0,0), html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'label', ))`
# MAGIC

# COMMAND ----------

# Initial the map
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)

# Iterate over each launch site
for index, site in launch_sites_df.iterrows():
    # Get coordinates for this site
    coordinate = [site['Lat'], site['Long']]
    site_name = site['Launch Site']
    
    # Create circle
    circle = folium.Circle(
        coordinate, 
        radius=1000, 
        color='#000000', 
        fill=True
    ).add_child(folium.Popup(site_name))
    
    # Create marker
    marker = folium.map.Marker(
        coordinate,
        icon=DivIcon(
            icon_size=(20,20),
            icon_anchor=(0,0),
            html='<div style="font-size: 12; color:#000000;"><b>%s</b></div>' % site_name,
        )
    )
    
    # Add to map
    site_map.add_child(circle)
    site_map.add_child(marker)

site_map

# COMMAND ----------

# MAGIC %md
# MAGIC The generated map with marked launch sites should look similar to the following:
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC <center>
# MAGIC     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/images/launch_site_markers.png">
# MAGIC </center>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Now, you can explore the map by zoom-in/out the marked areas
# MAGIC , and try to answer the following questions:
# MAGIC - Are all launch sites in proximity to the Equator line?
# MAGIC - Are all launch sites in very close proximity to the coast?
# MAGIC
# MAGIC Also please try to explain your findings.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # Task 2: Mark the success/failed launches for each site on the map
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Next, let's try to enhance the map by adding the launch outcomes for each site, and see which sites have high success rates.
# MAGIC Recall that data frame spacex_df has detailed launch records, and the `class` column indicates if this launch was successful or not
# MAGIC

# COMMAND ----------

spacex_df.tail(10)

# COMMAND ----------

# MAGIC %md
# MAGIC Next, let's create markers for all launch records. 
# MAGIC If a launch was successful `(class=1)`, then we use a green marker and if a launch was failed, we use a red marker `(class=0)`
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Note that a launch only happens in one of the four launch sites, which means many launch records will have the exact same coordinate. Marker clusters can be a good way to simplify a map containing many markers having the same coordinate.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Let's first create a `MarkerCluster` object
# MAGIC

# COMMAND ----------

marker_cluster = MarkerCluster()

# COMMAND ----------

# MAGIC %md
# MAGIC _TODO:_ Create a new column in `launch_sites` dataframe called `marker_color` to store the marker colors based on the `class` value
# MAGIC

# COMMAND ----------

# Apply a function to check the value of `class` column
# If class=1, marker_color value will be green
# If class=0, marker_color value will be red

# Function to assign color to launch outcome
def assign_marker_color(launch_outcome):
    if launch_outcome == 1:
        return 'green'
    else:
        return 'red'
    
spacex_df['marker_color'] = spacex_df['class'].apply(assign_marker_color)
spacex_df.tail(10)

# COMMAND ----------

# MAGIC %md
# MAGIC _TODO:_ For each launch result in `spacex_df` data frame, add a `folium.Marker` to `marker_cluster`
# MAGIC

# COMMAND ----------

# Add marker_cluster to current site_map
site_map.add_child(marker_cluster)

# for each row in spacex_df data frame
# create a Marker object with its coordinate
# and customize the Marker's icon property to indicate if this launch was successed or failed, 
# e.g., icon=folium.Icon(color='white', icon_color=row['marker_color']
for index, record in spacex_df.iterrows():
    # Create and add a Marker cluster to the site map
    marker = folium.Marker(
        location=[record['Lat'], record['Long']],
        icon=folium.Icon(color='white', icon_color=record['marker_color']),
        popup=record['Launch Site'],
        tooltip=record['Launch Site']
    )
    marker_cluster.add_child(marker)
site_map

# COMMAND ----------

# MAGIC %md
# MAGIC Your updated map may look like the following screenshots:
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC <center>
# MAGIC     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/images/launch_site_marker_cluster.png">
# MAGIC </center>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC <center>
# MAGIC     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/images/launch_site_marker_cluster_zoomed.png">
# MAGIC </center>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC From the color-labeled markers in marker clusters, you should be able to easily identify which launch sites have relatively high success rates.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # TASK 3: Calculate the distances between a launch site to its proximities
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Next, we need to explore and analyze the proximities of launch sites.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Let's first add a `MousePosition` on the map to get coordinate for a mouse over a point on the map. As such, while you are exploring the map, you can easily find the coordinates of any points of interests (such as railway)
# MAGIC

# COMMAND ----------

# Add Mouse Position to get the coordinate (Lat, Long) for a mouse over on the map
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)

site_map.add_child(mouse_position)
site_map

# COMMAND ----------

# MAGIC %md
# MAGIC Now zoom in to a launch site and explore its proximity to see if you can easily find any railway, highway, coastline, etc. Move your mouse to these points and mark down their coordinates (shown on the top-left) in order to the distance to the launch site.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC You can calculate the distance between two points on the map based on their `Lat` and `Long` values using the following method:
# MAGIC

# COMMAND ----------

from math import sin, cos, sqrt, atan2, radians

def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

# COMMAND ----------

# MAGIC %md
# MAGIC _TODO:_ Mark down a point on the closest coastline using MousePosition and calculate the distance between the coastline point and the launch site.
# MAGIC

# COMMAND ----------

# Select KSC LC-39A launch site for analysis
launch_site_lat = 28.573255
launch_site_lon = -80.649266

# Find coordinate of the closest coastline
# Coordinates obtained using MousePosition on the map
coastline_lat = 28.56367
coastline_lon = -80.57163

# Calculate distance
distance_coastline = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)
print(f"Distance to coastline: {distance_coastline:.2f} KM")

# COMMAND ----------

# MAGIC %md
# MAGIC _TODO:_ After obtained its coordinate, create a `folium.Marker` to show the distance
# MAGIC

# COMMAND ----------

# Create and add a folium.Marker on the selected closest coastline point
coastline_coordinate = [coastline_lat, coastline_lon]

distance_marker = folium.Marker(
    coastline_coordinate,
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_coastline),
    )
)

site_map.add_child(distance_marker)

# COMMAND ----------

# MAGIC %md
# MAGIC _TODO:_ Draw a `PolyLine` between a launch site to the selected coastline point
# MAGIC

# COMMAND ----------

# Create a PolyLine between launch site and coastline
launch_site_coordinate = [launch_site_lat, launch_site_lon]
coordinates = [launch_site_coordinate, coastline_coordinate]

lines = folium.PolyLine(locations=coordinates, weight=1, color='blue')
site_map.add_child(lines)
site_map

# COMMAND ----------

# MAGIC %md
# MAGIC Your updated map with distance line should look like the following screenshot:
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC <center>
# MAGIC     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/images/launch_site_marker_distance.png">
# MAGIC </center>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC _TODO:_ Similarly, you can draw a line betwee a launch site to its closest city, railway, highway, etc. You need to use `MousePosition` to find the their coordinates on the map first
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC A railway map symbol may look like this:
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC <center>
# MAGIC     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/images/railway.png">
# MAGIC </center>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC A highway map symbol may look like this:
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC <center>
# MAGIC     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/images/highway.png">
# MAGIC </center>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC A city map symbol may look like this:
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC <center>
# MAGIC     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/images/city.png">
# MAGIC </center>
# MAGIC

# COMMAND ----------

# Find coordinates for closest city, railway, and highway
# Coordinates obtained using MousePosition on the map

# Closest city (Titusville)
city_lat = 28.6122
city_lon = -80.8077
distance_city = calculate_distance(launch_site_lat, launch_site_lon, city_lat, city_lon)

# Closest railway
railway_lat = 28.5726
railway_lon = -80.6501
distance_railway = calculate_distance(launch_site_lat, launch_site_lon, railway_lat, railway_lon)

# Closest highway (US-1)
highway_lat = 28.5729
highway_lon = -80.6485
distance_highway = calculate_distance(launch_site_lat, launch_site_lon, highway_lat, highway_lon)

print(f"Distance to city: {distance_city:.2f} KM")
print(f"Distance to railway: {distance_railway:.2f} KM")
print(f"Distance to highway: {distance_highway:.2f} KM")

# Create markers and lines for each proximity
proximities = [
    {'name': 'City', 'lat': city_lat, 'lon': city_lon, 'distance': distance_city, 'color': 'green'},
    {'name': 'Railway', 'lat': railway_lat, 'lon': railway_lon, 'distance': distance_railway, 'color': 'purple'},
    {'name': 'Highway', 'lat': highway_lat, 'lon': highway_lon, 'distance': distance_highway, 'color': 'red'}
]

for proximity in proximities:
    # Create marker with distance
    coordinate = [proximity['lat'], proximity['lon']]
    
    marker = folium.Marker(
        coordinate,
        icon=DivIcon(
            icon_size=(20,20),
            icon_anchor=(0,0),
            html='<div style="font-size: 12; color:#d35400;"><b>%s: %s</b></div>' % (proximity['name'], "{:10.2f} KM".format(proximity['distance'])),
        )
    )
    site_map.add_child(marker)
    
    # Draw line between launch site and proximity point
    line_coords = [launch_site_coordinate, coordinate]
    line = folium.PolyLine(locations=line_coords, weight=1, color=proximity['color'])
    site_map.add_child(line)

site_map

# COMMAND ----------

# MAGIC %md
# MAGIC After you plot distance lines to the proximities, you can answer the following questions easily:
# MAGIC - Are launch sites in close proximity to railways?
# MAGIC - Are launch sites in close proximity to highways?
# MAGIC - Are launch sites in close proximity to coastline?
# MAGIC - Do launch sites keep certain distance away from cities?
# MAGIC
# MAGIC Also please try to explain your findings.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # Next Steps:
# MAGIC
# MAGIC Now you have discovered many interesting insights related to the launch sites' location using folium, in a very interactive way. Next, you will need to build a dashboard using Ploty Dash on detailed launch records.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Authors
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC [Yan Luo](https://www.linkedin.com/in/yan-luo-96288783/)
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Other Contributors
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Joseph Santarcangelo
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Change Log
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC |Date (YYYY-MM-DD)|Version|Changed By|Change Description|
# MAGIC |-|-|-|-|
# MAGIC |2021-05-26|1.0|Yan|Created the initial version|
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Copyright © 2021 IBM Corporation. All rights reserved.
# MAGIC