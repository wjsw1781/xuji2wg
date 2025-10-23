



# -*- coding: utf-8 -*-

from tqdm import tqdm
import subprocess, time,os,sys,json,random,ipaddress
from loguru import logger

from utils import *

sync_num = 100


import requests
debug_url_host = 'https://unfortunate-abandoned-takin.anvil.app'
# debug_url_host = 'http://8.217.224.52:59001'

d_table_json_url = f'{debug_url_host}/_/api/d_table_json'
c_table_json_url = f'{debug_url_host}/_/api/c_table_json'

for pro_table in table_names_import:
    print('正在同步 -----> ', pro_table)
    cur.execute(f"select * from {pro_table} limit {sync_num}")
    data = cur.fetchall()


    dev_table = pro_table.split('.')[-1]
    for index ,row in enumerate(tqdm(data)):
        if index > sync_num:
            break
        row = dict(row)
        row.pop('_id')
        res = requests.post(d_table_json_url, data={'table': dev_table,  **row})
        res = requests.post(c_table_json_url, data={'table': dev_table,  **row})

        










