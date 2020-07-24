import transportation_tutorials as tt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
pd.options.display.max_columns = 100

trip = pd.read_csv(tt.data('SERPM8-BASE2015-TRIPS'))
print(trip.info())
hh = pd.read_csv(tt.data('SERPM8-BASE2015-HOUSEHOLDS'))
print(hh.info())

trip_hh_merge = pd.merge(
    hh,
    trip.groupby(['hh_id']).size().rename('n_trips'),
    left_on=['hh_id'],
    right_index=True,
)
print(trip_hh_merge.head())
# Prepare a heatmap that visualizes the joint distribution of the number of trips taken by each household and the number of automobiles owned by the household.

# For households with 2 automobiles, what is the most frequent number of trips made by those households in the data?
'''resluts_1 = trip_hh_merge.pivot_table(
    index='autos',
    columns='n_trips',
    aggfunc='size'
)
print(resluts_1)
'''
sns.heatmap(
    trip_hh_merge.pivot_table(
        index='autos',
        columns='n_trips',
        aggfunc='size'
    ).fillna(0),
    annot=True,
    fmt=",.0f",
    vmax=1500,
    linewidths=0.5,
    cmap="YlGnBu",
    annot_kws={'size': 5, 'weight': 'bold', 'color': 'blue'}
);
plt.figure(figsize = (25, 3))
plt.show()
# answer=6

# For households making 2 trips in the data, how many automobiles do most households own?
# answer=1