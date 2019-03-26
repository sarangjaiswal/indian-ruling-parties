# import library
import geopandas as gpd
import os
import folium
import pandas as pd

# get current directory path
cur_dir = os.path.dirname(os.path.realpath(__file__))

# target path to save map
map_path = os.path.join('maps', 'ruling_political_party_in_india.html')

# read shape files with geopandas
gdf = gpd.read_file(cur_dir + '/data/StateBoundary/StateBoundary.shp')

# read csv file with pandas
df = pd.read_csv(open(os.path.join('data', 'IndianPoliticalPartyList.csv')))

# create a folium map object and point to a location & zoom start.
# http://geojson.io/#map=5/22.573/74.751
m = folium.Map(location=[22.573, 74.751], zoom_start=5)


# function to add data to folium map
def add_data_to_map(color, state, year):
    q = f"state=='{state}'"
    feature_group = folium.FeatureGroup(name=year)
    folium.Choropleth(
        geo_data=gdf.query(q),
        fill_color=color,
        fill_opacity=1,
        line_color='black',
        line_weight=1,
        line_opacity=0.5,
        highlight=True
    ).add_to(feature_group)

    feature_group.add_to(m)


# iterate the pandas data frame
for index, row in df.iterrows():
    add_data_to_map(row['hex_code'], row['state_name'], 2019)

# add layer to map
folium.LayerControl().add_to(m)

# save map to specified location
m.save(map_path)
