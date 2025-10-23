



# -*- coding: utf-8 -*-

from tqdm import tqdm
import subprocess, time,os,sys,json,random,ipaddress
from loguru import logger
from utils import *

# 对这个表进行 rtt 的数据上报 上报到 app_tables.wg_node_0000_status
src_table = 'app_tables.wg_node_0000'
tar_table = 'app_tables.wg_node_0000_status'


"""

    表名: app_tables.wg_node_0000
    列名: [{'column_name': '_id'}, {'column_name': 'wg_client_ip'}, {'column_name': 'wg_conf'}, {'column_name': 'public_key'}, {'column_name': 'private_key'}, {'column_name': 'wg_conf_img'}]

    表名: app_tables.wg_node_0000_status
    列名: [{'column_name': '_id'}, {'column_name': 'wg_node_0000'}, {'column_name': 'rtt'}, {'column_name': 'time_stamp'}, {'column_name': 'day'}]

"""

# 查询一次表中的数据 找到本机实际的 wgclient ip 批量 cur 上报
sql_query = f"select _id,wg_client_ip from {src_table} "
cur.execute(sql_query)

all_need_ping_ips = cur.fetchall()


import asyncio, re, datetime, psycopg2.extras as pe
rx  = re.compile(r'time[=<]\s*([0-9.]+)\s*ms') 
now = datetime.datetime.now()
sem = asyncio.Semaphore(1)                                  # 并发上限

ping_超时_或者不通 = 333

async def batch_ping(items, concurrency=100):
    sem = asyncio.Semaphore(concurrency)

    async def _one(row):
        ip = row['wg_client_ip']
        async with sem:
            p = await asyncio.create_subprocess_shell(
                    f'ping -c1 -W3 {ip}',
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.STDOUT)
            out, _ = await p.communicate()
            m = rx.search(out.decode() if out else '')
            row['rtt'] = float(m.group(1)) if m else ping_超时_或者不通
            return row

    return await asyncio.gather(*[ _one(r) for r in items ])
# ------------------------------------------------------------------

# 在同步代码里调用
nid_rtt_pairs = asyncio.run(batch_ping(all_need_ping_ips))  

vals = [(row['_id'], row['rtt'], now, now.strftime('%Y-%m-%d')) for row in nid_rtt_pairs] 

pe.execute_values(cur, f"INSERT INTO {tar_table} (wg_node_0000, rtt, time_stamp,day) VALUES %s", vals)



