import transportation_tutorials as tt
import numpy as np
import pandas as pd
import geopandas as gpd
from matplotlib import pyplot as plt

# 导入TAZ和MAZ的数据
xmin = 905712
ymin = 905343
taz = gpd.read_file(tt.data('SERPM8-TAZSHAPE')).cx[xmin:, ymin:]
maz = gpd.read_file(tt.data('SERPM8-MAZSHAPE')).cx[xmin:, ymin:]
center = (945495, 941036)

'''
# 5.3.1 Simple Map
# 用plot工具
ax = taz.plot()
ax = taz.plot(color='green', linewidth=2, edgecolor='white')

# 可以再同一个地图中展示
ax = maz.plot(linewidth=1,  color='green', edgecolor='white')
ax = taz.plot(ax=ax, color=(0,0,0,0), linewidth=1, edgecolor='black')

# 自定义地图的特征
fig, ax = plt.subplots(figsize=(12,9))
ax.axis('on')      # do show axis as a frame
ax.set_xticks([])  # but no tick marks
ax.set_yticks([])  # one either axis
ax.set_title("SERPM 8 Zones", fontweight='bold', fontsize=16, pad=20)
ax.annotate('in the viscinity of Jupiter, FL',
            xy=(0.5, 1.0), xycoords='axes fraction',
            xytext=(0, 5), textcoords='offset points',
            horizontalalignment='center',
            fontstyle='italic')

from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color='black', linewidth=1, label='TAZ'),
    Line2D([0], [0], color='red', linewidth=0.5, label='MAZ'),
]
ax.legend(handles=legend_elements, title='Legend')
ax = maz.plot(ax=ax, linewidth=0.5,  color='white', edgecolor='red', label='MAZ')
ax = taz.plot(ax=ax, color=(0,0,0,0), linewidth=1, edgecolor='black')
'''
# 5.3.2 Mapping Data
mazd = pd.read_csv(tt.data('SERPM8-MAZDATA', '*.csv'))
maz1 = maz.merge(mazd, how='left', left_on='MAZ', right_on='mgra')
'''
# 5.3.3 Choropleth Maps 分级统计图
fig, ax = plt.subplots(figsize=(12,9))
ax.axis('off') # don't show axis
ax.set_title("Population Density", fontweight='bold', fontsize=16)
ax = maz1.plot(ax=ax, column='PopDen’)   # 用PopDen作为

# 增加图例
fig, ax = plt.subplots(figsize=(12,9))
ax.axis('off') # don't show axis
ax.set_title("Population Density", fontweight='bold', fontsize=16)
ax = maz1.plot(ax=ax, column='PopDen', legend=True)

# 改变颜色
fig, ax = plt.subplots(figsize=(12,9))
ax.axis('off') # don't show axis
ax.set_title("Population Density", fontweight='bold', fontsize=16)
ax = maz1.plot(ax=ax, column='PopDen', legend=True, cmap='OrRd')
'''
'''
# Adding a Background
import contextily as ctx


def add_basemap(ax, zoom, url='http://tile.stamen.com/terrain/tileZ/tileX/tileY.png'):
    xmin, xmax, ymin, ymax = ax.axis()
    basemap, extent = ctx.bounds2img(xmin, ymin, xmax, ymax, zoom=zoom, url=url)
    ax.imshow(basemap, extent=extent, interpolation='bilinear')
    # restore original x/y limits
    ax.axis((xmin, xmax, ymin, ymax))


    attribution_txt = "Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL."
    ax.annotate(
        attribution_txt,
        xy=(1.0, 0.0), xycoords='axes fraction',
        xytext=(0, -10), textcoords='offset points',
        horizontalalignment='right',
        fontstyle='italic',
        fontsize=8,
    )
    return ax

maz2 = maz1.to_crs(epsg=3857)

fig, ax = plt.subplots(figsize=(12,9))
ax.axis('off') # don't show axis
ax.set_title("Population Density", fontweight='bold', fontsize=16)
ax = maz2.plot(ax=ax, alpha=0.6, linewidth=0, cmap='viridis', column='PopDen', legend=True)
ax = add_basemap(ax, zoom=12, url=ctx.sources.ST_TONER_LITE)
'''

tt.show_file(tt.tools.point_map)
random_points = tt.tools.point_map.generate_points_in_areas(maz1, values='POP', points_per_unit=20,)
fig, ax = plt.subplots(figsize=(12,9))
ax.axis('off') # don't show axis
ax.set_title("Population", fontweight='bold', fontsize=16, pad=20)
ax.annotate('Each point represents 20 people',
            xy=(0.5, 1.0), xycoords='axes fraction',
            xytext=(0, 5), textcoords='offset points',
            horizontalalignment='center',
            fontstyle='italic')
ax = random_points.plot(ax=ax, markersize=1)
plt.show()

