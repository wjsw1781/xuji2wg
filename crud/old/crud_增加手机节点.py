



# -*- coding: utf-8 -*-

from tqdm import tqdm
import subprocess, time,os,sys,json,random,ipaddress
from loguru import logger
from utils import *

table = 'app_tables.imei_node'


"""
    列名: [{'column_name': '_id'}, {'column_name': 'imei'}, {'column_name': 'type_zhenji_or_xuji'}, {'column_name': 'imei_url'}]
"""

# 全量导入  业务就是这样 不要想着每次新增一点 方便设计业务
import pandas as pd 
csv_all_imei = './device_info.csv'




now = int(time.time())
print(now)
good_iemie = []
datas = pd.read_csv(csv_all_imei).to_dict('records')
for imei in datas:
    心跳时间戳 = imei['心跳时间戳']
    设备号 = imei['设备号']
    if now - 心跳时间戳//1000 > 60*60*24*3:
        continue

    good_iemie.append(imei)

process_bar = tqdm(total=len(good_iemie))

for i in range(len(good_iemie)):
    process_bar.update(1)
    imei = good_iemie[i]
    imei =imei['设备号'] 
    imei_url = f'https://dataant.alibaba-inc.com/device/?deviceId={imei}'

    # 如果存在就删除
    cur.execute(f"DELETE FROM {table} WHERE imei = '{imei}'")
    # 添加
    cur.execute(f"INSERT INTO {table} (imei,imei_url) VALUES (%s,%s)", (imei,imei_url))
    conn.commit()












