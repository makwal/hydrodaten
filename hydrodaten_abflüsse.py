#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from datetime import timedelta


# In[ ]:


def abfluss(station):
    df_abfluss = pd.read_csv('{}.csv'.format(station))
    df_abfluss['Time'] = pd.to_datetime(df_abfluss['Time'])
    df_abfluss['date'] = pd.to_datetime(df_abfluss['Time'].dt.strftime('%Y-%m-%d %H:%M:%S')) + timedelta(hours=1)
    df_abfluss.columns = ['Time', 'abfluss', 'date']
    df_abfluss = df_abfluss[['date', 'abfluss']].copy()
    df_abfluss.to_csv('final_data/final_{}.csv'.format(station))


# In[ ]:


stations = [2016, 2018, 2063, 2091, 2110, 2243]

for s in stations:
    abfluss(str(s))

