import transportation_tutorials as tt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

bridge = pd.read_csv(tt.data('FL-BRIDGES'))
print(bridge.info())
print(bridge.head())
print(bridge['SD #'])
print(bridge['County'])

# Which county has the highest number of structurally deficient bridges? Use a frequency plot to find your answer.
bridge = bridge[:-1]
bridge['SD #'] = bridge['SD #'].replace('-', 0).astype('int64')
print(bridge['SD #'])
# bridge_SD_counts = bridge['SD #'].value_counts(sort=True)
ax = bridge.plot(x='County', y='SD #', kind='bar', color='green', figsize = (25,3))
ax.set_xlabel("County")
ax.set_ylabel("number of structurally deficient bridges");
plt.show()
# answer: DUVAL(031)
# Solution: bridge_count.sort_values(by = 'SD #', ascending = False).plot( x = 'County', y = 'SD #', kind = 'bar', figsize = (25,3), color = 'coral');
# bridge_count[bridge_count['SD #'] == bridge_count['SD #'].max()]['County'].values[0]

# Which county has the lowest percentage of bridges that are in good condition? Use a bar chart to find your answer.
bridge['Fraction of Good #'] = bridge["Good #"] / bridge.groupby('County')["Total #"].transform('sum')
bridge.sort_values(by = 'Fraction of Good #', ascending = True).plot(x = 'County', y = 'Fraction of Good #', kind = 'bar', figsize = (25,3), color = 'coral');
ax.set_xlabel("County")
ax.set_ylabel("Fraction of Good #");
plt.show()

# answer: FRANKLIN(037)
# Solution: bridge_percentage[bridge_percentage['Good %'] == bridge_percentage['Good %'].min()]['County'].values[0]