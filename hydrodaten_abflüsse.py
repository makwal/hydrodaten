#!/usr/bin/env python
# coding: utf-8

# In[5]:


import requests
import pandas as pd
from datetime import timedelta, time
from time import sleep


# **Datawrapper-Update-Funktion**

# In[ ]:


#Grafik-Updates nur um 00.05 und 12 Uhr. Variablen werden in Abfluss-Funktion verwendet
update_time1 = time(hour=0, minute=5)
update_time2 = time(hour=12, minute=0)

datawrapper_url = 'https://api.datawrapper.de/v3/charts/'
headers = {"Authorization": "Bearer exBDzRsC86QAktkFECOOvK0ZjVTDN2u1LOWq6VjdTsaHUh9mjaKJodeYRIh75F68"}

def datawrapper_updater(chart_id, last_three_days):
    
    url_update = datawrapper_url + chart_id
    url_publish = url_update + "/publish"
    
    payload = {
        
    "metadata": {"visualize": {"custom-ticks-x": last_three_days}}
    
    }
    
    res_update = requests.patch(url_update, json=payload, headers=headers)
    
    sleep(3)
    
    res_publish = requests.post(url_publish, headers=headers)


# **Hauptdaten: Abfluss-Funktion**

# In[ ]:


#Funktion erstellen, die die Stationsnummer und die dazugehörigen Gefahrenstufen mitnimmt
def abfluss(station, gefahrenstufen):
    df_abfluss = pd.read_csv('/root/hydrofiles/{}.csv'.format(station))
    
    #Formatieren
    df_abfluss['Time'] = pd.to_datetime(df_abfluss['Time'])
    df_abfluss['date'] = pd.to_datetime(df_abfluss['Time'].dt.strftime('%Y-%m-%d %H:%M:%S')) + timedelta(hours=2)
    df_abfluss.columns = ['Time', 'abfluss', 'date']
    
    #Daten von heute, gestern und vorgestern (für Datawrapper-Grafiken)
    last_three_days = df_abfluss['date'].dt.strftime('%d.%m.%Y').unique()[1:]
    last_three_days = ', '.join(last_three_days)
    
    #letzte Zeitangabe (je nach dem werden Datawrapper-Grafiken upgedatet und neu publiziert)
    last_date = df_abfluss['date'].tail(1).values[0]
    last_date_time = pd.Timestamp(last_date).time()
    
    #nur die benötigten Spalten behalten
    df_abfluss = df_abfluss[['date', 'abfluss']].copy()
    
    #Gefahrenstufen hinzufügen
    df_abfluss['gs1'] = gefahrenstufen['gs1']
    df_abfluss['gs2'] = gefahrenstufen['gs2']
    df_abfluss['gs3'] = gefahrenstufen['gs3']
    df_abfluss['gs4'] = gefahrenstufen['gs4']
    df_abfluss['gs5'] = gefahrenstufen['gs5']
    
    #Wenn eine Bedingung == True, werden Grafiken upgedatet
    if last_date_time == update_time1 or last_date_time == update_time2:
        datawrapper_updater(gefahrenstufen['datawrapper-id'], last_three_days)
    
    #Export als csv
    df_abfluss.to_csv('/root/hydrofiles/final_data/final_{}.csv'.format(station), index=False)


# In[ ]:


#Gefahrenstufen für jede Station
stations = {
    #Aare Brugg
    2016:
    {
        'gs1': 820,
        'gs2': 1100,
        'gs3': 1250,
        'gs4': 1350,
        'gs5': 2000,
        'datawrapper-id': '1Zrrn'
    },
    #Reuss Mellingen
    2018:
    {
        'gs1': 480,
        'gs2': 640,
        'gs3': 720,
        'gs4': 830,
        'gs5': 2000,
        'datawrapper-id': '9Vw1A'
    },
    #Aare Murgenthal
    2063:
    {
        'gs1': 720,
        'gs2': 940,
        'gs3': 1050,
        'gs4': 1150,
        'gs5': 2000,
        'datawrapper-id': 'gZgpV'
    },
    #Rhein Rheinfelden
    2091:
    {
        'gs1': 2500,
        'gs2': 3000,
        'gs3': 3600,
        'gs4': 4500,
        'gs5': 6000,
        'datawrapper-id': 'p9yMw'
    },
    #Reuss Mühlau
    2110:
    {
        'gs1': 470,
        'gs2': 600,
        'gs3': 700,
        'gs4': 810,
        'gs5': 2000,
        'datawrapper-id': 'BjWyo'
    },
    #Limmat Baden
    2243:
    {
        'gs1': 350,
        'gs2': 480,
        'gs3': 550,
        'gs4': 630,
        'gs5': 2000,
        'datawrapper-id': 'JUMNz'
    }
}

for key, value in stations.items():
    abfluss(str(key), value)


# **Datawrapper-Update**

# In[6]:


datawrapper_charts = {
    'aare_brugg': '1Zrrn',
    'aare_murgenthal': 'gZgpV',
    'limmat_baden': 'JUMNz',
    'reuss_mellingen': '9Vw1A',
    'reuss_mühlau': 'BjWyo',
    'rhein_rheinfelden': 'p9yMw'
}

