import transportation_tutorials as tt
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import osmnx as ox
from shapely.geometry import Polygon

'''
maz = gpd.read_file(tt.data('SERPM8-MAZSHAPE'))
# print(maz.crs)
# maz1 = maz.to_crs(epsg=4326)
# print(maz1.crs)
# maz1.plot(figsize = (10,10))
# print(maz1.head())
import pyproj
    # 读取经纬度
input_Proj = pyproj.Proj(init="EPSG:2236", preserve_units=True)  # 定义数据地理坐标系
output_Proj = pyproj.Proj(init="EPSG:4326")  # 定义转换投影坐标系

point_x = []
point_y = []

for index, row in maz.iterrows():
    # print(row.POINT_X)
    coor = pyproj.transform(input_Proj, output_Proj, row.POINT_X, row.POINT_Y)
    point_x.append(coor[0])
    point_y.append(coor[1])
# print(point_x)
# print(point_y)

maz['POINT_X_'] = point_x
print(maz['POINT_X_'])
maz['POINT_Y_'] = point_y
maz.plot(figsize = (10,10))
plt.show()

'''
clipper_poly = Polygon([
    (-80.170862, 26.328588),
    (-80.170158, 26.273494),
    (-80.113007, 26.274882),
    (-80.104592, 26.293503),
    (-80.072967, 26.293790),
    (-80.070111, 26.329349)
])
# city = ox.gdf_from_place('Jupiter, Florida, USA')
# why the 'Deerfield Beach' is a point？
city = ox.gdf_from_place('Deerfield Beach, Florida, USA')
ax = city.plot()
lines = ax.plot(*clipper_poly.exterior.xy, color = 'r')
tt.mapping.add_basemap(ax, zoom=13, epsg=4326)
plt.show()

# Use OSMnx to download the boundaries for Deerfield Beach, and generate an image that compares the city to the indicated study area polygon. Are there any areas in the city of Deerfield Beach that are outside the designated studay area, and if so, is this concerning? (Hint: use the ``add_basemap`` function from the ``transportation_tutorials.mapping`` package to add context to your map.)

# How many MAZs are there that are located completely inside the study area? Generate a static map of only these MAZ’s. (Hint: Please make sure to use appropriate Coordinate Reference Systems (CRS) in your analysis.)


# How many MAZs are at least partially inside the study area? Generate a static map of these MAZ’s, including the full area of any MAZ that is at least partially contained in the study area.