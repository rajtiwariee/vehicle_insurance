# %%
import pandas as pd
import numpy as np

df  = pd.read_csv('data.csv', sep=',')
df.head()
#%%

df_dict = df.to_dict(orient='records')
df_dict

