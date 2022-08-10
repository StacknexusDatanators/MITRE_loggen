import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import sqlite3 as lite

print("running log generator...")


con = lite.connect('./testdb.db')

print("connected to db")


events = ['FuelIngest', 'FuelSpent']

depots = ['Osaka', 'Guam'] 
# Sydney ID : 07d62e88-ff0c-4254-9350-c5829e28c9a9	
depot_ids = ['4cb10252-6708-4780-ba93-c877a9474483', '8ed0d98e-6e05-448a-a358-74434eaed284']


min_fuel_threshold = 10
max_fuel_threshold = 1000

curr_fuel = {}

def get_curr_fuel(did):
    qr = "SELECT event, sum(value) as val FROM eventlogs WHERE depot='{0}' GROUP BY event;".format(did)
    df = pd.read_sql(qr, con).set_index('event')
    return df.loc['FuelIngest', 'val']-df.loc['FuelSpent', 'val']
### Check if table exists
qr = "SELECT name FROM sqlite_master WHERE type='table' AND name='eventlogs';"
cur = con.execute(qr)

if len(cur.fetchall()) != 0:
    for did in depot_ids:
        curr_fuel[did] = get_curr_fuel(did)

nlogs = np.random.randint(low = 10, high = 500)

logs_df = pd.DataFrame()

logs_df['timestamp'] = pd.date_range(start = datetime.now()-timedelta(minutes = 10), end = datetime.now()
                      , periods = nlogs)

logs_df['depot'] = list(np.random.choice(depot_ids, size = nlogs))


eventlist = []
vallist = []
for i, row in logs_df.iterrows():
    if row['depot'] in curr_fuel.keys():
        if curr_fuel[row['depot']]<=min_fuel_threshold:
            eventlist.append('FuelIngest')
            val = np.random.randint(low = 100, high = max_fuel_threshold)
            vallist.append(val)
            curr_fuel[row['depot']] += val
        else:
            ev = np.random.choice(events)
            if ev == 'FuelIngest':
                val = np.random.randint(low = 100, high = max_fuel_threshold)
                vallist.append(val)
                curr_fuel[row['depot']] += val
            elif ev == 'FuelSpent':
                val = np.random.randint(low = min_fuel_threshold, high = curr_fuel[row['depot']])
                vallist.append(val)
                curr_fuel[row['depot']] -= val
            eventlist.append(ev)
    else:
        eventlist.append('FuelIngest')
        val = np.random.randint(low = 100, high = max_fuel_threshold)
        vallist.append(val)
        curr_fuel[row['depot']] = val

logs_df['event'] = eventlist
logs_df['value'] = vallist

def get_units(did):
    if did == '4cb10252-6708-4780-ba93-c877a9474483':
        return 'litres'
    elif did == '8ed0d98e-6e05-448a-a358-74434eaed284':
        return 'gallons'


logs_df['units'] = logs_df['depot'].apply(get_units)

logs_df.to_sql('eventlogs', con, index = False, if_exists='append')

print("data logged from {0} to {1}".format(logs_df['timestamp'].min(), logs_df['timestamp'].max()))


con.close()