



# -*- coding: utf-8 -*-

from tqdm import tqdm
import subprocess, time,os,sys,json,random,ipaddress
from loguru import logger
from crud.utils import *

table2 = 'app_tables.job'
table1 = 'app_tables.imei_node'
table3 = 'app_tables.wg_node_0000'

table4='app_tables.job_node'

"""
"""

import pandas as pd 
csv_all_imei = '../颂元第一批96节点.txt'

with open(csv_all_imei, 'r') as f:
    all_imei = eval(f.read())

# 提取出所有的imei
sql = f"select * from {table1}"
cur.execute(sql)
imei_node = cur.fetchall()

imei_node = list(filter(lambda x: x['imei_name'] in all_imei, imei_node))

# 提取出所有路由节点
sql = f"select * from {table3}"
cur.execute(sql)
wg_node = cur.fetchall()

# 提取出所有任务
sql = f"select * from {table2}"
cur.execute(sql)
job = cur.fetchall()

from itertools import cycle
pairs = list(zip(cycle([job[0]]),wg_node, imei_node))

for pair in tqdm(pairs):
    job_id, wg_node_id, imei_node_id = pair
    # print(job_id['_id'], wg_node_id['_id'], imei_node_id['_id'],job_id['job_name'])
    print(job_id['job_name'], wg_node_id['wg_client_ip_name'], imei_node_id['imei_name'],job_id['job_name'])












