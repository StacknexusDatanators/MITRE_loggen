from fastapi import FastAPI
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import sqlite3 as lite
import os

con = lite.connect('../loggen/testdb.db')


app = FastAPI()

@app.get('/')
async def hello():
    return "Welcome to MITRE mock api"
def check_db():
    qr = "SELECT name FROM sqlite_master WHERE type='table' AND name='eventlogs';"
    cur = con.execute(qr)

    if len(cur.fetchall()) != 0:
        print('running loggen initially')
        os.system("/usr/local/bin/python /loggen/loggen.py")

@app.post('/logs_last_time', status_code = 200)
async def get_logs_lt(last_time:datetime):
    check_db()
    qr = "SELECT * FROM eventlogs WHERE datetime(timestamp) > '{0}'".format(last_time.strftime('%Y-%m-%d %H:%M:%S'))
    res_df = pd.read_sql(qr, con)
    messages = res_df.to_string(index_names = False, header = False, index = False).split('\n')
    return messages
@app.get('/get_logs', status_code=200)
async def get_logs():
    check_db()
    last_time = datetime.now()-timedelta(hours  = 1)
    qr = "SELECT * FROM eventlogs WHERE datetime(timestamp) > '{0}'".format(last_time.strftime('%Y-%m-%d %H:%M:%S'))
    res_df = pd.read_sql(qr, con)
    messages = res_df.to_string(index_names = False, header = False, index = False).split('\n')
    return messages