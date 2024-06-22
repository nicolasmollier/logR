import geopandas as gpd

df = gpd.read_file("data/gps/WayLog-GPX-20240604220321.gpx", layer="track_points")
df.columns