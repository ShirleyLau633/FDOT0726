import transportation_tutorials as tt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

hh = pd.read_csv(tt.data('SERPM8-BASE2015-HOUSEHOLDS'))
person = pd.read_csv(tt.data('SERPM8-BASE2015-PERSONS'))
print(person.info())
print(hh.info())

hh_person_merge = pd.merge(
    hh,
    person,
    on='hh_id',
    how='inner',
)
print(hh_person_merge.head())

# Use a boxplot to show the distribution of household income in the Jupiter study area, by number of automobiles owned. What is the median income of households who own exactly two automobiles? (Hint: the correct answer is $96 thousand.)
hh = hh[(hh.income > 0) & (hh.income != 0)]
data_1 = list(hh.groupby('autos').income)
ax = plt.boxplot(
    [i[1] for i in data_1],
    vert=False,
    labels=[i[0] for i in data_1],
    notch=True,
)
plt.title('Household Income by number of automobiles owned')
plt.xlim(-10_000,200_000)
plt.xlabel('Household Income')
plt.ylabel('number of automobiles')
plt.show()
result_1 = np.median(hh[hh.autos == 2].income)
print(result_1)

# Is the median income higher or lower if we only consider two-car households that have at least one person over age 65? Create a set of box plots similar to those created in question (1), but only for households with at least one person over age 65.
age_over_65 = pd.merge(
    hh_person_merge,
    hh_person_merge.groupby(['hh_id'])['age'].max().rename('age_over_65'),
    left_on=['hh_id'],
    right_index=True,
)
print(age_over_65)
age_over_65 = age_over_65[age_over_65.age_over_65 > 65 ]
print(age_over_65)
data_2 = list(age_over_65.groupby('autos').income)
ax = plt.boxplot(
    [i[1] for i in data_1],
    vert=False,
    labels=[i[0] for i in data_1],
    notch=True,
    positions = range(2, (len(data_2))*2+2, 2),
)
ax = plt.boxplot(
    [i[1] for i in data_2],
    vert=False,
    labels=[i[0] for i in data_2],
    notch=True,
    boxprops={'color':'red'},
    flierprops = {'marker':'o', 'color':'red'},
    positions=range(1, (len(data_2)) * 2 + 1, 2),
)
plt.title('Household Income by number of automobiles owned with at least one person over age 65')
plt.xlim(-10_000, 300_000)
plt.xlabel('Household Income')
plt.ylabel('number of automobiles')
plt.show()

# answer：higher