#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from datetime import timedelta


# In[ ]:


def abfluss(station, gefahrenstufen):
    df_abfluss = pd.read_csv('/root/hydrofiles/{}.csv'.format(station))
    df_abfluss['Time'] = pd.to_datetime(df_abfluss['Time'])
    df_abfluss['date'] = pd.to_datetime(df_abfluss['Time'].dt.strftime('%Y-%m-%d %H:%M:%S')) + timedelta(hours=1)
    df_abfluss.columns = ['Time', 'abfluss', 'date']
    df_abfluss = df_abfluss[['date', 'abfluss']].copy()
    df_abfluss['gs1'] = gefahrenstufen['gs1']
    df_abfluss['gs2'] = gefahrenstufen['gs2']
    df_abfluss['gs3'] = gefahrenstufen['gs3']
    df_abfluss['gs4'] = gefahrenstufen['gs4']
    df_abfluss['gs5'] = gefahrenstufen['gs5']
    df_abfluss.to_csv('/root/hydrofiles/final_data/final_{}.csv'.format(station), index=False)


# In[7]:


stations = {
    2016:
    {
        'gs1': 820,
        'gs2': 1100,
        'gs3': 1250,
        'gs4': 1350,
        'gs5': 2000
    },
    2018:
    {
        'gs1': 480,
        'gs2': 640,
        'gs3': 720,
        'gs4': 830,
        'gs5': 2000
    },
    2063:
    {
        'gs1': 720,
        'gs2': 940,
        'gs3': 1050,
        'gs4': 1150,
        'gs5': 2000
    },
    2091:
    {
        'gs1': 2500,
        'gs2': 3000,
        'gs3': 3600,
        'gs4': 4500,
        'gs5': 6000
    },
    2110:
    {
        'gs1': 470,
        'gs2': 600,
        'gs3': 700,
        'gs4': 810,
        'gs5': 2000
    },
    2243:
    {
        'gs1': 350,
        'gs2': 480,
        'gs3': 550,
        'gs4': 630,
        'gs5': 2000
    }
}

for key, value in stations.items():
    abfluss(str(key), value)

