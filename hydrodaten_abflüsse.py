#!/usr/bin/env python
# coding: utf-8

# In[5]:


import requests
import pandas as pd
from datetime import timedelta, time
from time import sleep
import numpy as np


# **Datawrapper-Update-Funktion**

# In[ ]:


#Grafik-Updates nur um 00.05 und 12 Uhr. Variablen werden in Abfluss-Funktion verwendet
update_time1 = time(hour=3, minute=10)
update_time2 = time(hour=10, minute=30)

datawrapper_url = 'https://api.datawrapper.de/v3/charts/'
headers = {"Authorization": "Bearer exBDzRsC86QAktkFECOOvK0ZjVTDN2u1LOWq6VjdTsaHUh9mjaKJodeYRIh75F68"}

def datawrapper_updater(chart_id, four_day_range):
    
    url_update = datawrapper_url + chart_id
    url_publish = url_update + "/publish"
    
    payload = {
        
    "metadata": {"visualize": {"custom-ticks-x": four_day_range}}
    
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
    df_abfluss.columns = ['Time', 'Abfluss', 'date']
    
    #letzte Zeitangabe (je nach dem werden Datawrapper-Grafiken upgedatet und neu publiziert)
    last_date = df_abfluss['date'].tail(1).values[0]
    last_date_time = pd.Timestamp(last_date).time()
    
    #nur die benötigten Spalten behalten, date als Index
    df_abfluss = df_abfluss[['date', 'Abfluss']].copy()
    df_abfluss.set_index('date', inplace=True)
    
    #Zusätzliche, leere Zeiten einfügen (damit die Grafiken besser aussehen)
    additional_values = pd.date_range(start=df_abfluss.index.max(), freq="5min", periods=240)
    additional_values = additional_values[1:]
    
    for t in additional_values:
        df_abfluss.loc[t] = np.nan
    
    #Gefahrenstufen hinzufügen
    df_abfluss['gs1'] = gefahrenstufen['gs1']
    df_abfluss['gs2'] = gefahrenstufen['gs2']
    df_abfluss['gs3'] = gefahrenstufen['gs3']
    df_abfluss['gs4'] = gefahrenstufen['gs4']
    df_abfluss['gs5'] = gefahrenstufen['gs5']
    
    #Daten von heute, gestern, vorgestern und morgen (für Datawrapper-Grafiken)
    four_day_range = df_abfluss.index.strftime('%d.%m.%Y').unique()[1:]
    four_day_range = ', '.join(four_day_range)
    
    #Wenn eine Bedingung == True, werden Grafiken upgedatet
    if last_date_time == update_time1 or last_date_time == update_time2:
        datawrapper_updater(gefahrenstufen['datawrapper-id'], four_day_range)
    
    #Export als csv
    df_abfluss.to_csv('/root/hydrofiles/final_data/final_{}.csv'.format(station))


# In[ ]:


#Gefahrenstufen und Datawrapper-Chart-ID für jede Station
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
    },
    #Rheintaler Binnenkanal - St. Margrethen
    2139:
    {
        'gs1': 75,
        'gs2': 110,
        'gs3': 130,
        'gs4': 150,
        'gs5': 300,
        'datawrapper-id': '1u2ku'
    },
    #Rhein - Diepoldsau, Rietbrücke
    2473:
    {
        'gs1': 1300,
        'gs2': 1950,
        'gs3': 2450,
        'gs4': 3050,
        'gs5': 5000,
        'datawrapper-id': 'Nv1Rj'
    },
    #Reuss - Luzern, Geissmattbrücke
    2152:
    {
        'gs1': 280,
        'gs2': 350,
        'gs3': 390,
        'gs4': 430,
        'gs5': 750,
        'datawrapper-id': 'KAji1'
    },
    #Reuss - Seedorf
    2056:
    {
        'gs1': 280,
        'gs2': 450,
        'gs3': 570,
        'gs4': 690,
        'gs5': 1500,
        'datawrapper-id': 'b9L8z'
    },
    #Engelberger Aa - Buochs, Flugplatz
    2481:
    {
        'gs1': 70,
        'gs2': 110,
        'gs3': 140,
        'gs4': 170,
        'gs5': 300,
        'datawrapper-id': 'WhEA0'
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

