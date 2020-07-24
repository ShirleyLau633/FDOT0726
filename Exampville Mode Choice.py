import larch, numpy, pandas, os
import larch.exampville
from matplotlib import pyplot as plt

# 导入数据
skims = larch.OMX(larch.exampville.files.skims, mode='r')
hh = pandas.read_csv(larch.exampville.files.hh)
pp = pandas.read_csv(larch.exampville.files.person)
tour = pandas.read_csv(larch.exampville.files.tour)

tour.TOURPURP.statistics()
df = tour[tour.TOURPURP == 1]    # 筛选出步行的数据
# print(df.info()) # df的数据信息
# print(df['TOURPURP'])   # 读取df的'TOURPURP'的列

df = df.merge(hh, on='HHID').merge(pp, on=('HHID', 'PERSONID'))
df["HOMETAZi"] = df["HOMETAZ"] - 1
df["DTAZi"] = df["DTAZ"] - 1


df = df.join(
    skims.get_rc_dataframe(
        df["HOMETAZi"], df["DTAZi"],
    )
)


# For clarity, we can define numbers as names for modes
DA = 1
SR = 2
Walk = 3
Bike = 4
Transit = 5

dfs = larch.DataFrames(
    co=df,
    alt_codes=[DA,SR,Walk,Bike,Transit],
    alt_names=['DA','SR','Walk','Bike','Transit'],
    ch_name='TOURMODE',
)

# Model Definition
m = larch.Model(dataservice=dfs)
m.title = "Exampville Work Tour Mode Choice v1"

from larch import P, X
P('NamedParameter')
X.NamedDataValue
P('Named Parameter')
X("log(INCOME)")
P.InVehTime * X.AUTO_TIME + P.Cost * X.AUTO_COST

m.utility_co[DA] = (
        + P.InVehTime * X.AUTO_TIME
        + P.Cost * X.AUTO_COST # dollars per mile
)


m.utility_co[SR] = (
        + P.ASC_SR
        + P.InVehTime * X.AUTO_TIME
        + P.Cost * (X.AUTO_COST * 0.5) # dollars per mile, half share
        + P("LogIncome:SR") * X("log(INCOME)")
)


m.utility_co[Walk] = (
        + P.ASC_Walk
        + P.NonMotorTime * X.WALK_TIME
        + P("LogIncome:Walk") * X("log(INCOME)")
)


m.utility_co[Bike] = (
        + P.ASC_Bike
        + P.NonMotorTime * X.BIKE_TIME
        + P("LogIncome:Bike") * X("log(INCOME)")
)


m.utility_co[Transit] = (
        + P.ASC_Transit
        + P.InVehTime * X.TRANSIT_IVTT
        + P.OutVehTime * X.TRANSIT_OVTT
        + P.Cost * X.TRANSIT_FARE
        + P("LogIncome:Transit") * X('log(INCOME)')
)

Car = m.graph.new_node(parameter='Mu:Car', children=[DA,SR], name='Car')
NonMotor = m.graph.new_node(parameter='Mu:NonMotor', children=[Walk,Bike], name='NonMotor')
Motor = m.graph.new_node(parameter='Mu:Motor', children=[Car,Transit], name='Motor')


m.choice_co_code = 'TOURMODE'

m.availability_co_vars = {
    DA: 'AGE >= 16',
    SR: 1,
    Walk: 'WALK_TIME < 60',
    Bike: 'BIKE_TIME < 60',
    Transit: 'TRANSIT_FARE>0',
}

m.load_data()
# print(m.dataframes.choice_avail_summary())

# print(m.dataframes.data_co.statistics())
result = m.maximize_loglike(method='slsqp')
# print(result)
m.calculate_parameter_covariance()
# print(m.parameter_summary())
print(m.estimation_statistics())

report = larch.Reporter(title=m.title)
report << "# Estimation Statistics" << m.estimation_statistics()
report << "# Utility Functions" << m.utility_functions()
report.save(
    '/tmp/exampville_mode_choice.html',
    overwrite=True,
    metadata=m,
)
