import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

vehicles_df = pd.read_csv('vehicles.csv')
names = list(vehicles_df['brand + Model' ])
brands = [i.split(' ', 1)[0] for i in names]
vehicles_df['Brands'] = brands
vehicles_df['Brandsid'] = vehicles_df['Brands'].astype('category').cat.codes
vehicles_df.to_csv('vehicles.csv',index=False)

# %%
r = vehicles_df.emit_vehicleprod/vehicles_df.emit_fuelcons
plt.boxplot(r[~np.isnan(r)])


pd.plotting.parallel_coordinates(vehicles_df, 'Brands', cols=['MPGe', 'MPG', 'HP', 'cost_fuel', 'emit_vehicleprod',
       'emit_batteryprod', 'emit_fuelprod', 'emit_fuelcons'])
plt.xticks(rotation=90)
plt.gca().legend_.remove()