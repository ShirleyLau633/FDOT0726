import transportation_tutorials as tt
import numpy as np
import pandas as pd
import geopandas as gpd
import folium
from matplotlib import pyplot as plt
import webbrowser as wb


xmin = 905712
ymin = 905343
taz = gpd.read_file(tt.data('SERPM8-TAZSHAPE')).cx[xmin:, ymin:].to_crs(epsg=4326)
maz = gpd.read_file(tt.data('SERPM8-MAZSHAPE')).cx[xmin:, ymin:].to_crs(epsg=4326)
center = (26.9198, -80.1121)    # regular lat-lon

m = folium.Map(center, zoom_start = 12)
folium.GeoJson(taz).add_to(m)
# 存储动态地图，并且显示
m.save('f1.html')
wb.open('f1.html')  # 运行一下"f1.html"文件即可

# 备用Tiles
m = folium.Map(center, zoom_start = 12, tiles='CartoDB positron',)

# 地图标记
m = folium.Map(
    location=[26.8645, -80.1040],
    tiles='Stamen Toner',
    zoom_start=13
)

# 标记一个实心圆
folium.CircleMarker(
    radius=20, # in pixels, regardless of map zoom
    location=[26.8853, -80.1140],
    popup='Scripps Research Institute',
    color='blue',  # 圈的颜色
    fill=True,
).add_to(m)

# 标记一个空心圆
folium.Circle(
    radius=300, # in meters, scales with map zoom
    location=[26.8484, -80.0855],
    popup='The Gardens Mall',
    color='crimson',
    fill=True,
    fill_color='pink'   # 填充颜色
).add_to(m)

# 把副标的样式进行修改
folium.Marker(
    [26.677037, -80.037117],
    popup='Mar-a-Lago Club',
    icon=folium.Icon(color='red', icon='info-sign'),
).add_to(m)


mazd = pd.read_csv(tt.data('SERPM8-MAZDATA', '*.csv'))
maz1 = maz.merge(mazd, how='left', left_on='MAZ', right_on='mgra')
maz1.index = maz1.MAZ

from branca import colormap

colormapper = colormap.linear.YlGn_09.scale(
    maz1.PopDen.min(),
    maz1.PopDen.max(),
)
colormapper.caption = "Population Density"


def colormapper_with_zero(x):
    if x==0:
        return "#faded1"
    else:
        return colormapper(x)


m = folium.Map(center, zoom_start = 12)
gj = folium.GeoJson(
    maz1,
    style_function=lambda feature: {
        'fillColor': colormapper_with_zero(feature['properties']['PopDen']),
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.8,
    },
    highlight_function=lambda feature: {
        'color': 'blue',
        'weight': 4,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['TAZ', 'MAZ', 'PopDen'],
    ),
).add_to(m)
colormapper.add_to(m)
m.save('f2.html')
wb.open('f2.html')  # 运行一下"f1.html"文件即可


