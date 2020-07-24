import transportation_tutorials as tt
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

#Basic Data Visualization
'''
total_florida_vmt = pd.Series({
    2003: 508_607_851,
    2004: 537_494_319,
    2005: 550_614_540,
    2006: 558_308_386,
    2007: 562_798_032,
    2008: 542_334_376,
    2009: 538_088_986,
    2010: 536_315_479,
    2011: 525_630_013,
    2012: 522_879_155,
    2013: 527_950_180,
    2014: 550_795_629,
    2015: 566_360_175,
    2016: 588_062_806,
    2017: 599_522_329,
})

plt.plot(total_florida_vmt)
plt.ylabel("Total Statewide VMT")

plt.plot(total_florida_vmt, 'blue', label='Current Year VMT')
plt.plot(total_florida_vmt.rolling(5).mean(), 'r--', label='5 Year Rolling Average')
plt.ylabel("Total Statewide VMT")
plt.legend();
plt.show()
'''

# Multi-Dimensional Data
'''
# 导入数据
hh = pd.read_csv(tt.data('SERPM8-BASE2015-HOUSEHOLDS'), index_col=0)
persons = pd.read_csv(tt.data('SERPM8-BASE2015-PERSONS'), index_col=0)
trips = pd.read_csv(tt.data('SERPM8-BASE2015-TRIPS'), index_col=0)

# Add household income to persons
persons = persons.merge(hh.income, left_on='hh_id', right_on=hh.hh_id)

# Count of persons per HH
hh = hh.merge(
    persons.groupby('hh_id').size().rename('hhsize'),
    left_on=['hh_id'],
    right_index=True,
)

# Count of trips per HH
hh = hh.merge(
    trips.groupby(['hh_id']).size().rename('n_trips'),
    left_on=['hh_id'],
    right_index=True,
)

# 散点图--------------
hh.plot(kind='scatter', x='income', y='n_trips')

# 设置点的透明度，用alpha=？
hh.plot(kind='scatter', x='income', y='n_trips', alpha=0.01);


# 聚焦到图片的某一部分，可以设置x轴的长度
ax = hh.plot(kind='scatter', x='income', y='n_trips', alpha=0.03)
ax.set_xlim(0,200_000)
ax.set_ylim(0,30)   # 设置y轴的长度
# ----------------
'''


# 热力图---------------
'''
sns.heatmap(
    hh.pivot_table(
        index='autos',
        columns='hhsize',
        aggfunc='size'
    ).fillna(0),
    annot=True,
    fmt=",.0f"
);

# 设置颜色的跨越维度
sns.heatmap(
    hh.pivot_table(
        index='hhsize',
        columns='autos',
        aggfunc='size'
    ).fillna(0),
    annot=True,
    fmt=",.0f",
    vmax=1500,
);
# 设置不同的颜色
sns.heatmap(
    hh.pivot_table(
        index='hhsize',
        columns='autos',
        aggfunc='size'
    ).fillna(0),
    annot=True,
    fmt=",.0f",
    vmax=1500,
    cmap="YlGnBu",
);
plt.show()



# Box Plots

# Create a hhsize variable capped at 5
hh['hhsize5'] = np.fmin(hh['hhsize'], 5)  # 用于求最小值

data = list(hh.groupby('hhsize5').income)
plt.boxplot(
    [i[1] for i in data],
    vert=False,
    labels=[i[0] for i in data],
)
plt.title('Household Income by Household Size')
plt.xlabel('Household Income')
plt.ylabel('Household Size');

# 聚焦到上图的某一部分
plt.boxplot(
    [i[1] for i in data],
    vert=False, labels=[i[0] for i in data],
    notch=True,
)
plt.title('Household Income by Household Size’)
plt.xlim(-10_000,200_000)
plt.xlabel('Household Income’)
plt.ylabel('Household Size’);
'''


# Histograms and Frequency Plots（直方图和频率图）

# Computing Frequency Data
'''
trips = pd.read_csv(tt.data('SERPM8-BASE2015-TRIPS'))
print(trips.info())

trip_mode_counts = trips.trip_mode.value_counts(sort=True)
print(trip_mode_counts)
trip_mode_dictionary = {
    1: "DRIVEALONEFREE",
    2: "DRIVEALONEPAY",
    3: "SHARED2GP",
    4: "SHARED2PAY",
    5: "SHARED3GP",
    6: "SHARED3PAY",
    7: "TNCALONE",
    8: "TNCSHARED",
    9: "WALK",
    10: "BIKE",
    11: "WALK_MIX",
    12: "WALK_PRMW",
    13: "WALK_PRMD",
    14: "PNR_MIX",
    15: "PNR_PRMW",
    16: "PNR_PRMD",
    17: "KNR_MIX",
    18: "KNR_PRMW",
    19: "KNR_PRMD",
    20: "SCHBUS",
}
trip_mode_counts.index = trip_mode_counts.index.map(trip_mode_dictionary)
print(trip_mode_counts)

# Plotting Frequency Data
#trip_mode_counts.plot(kind='barh', color=‘red’,figsize = ‘?’);
# 对于饼图来说，设置图的颜色没有任何意义

ax = trip_mode_counts.plot(kind='bar')
ax.set_title("Trip Mode Frequency", fontweight='bold')
ax.set_xlabel("Trip Mode")
ax.set_ylabel("Number of Trips");
ax.set_yticklabels([f"{i:,.0f}" for i in ax.get_yticks()])
ax.set_yticks([5000,15000,25000,35000], minor=True);


tm = {11,12,13,14,15,16,17,18,19}
trip_mode_dictionary[21] = 'TRANSIT'
trip_mode_counts = trips.trip_mode.map(lambda x: 21 if x in tm else x).value_counts(sort=False)
trip_mode_counts.index = trip_mode_counts.index.map(trip_mode_dictionary)


ax = trip_mode_counts.plot(kind='bar', color='green')
ax.set_title("Trip Mode Frequency")
ax.set_xlabel("Trip Mode")
ax.set_ylabel("Number of Trips");
plt.show()
'''

# Plotting Histogram Data
hh = pd.read_csv(tt.data('SERPM8-BASE2015-HOUSEHOLDS'), index_col=0)
hh.set_index('hh_id', inplace=True)

hh.income.hist();
plt.show()


hh.income.hist(bins=50, grid=False, color='red');
plt.show()

hh.income.hist(bins=100, grid=False, color='red');
plt.show()

hh.income.hist(bins=200, grid=False, color='red');
plt.show()

bins = np.array([0,10,20,40,60,70,80,90,100,125,150,200,1000]) * 1000
hh.income.hist(bins=bins);
fig, ax = plt.subplots()
ax.hist(hh.income, bins=bins, density=True);
ax = hh.income.hist(grid=False, bins=80)
ax.set_xlim(0,350_000)
ax.set_title("Household Income Histogram");
ax.set_xticklabels([f"${i/1000:.0f}K" for i in ax.get_xticks()]);
ax.set_ylabel("Relative Frequency");
ax.set_yticks([]);





















