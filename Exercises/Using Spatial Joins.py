import transportation_tutorials as tt
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import matplotlib.pyplot as plt

maz = gpd.read_file(tt.data('SERPM8-MAZSHAPE'))
taz = gpd.read_file(tt.data('SERPM8-TAZSHAPE'))
#print(maz.info())
#print(taz.info())

maz_points = maz.copy()   # copy

# Q1: Within the SERPM 7 region, what TAZ has the largest number of MAZs within its boundary? How many does it have?
# Every piece of data has a center point
maz_points.geometry = maz_points.apply(lambda x: Point(x.POINT_X, x.POINT_Y), axis=1)
# join
taz_maz = gpd.sjoin(maz_points, taz, how='left', op='within')

taz_maz_counts = taz_maz.groupby(['TAZ_REG'])['MAZ'].count()

idx = taz_maz_counts.idxmax()
print(idx)

idx_max_1 = taz_maz_counts.max()
print(idx_max_1)

idx_max_2 = taz_maz_counts.loc[idx]
print(idx_max_2)


# Q2: Generate a map of the MAZ boundaries within this TAZ, including context as necessary from OpenStreetMaps. What features of this TAZ helped lead to the large number of MAZ’s?
print(taz_maz.info())

taz_maz.geometry = maz.geometry
ax = taz_maz.query("TAZ_REG == 466").plot(color='none',edgecolor='red')
tt.mapping.add_basemap(ax, zoom=14, crs=maz.crs)
plt.show()
