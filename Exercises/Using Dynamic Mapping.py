import transportation_tutorials as tt
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import folium
from shapely.geometry import Polygon

maz = gpd.read_file(tt.data('SERPM8-MAZSHAPE'))
maz_data = pd.read_csv(tt.data('SERPM8-MAZDATA', '*.csv'))
print(maz.crs)
# maz = maz.to_crs(epsg = 4326)
print(maz.info())
print(maz_data.info())

maz_data_1 = maz_data[['PopDen', 'emp_total']]
print(maz_data_1)

maz_data_1 = maz_data_1.astype(float)
maz_1 = maz.merge(maz_data_1, how='left', left_on='MAZ', right_on='PopDen')
print(maz_1)

maz_1 = maz_1.sort_values(by = 'PopDen', ascending = False).head(5)
print(maz_1.info())

# From the Solution, how to change the data from CRS format to folium

import pyproj
    # 读取经纬度
input_Proj = pyproj.Proj(init="EPSG:2236", preserve_units=True)  # 定义数据地理坐标系
output_Proj = pyproj.Proj(init="EPSG:4326")  # 定义转换投影坐标系

point_x = []
point_y = []

for index, row in maz_1.iterrows():
    # print(row.POINT_X)
    coor = pyproj.transform(input_Proj, output_Proj, row.POINT_X, row.POINT_Y)
    point_x.append(coor[0])
    point_y.append(coor[1])
# print(point_x)
# print(point_y)

maz_1['POINT_X_'] = point_x
print(maz_1['POINT_X_'])
maz_1['POINT_Y_'] = point_y

center_x = maz_1['POINT_X_'].mean()
certer_y = maz_1['POINT_Y_'].mean()
center = (certer_y, center_x)
print(center)

m = folium.Map(center, zoom_start = 12)
m = folium.GeoJson(maz_1).add_to(m)

for index, row in maz_1.iterrows():
    popup = 'PopDen:{}, EMP:{}'.format(row.PopDen, row.emp_total),
    folium.Marker(
        location=[row.POINT_Y_, row.POINT_X_],
        popup=popup,
        tooltip='MAZ ID:{}'.format(row.MAZ),
        color='blue',  # 圈的颜色
        fill=True,
    ).add_to(m)

gj = folium.GeoJson(
    maz_1,
    highlight_function=lambda feature: {
        'color': 'blue',
        'weight': 4,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['MAZ', 'PopDen', 'emp_total'],
    ),
).add_to(m)

m.save('maz_2.html')
import webbrowser as wb
wb.open('maz_2.html')  # 运行一下".html"文件即可

# Using folium, create a dynamic map and place markers on the centroids of the five MAZ’s with the highest population density MAZs. Use popup text on markers to show population density and total employment information for each of those MAZs. By clicking the markers, you should be able to answer the following questions:

# Where is the highest population density?

# What is the total employment in the MAZ that has the highest population density?