import transportation_tutorials as tt
import geopandas as gpd
from matplotlib import pyplot as plt
from shapely.geometry import Polygon

shapefile_filename = tt.data('SERPM8-TAZSHAPE')
taz = gpd.read_file(shapefile_filename)

ax = taz.plot()  #画shapefile的图


# Selection by Rectangular Envelope
xmin = 905712.145924
ymin = 905343.94408855
xmax = 983346.68922847
ymax = 981695.93140023
taz_jupiter = taz.cx[xmin:xmax, ymin:ymax]
ax = taz_jupiter.plot(edgecolor='w')

taz_jupiter2 = taz.cx[xmin:, ymin:]
taz_jupiter2.equals(taz_jupiter)

from shapely.geometry import box
study_area = gpd.GeoDataFrame(geometry=[box(xmin, ymin, xmax, ymax)], crs={'init': 'epsg:2236'})
ax = taz_jupiter.plot(edgecolor='w')
transparent = (0,0,0,0)
ax = study_area.plot(ax=ax, edgecolor='red', facecolor=transparent)

# Selection by Polygon
irregular_polygon = Polygon([
    (973346, 935343),
    (973346, 971695),
    (912812, 973695),
    (915812, 943695),
    (928812, 943695),
    (935712, 905343),
])
ax = taz_jupiter.plot(edgecolor='w')
lines = ax.plot(*irregular_polygon.exterior.xy,color='r')

# 以下语句用于判断哪些区域在与红色框线内，即小区域在大研究区域内
# 用于筛选研究区域内的即有用的数据
taz_jupiter.intersects(irregular_polygon)
# 筛选有用的数据
taz_jupiter_irregular = taz_jupiter[taz_jupiter.intersects(irregular_polygon)]

# 保存一个副本
taz_jupiter_irregular = taz_jupiter_irregular.copy()
ax = taz_jupiter_irregular.plot(edgecolor='w')
lines = ax.plot(*irregular_polygon.exterior.xy, color='r')


'''
# Clipping by Geography

taz_jupiter_clip = gpd.overlay(taz, study_area, how='intersection')

ax = taz_jupiter_clip.plot(edgecolor='w')
transparent = (0, 0, 0, 0)
ax = study_area.plot(ax=ax, edgecolor='red', facecolor=transparent)

taz_jupiter_irregular.geometry = taz_jupiter_irregular.intersection(irregular_polygon)
ax = taz_jupiter_irregular.plot(edgecolor='w')
transparent = (0,0,0,0)
lines = ax.plot(*irregular_polygon.exterior.xy, color='r')


taz_jupiter_clip.geometry = taz_jupiter_clip.intersection(irregular_polygon)
ax = taz_jupiter_clip.plot(edgecolor='w')
transparent = (0,0,0,0)
lines = ax.plot(*irregular_polygon.exterior.xy, color='r')

plt.show()

print(len(taz_jupiter_irregular), len(taz_jupiter_clip))
print(sum(taz_jupiter_clip.geometry.area == 0))
print(sum(taz_jupiter_irregular.geometry.area == 0))
'''
# ------------------------------------------------------------
# Joining by Geography
#读取文件
mazshape_filename = tt.data('SERPM8-MAZSHAPE')
maz = gpd.read_file(mazshape_filename)
print(maz)
#选择研究区域内的数据
maz_jupiter = maz.cx[xmin:xmax, ymin:ymax]
print(maz_jupiter)
#用overlay（）函数join两个数据
maz_taz = gpd.overlay(maz_jupiter, taz_jupiter, how='intersection')
maz_taz = maz_taz.iloc[maz_taz.area.argsort()]
maz_taz = maz_taz.drop_duplicates('MAZ', keep='last')
print(maz_taz)