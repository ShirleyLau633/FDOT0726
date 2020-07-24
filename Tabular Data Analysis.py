import os
import gzip
import numpy as np
import geopandas as gpd
import pandas as pd
import transportation_tutorials as tt
import statsmodels.api as sm
from larch.util.data_expansion import piecewise_expansion

#-------------------------------------------------------------------
#Basic Data Analysis with Pandas
'''
raw_los = {
    'Speed': {'Car': 60, 'Bus': 20, 'Walk':3},
    'Cost': {'Car': 3.25, 'Bus': 1.75, 'Walk':0},
}
los = pd.DataFrame(raw_los)
print(los)
print(los.index)
print(los.columns)

los.index = [2, 1, 3]  # 改变index和columns
# print(los)

los = los.set_index('Speed')  # 选择某一列作为index
# print(los)
'''


# 改变矩阵元素的类型
'''raw = {'A': [7,8,9], 'B': [1,2,3], 'C': [4.1,5.2,6.3]}
df = pd.DataFrame(raw)
print(df)
print(df.index)
print(df.dtypes)
print(df.T)'''


'''
# pandas读取csv文件
a = os.path.basename(tt.data('FL-COUNTY-POP'))
fl = pd.read_csv(tt.data('FL-COUNTY'))
# print(fl)
fl['Population Density'] = fl['2019 Population'] / fl['Land Area']
# print(fl)
fl.loc[999,['Name', '2019 Population']] = ('Dry Tortugas', 0)  #加一行
# print(fl)
# print(fl.iloc[1:3, 1:2])
districts = pd.read_csv(tt.data('FL-COUNTY-BY-DISTRICT'))
# print(districts.head())
pd.merge(fl, districts, left_on='Name', right_on='County')
fl['County'] = fl['Name'].str.replace(' County', '')   #一对一的匹配
fl_2 = pd.merge(fl, districts, on='County')  #一对一的匹配
print(fl_2.head())
district_info = pd.read_csv(tt.data('FL-DISTRICTS'), index_col='District')
print(district_info.head())
# fl_3 = pd.merge(fl_2, district_info, on='District')
# print(fl_3.head())

fl_4 = pd.merge(fl_2, district_info, on='District')  #一对多的匹配
print(fl_4.head())
print(pd.merge(fl_2, district_info[['Name']].add_prefix('District_'), on='District').head())
'''



'''states = gpd.read_file(tt.data('US-STATES'))
print(states.head())'''


'''
with gzip.open(tt.data('FL-BRIDGES'), 'rt') as previewfile:
    print(*(next(previewfile) for x in range(6)))
bridges = pd.read_csv(tt.data('FL-BRIDGES'))
print(bridges.head())
print(bridges.columns)
bridges2 = bridges.set_index('County')   # 把County作为行号的index
print(bridges2.head())
print(bridges2.columns)
bridges2.columns = pd.MultiIndex.from_tuples(
    [('Count','Total'), ('Count','Good'), ('Count','Fair'), ('Count','Poor'), ('Count','SD'),
     ('Area','Total'), ('Area','Good'), ('Area','Fair'), ('Area','Poor'), ('Area','SD'),     ],
    names=['measure', 'condition'],
)
print(bridges2.head())
print(bridges2.columns)
'''

'''
bridges = bridges.replace('-', 0)  # 当数据中是用“-”来代替“0”的时候
bridges[['Poor #', 'SD #']] = bridges[['Poor #', 'SD #']].astype(int)  # 当数据中是用“-”来代替“0”的时候：
a = bridges['SD #'].sum()
print(a)
print(bridges.sort_values('SD #', ascending=False).head())
bridges.drop(67, inplace=True)
b = bridges['SD #'].sum()
print(b)

bridges.fillna(0, inplace=True) #当数据中用“omit”来代替“0”的时候
c = bridges['SD Area'].mean()
print(c)
'''
#--------------------------------------------------------------------------------------------------------------------

#Crosstab and Pivot Tables
'''
hh = pd.read_csv(tt.data('SERPM8-BASE2015-HOUSEHOLDS'), index_col=0)
hh.set_index('hh_id', inplace=True)
print(hh)

# Count of persons per HH
persons = pd.read_csv(tt.data('SERPM8-BASE2015-PERSONS'))
hh = hh.merge(
    persons.groupby('hh_id').size().rename('hhsize'),
    left_on=['hh_id'],
    right_index=True,
)
print(hh)

# Count of trips per HH
trips = pd.read_csv(tt.data('SERPM8-BASE2015-TRIPS'))
hh = hh.merge(
    trips.groupby(['hh_id']).size().rename('n_trips'),
    left_on=['hh_id'],
    right_index=True,
)
print(hh)

print(hh.pivot_table(
    index='hhsize',
    columns='autos',
    values='n_trips',
))


print(hh.pivot_table(
    index='hhsize',
    values='n_trips',
))

print(hh.pivot_table(
    columns='hhsize',
    values='n_trips',
))

hh.pivot_table(
    index=pd.qcut(hh.income, 5),
    columns='autos',
    values='n_trips',
)
'''
#--------------------------------------------------

#Linear Regression

#读取households数据
hh = pd.read_csv(tt.data('SERPM8-BASE2015-HOUSEHOLDS'), index_col=0)
hh.set_index('hh_id', inplace=True)

#读取trips数据
trips = pd.read_csv(tt.data('SERPM8-BASE2015-TRIPS'))


#要寻找线性回归关系，需要将hh和trips表格先进行合并
hh = hh.merge(
    trips.groupby(['hh_id']).size().rename('n_trips'),
    left_on=['hh_id'],
    right_index=True,
)

#假设n_trips和income、autos（拥有机动车数量）有关，构建最小二乘回归模型
mod = sm.OLS(
    hh.n_trips,
    sm.add_constant(hh[['autos','income']])
)
res = mod.fit()
#print(res.summary())


hh['income_100k'] = hh.income / 100_000
mod = sm.OLS(
    hh.n_trips,
    sm.add_constant(hh[['autos','income_100k']])
)
res = mod.fit()
#print(res.summary())


#print(piecewise_expansion(hh.income, [25_000, 75_000]).head())

hh['autos^2'] = hh['autos'] ** 2
hh['income^2'] = hh['income_100k'] ** 2

mod = sm.OLS(
    hh.n_trips,
    sm.add_constant(hh[['autos','income_100k', 'autos^2', 'income^2']])
)
res = mod.fit()
# print(res.summary())

piecewise_expansion(hh.income, [25_000, 75_000]).head()


hh_edited = pd.concat([
    hh.autos,
    piecewise_expansion(hh.income_100k, [.25, .75]),
], axis=1)

hh_edited.head()

mod = sm.OLS(
    hh.n_trips,
    sm.add_constant(hh_edited)
)
res = mod.fit()
print(res.summary())

'''
def polynomial(x, **kwargs):
    from sklearn.preprocessing import PolynomialFeatures
    poly = PolynomialFeatures(**kwargs)
    arr = poly.fit_transform(x)
    return pd.DataFrame(arr, columns=poly.get_feature_names(x.columns), index=x.index)

hh_poly = polynomial(hh[['autos','income_100k']], degree=3)
print(hh_poly.head())
'''