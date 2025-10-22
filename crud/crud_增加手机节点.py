



# -*- coding: utf-8 -*-

from tqdm import tqdm
import subprocess, time,os,sys,json,random,ipaddress
from loguru import logger


url_host = 'http://8.217.224.52:59001/_/api'

crud_c_url = f'{url_host}/c_table_json'
crud_r_url = f'{url_host}/r_table_json'
crud_u_url = f'{url_host}/u_table_json'
crud_d_url = f'{url_host}/d_table_json'

import requests


table = 'imei_node'


"""

imei
type_zhenji_or_xuji
imei_url
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
    if now - 心跳时间戳//1000 > 60*60*5:
        continue

    good_iemie.append(imei)


for imei in good_iemie:
    imei =imei['设备号'] 
    data ={
        "table": table,
        'imei':imei,
        'imei_url':f'https://dataant.alibaba-inc.com/device/?deviceId={imei}',
    }
    # 如果存在就删除
    requests.post(crud_d_url,data=data)
    requests.post(crud_c_url,data=data)








