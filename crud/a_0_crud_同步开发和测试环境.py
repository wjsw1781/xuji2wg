



# -*- coding: utf-8 -*-

from tqdm import tqdm
import subprocess, time,os,sys,json,random,ipaddress
from loguru import logger

from utils import *

sync_num = 10


import anvil.server
import anvil.media
from anvil.tables import app_tables
anvil.server.connect("server_G5LS4NKQI44CSJSY73GRKMRG-F4ZBMGWQBKSHSVYG")



for pro_table in table_names_import:
    print('正在同步 -----> ', pro_table)
    cur.execute(f"select * from {pro_table} limit {sync_num}")
    data = cur.fetchall()


    dev_table = pro_table.split('.')[-1]
    
    try:
        dev_table_obj = getattr(app_tables, dev_table)
    except:
        continue

    for index ,row in enumerate(tqdm(data)):
        if index > sync_num:
            break
        row = dict(row)
        row.pop('_id')

        # 先删后增
        if len(dev_table_obj.search(**row))>0:
            for old_row in dev_table_obj.search(**row):
                old_row.delete()

        dev_table_obj.add_row(**row)

        










