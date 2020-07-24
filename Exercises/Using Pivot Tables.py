import transportation_tutorials as tt
import pandas as pd
import numpy as np

tour = pd.read_csv(tt.data('SERPM8-BASE2015-TOURS'))
print(tour.info())

tour_mode_dict = {
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

# Within the Jupiter study area, what is the average distance for bike tours to work? (Hint: It is 4.03 miles)
#print(tour[['person_id', 'tour_mode', 'tour_distance']])
walk_tour = tour[['person_id', 'tour_purpose', 'tour_mode', 'tour_distance']]
walk_tour['tour_mode'] = walk_tour['tour_mode'].map(tour_mode_dict)
print(walk_tour)
resluts_1 = walk_tour.pivot_table(
    index='tour_mode',
    columns='tour_purpose',
    values='tour_distance',
    margins=True,
)
print(resluts_1['Work'])

# What tour purpose has the highest average tour distance? (Hint: Work tours)
resluts_2 = walk_tour.pivot_table(
    index='tour_purpose',
    values='tour_distance',
    margins=True,
)
print(resluts_2)

# What is the median distance of walking for all tour purposes? (Hint: 0.548 miles)
resluts_3 = walk_tour.pivot_table(
    index='tour_mode',
    values='tour_distance',
    aggfunc=['median']
)
print(resluts_3)