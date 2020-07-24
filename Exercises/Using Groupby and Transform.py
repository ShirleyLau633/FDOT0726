import transportation_tutorials as tt
import pandas as pd
import numpy as np

districts = pd.read_csv(tt.data('FL-COUNTY-BY-DISTRICT'))
print(districts.head())

bridges = pd.read_csv(tt.data('FL-BRIDGES'))

# Recall the necessary cleaning for the bridges data file
bridges = bridges.replace('-', 0)
bridges[['Poor #', 'SD #']] = bridges[['Poor #', 'SD #']].astype(int)
bridges.fillna(0, inplace=True)
print(bridges.head())
print(bridges.info())

# Within each FDOT District, what is the fraction of structurally deficient bridge deck area in each County?
bridges['County'] = bridges['County'].str[:-6]   # delete the code of each country
districts['County'] = districts['County'].str.upper()   # transfer the country name

bridges_2 = pd.merge(
    bridges,
    districts,
    on='County'
)
print(bridges_2.head())
print(bridges_2.info())


bridges_2['Fraction of SD area'] = bridges_2.groupby('District')['SD Area'].transform(lambda x: (x / x.sum()))
print(bridges_2)

# Which county has the highest share of structurally deficient bridge deck area within its FDOT District? (Hint: the correct answer is PALM BEACH.)

SD_Fraction_Max = bridges_2[['District', 'County', 'Fraction of SD area']].groupby('District').max()
print(SD_Fraction_Max)

# the answer for Q2: bridges_2.loc[bridges_2['SD Area Share in District'].idxmax()]