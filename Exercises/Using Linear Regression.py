import transportation_tutorials as tt
import pandas as pd
import numpy as np
import statsmodels.api as sm

per = pd.read_csv(tt.data('SERPM8-BASE2015-PERSONS'))
hh = pd.read_csv(tt.data('SERPM8-BASE2015-HOUSEHOLDS'))
print(per.info())
print(hh.info())

per_hh_merge = pd.merge(
    per,
    hh,
    on='hh_id',
    how='inner',
)
print(per_hh_merge.info())
print(per_hh_merge['type'].head())
print(per_hh_merge['gender'].head())
print(per_hh_merge['transponder'].head())
print(per_hh_merge['autotech'].head())
print(per_hh_merge['autos'].head())

per_hh_merge['gender'] = np.where((per_hh_merge['gender'] == 'm'), 1, 0)     # result = np.where(condition, x, y) condition=True→x
per_hh_merge['type'] = np.where((per_hh_merge['type'] == 'Full-time worker'), 1, 0)

mod = sm.OLS(
    per_hh_merge.value_of_time,
    sm.add_constant(per_hh_merge[['age', 'gender', 'type', 'income']])
)
res = mod.fit()
print(res.summary())


'''Construct an ordinary least squares linear regression model to predict the given value of time for each individual in the Jupiter study area data as a function of: - age, - gender, - full-time employment status, and - household income.'''

# What are the coefficients on this model?
'''
                coef
const          6.9306
age            0.0361
gender         0.0345
type           1.7770
income      9.476e-06
'''
# Do any of these factors appear to actually be not relevant in determining an individual’s value of time? (Hint: Gender)
'''gender'''
# If other variables from the household and person datasets could also be included in the OLS model specificiation, are there any that are also significant? (Hint: Yes, there is at least one other relevant factor in this data.)
mod = sm.OLS(
    per_hh_merge.value_of_time,
    sm.add_constant(per_hh_merge[['age', 'gender', 'type', 'income', 'autos', 'transponder']])
)
res = mod.fit()
print(res.summary())
'''autos is relevent'''