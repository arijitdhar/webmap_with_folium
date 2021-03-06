__author__ = '220152'

import folium
import pandas
import os

# load the data
data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])


def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

html = """<h4>Volcano information:</h4>
Name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

# Create a base map
my_map = folium.Map([38.53, -99.09], zoom_start=10, tiles="Stamen Terrain")

# Add a point marker in the map
# Way 1
# folium.Marker(location=[22.53, 88.34], popup="<i>Hi, I am a Marker</i>", icon=folium.Icon(color='blue')).add_to(my_map)

# Way 2
#my_map.add_child(folium.Marker(location=[22.53, 88.34], popup="<i>Hi, I am a Marker</i>", icon=folium.Icon(color='blue')))

# Way 3. Create a FeatureGroup that can be used to control layers as a whole
volcano_feature_group = folium.FeatureGroup(name="Volcanoes")
# Now add the Marker child to the FeatureGroup

# Zip function iterates more than 1 list and stores ith elements
# from each list in the individual variables for each list as defined
for lt, ln, el, nm in zip(lat, lon, elev, name):
    # Create an iframe for popup for each volcano
    iframe = folium.IFrame(html=html  % (nm, nm, str(el)), width=200, height=100)
    # my_fg.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe), icon=folium.Icon(color=color_producer(el))))
    volcano_feature_group.add_child(folium.CircleMarker(location=[lt, ln], popup=folium.Popup(iframe), fill_color=color_producer(el),
                                        radius=6, color='grey', fill_opacity=0.7))

population_feature_group = folium.FeatureGroup(name="Population")
# Add GeoJsonData
population_feature_group.add_child(folium.GeoJson(data=open("world.json", 'r', encoding='utf-8-sig').read(), style_function=lambda x: {
'fillColor': 'green' if x['properties']['POP2005'] < 10000000 else 'orange' if 10000000 <= x['properties'][
    'POP2005'] < 20000000 else 'red'}))

# Now add the FeatureGroup to the Map
my_map.add_child(volcano_feature_group)
my_map.add_child(population_feature_group)

# Always add LayerControl in the map after the FeatureGroup(s) have been added in the map
my_map.add_child(folium.LayerControl())

my_map.save("MyMap.html")

print("Generated MyMap.html using Folium at:{}!".format(os.path.join(os.getcwd(), "MyMap.html")))



