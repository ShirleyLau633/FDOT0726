import osmnx as ox
import geopandas as gpd
import networkx as nx
import numpy as np
import transportation_tutorials as tt
from matplotlib import pyplot as plt


# Municipal Boundaries
#选取Jupiter Florida作为例子
city = ox.gdf_from_place('Jupiter, Florida, USA')
# ax = city.plot()


official_shp = tt.download_zipfile("http://www.jupiter.fl.us/DocumentCenter/View/10297")
city_official = gpd.read_file(official_shp)
# ax = city_official.plot()
# ax = city.plot(ax=ax, edgecolor='r')

#print(city.crs, city_official.crs)

# city.to_crs(epsg=2881, inplace=True)

#print(city.crs, city_official.crs)
# ax = city_official.plot()
# ax = city.plot(ax=ax, edgecolor='r')
transparent = (0,0,0,0)
ax = city_official.plot(edgecolor='blue', facecolor=transparent)
ax = city.plot(ax=ax, edgecolor='red', facecolor=transparent)
# ax = tt.mapping.add_basemap(ax=ax, zoom=14, epsg=2881, axis='off', figsize=(10,10))

# Street Network（路网）
# 获取路网
jupiter_streets = ox.graph_from_place('Jupiter, Florida, USA')
# 画出路网
fig, ax = ox.plot_graph(jupiter_streets, show=False, close=False)
ax = city.to_crs(epsg=4326).plot(ax=ax, edgecolor='red', facecolor=transparent)
# 扩大路网区域，确定研究范围
study_area = city.buffer(20000).envelope.to_crs(epsg=4326)

west, south, east, north = study_area.total_bounds
streets = ox.graph_from_bbox(north, south, east, west, simplify=False)

fig, ax = ox.plot_graph(streets, show=False, close=False)
ax = city.to_crs(epsg=4326).plot(ax=ax, edgecolor='red', facecolor=transparent, zorder=2)
plt.show()