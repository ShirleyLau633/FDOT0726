# the data provided by the Exercise might be wrong

import transportation_tutorials as tt
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon, Point

maz = gpd.read_file(tt.data('SERPM8-MAZSHAPE'))
#print(maz.head())
#print(maz.info())
maz_data = pd.read_csv(tt.data('SERPM8-MAZDATA', '*.csv'))
#print(maz_data.head())
#print(maz_data.info())
# fl_county = gpd.read_file(tt.data('FL-COUNTY-SHAPE'))  the data provided by the Exercise might be wrong




# Q: Generate a population density map of Miami-Dade County, at the MAZ resolution level for SERPM 8.

'''
fig, ax = plt.subplots(figsize=(12,9))
ax.axis('off')      # don't show axis
ax.set_title("Population Density", fontweight='bold', fontsize=16)
ax = maz_1.plot(ax=ax, column='PopDen')
plt.show()
'''