



# -*- coding: utf-8 -*-

from tqdm import tqdm
import subprocess, time,os,sys,json,random,ipaddress
from loguru import logger
from utils import *

table = 'app_tables.job'


"""
等待网络节点就绪 ⏳ (U+23F3)
成功 ✅ (U+2705)
失败 ❌ (U+274C)

列名: [{'column_name': '_id'}, {'column_name': 'job_name'}, {'column_name': 'job_status'}, {'column_name': 'job_many_to_many_url'}]
    
"""
job_name = '测试_采集海外app_越南'
job_status = '⏳'

# 如果存在就删除
cur.execute(f"DELETE FROM {table} WHERE job_name = '{job_name}'")
# 添加
cur.execute(f"INSERT INTO {table} (job_name, job_status) VALUES ('{job_name}', '{job_status}')")
conn.commit()
