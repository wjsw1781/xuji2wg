



# -*- coding: utf-8 -*-

from tqdm import tqdm
import subprocess, time,os,sys,json,random,ipaddress
from loguru import logger
from crud.utils import *
import asyncio

table1_imei = 'app_tables.imei_node'
table2_job = 'app_tables.job'
table3_wg = 'app_tables.wg_node_0000'

table4_m2m='app_tables.job_node'

"""
curl 10.96.1.228:9627/shell/getDeviceId
"""
import subprocess

所有的分配wg手机节点映射关系 = subprocess.check_output(
    f"""
        wg show all dump   | grep -v 10_97_0_3 | grep -v -E '\(none\).*\(none\)'
    """,
    shell=True
).decode('utf-8').strip().split('\n')



headers = ["interface", "public_key", "preshared_key", "endpoint", "allowed_ips_peer_ip",'last_握手时间','接受字节','发送字节','心跳时间']
data = list(map(lambda x: x.split('\t'), 所有的分配wg手机节点映射关系))
data = list(filter(lambda x: len(x) == 9, data))


import pandas as pd,arrow
df = pd.DataFrame(data, columns=headers)

df['last_握手时间距离现在'] = df['last_握手时间'].apply(
    lambda ts: int(time.time()) - int(ts)
)
arrow_now = arrow.now()

def apply_last_握手时间(ts):
    if ts<60*10:
        return f'10 分钟内'
    else:
        moment = arrow_now.shift(seconds=-ts)
        return moment.humanize(locale='zh_cn')
    
df['last_握手_ago'] = df['last_握手时间距离现在'].apply(apply_last_握手时间)

# 统计字段 last_握手_ago 占比
print(   df.value_counts('last_握手_ago')   )



async def append_imei_async(df: pd.DataFrame):

    import asyncio,aiohttp

    async def fetch_imei_async(session, peerip, timeout=5):
        url = f'http://{peerip}:9627/shell/getDeviceId'
        try:
            async with session.get(url, timeout=timeout) as resp:
                return await resp.text()
        except Exception:
            return '获取 imei 失败'
        

    ips = df['allowed_ips_peer_ip'].str.split('/').str[0].tolist()
    
    async with aiohttp.ClientSession() as sess:
        tasks = [fetch_imei_async(sess, ip) for ip in ips]
        df['imei'] = await asyncio.gather(*tasks)

    return df

df = asyncio.run(append_imei_async(df))
print(    df.value_counts('imei')   )


cur.execute(f""" 
    select * from {table2_job} 
""")
all_jobs = cur.fetchall()
for job in all_jobs:
    if '全球 app 组网' != job['job_name']:
        # 删除
        cur.execute(f"""
            delete from {table2_job} where _id={job['_id']}
            """)
        conn.commit()


job = all_jobs[0]
job_table_id = get_table_id_in_anvil(table2_job)
job_pk = f'[{job_table_id},{job["_id"]}]'

# 删除所有 table4 等于这个 job 的
cur.execute(f"""
    delete from {table4_m2m} where job_id={job['_id']}
    """
)
conn.commit()
# 统计数量
cur.execute(f"""
    select count(*) from {table4_m2m}
    """)
print(cur.fetchall())





for data in df[(df['imei']!='获取 imei 失败') & (df['last_握手_ago']=='10 分钟内') ].to_dict('records'):
    allowed_ips_peer_ip = data['allowed_ips_peer_ip']
    imei_str = data['imei']
    peerip = allowed_ips_peer_ip.split('/')[0]

    cur.execute(f"""
        select * from {table1_imei} where imei_name='{imei_str}'
    """)
    imei = cur.fetchall()[0]
    table_imei_id = get_table_id_in_anvil(table1_imei)
    imei_pk = f'[{table_imei_id},{imei["_id"]}'

    cur.execute(f"""
        select * from {table3_wg} where wg_client_ip_name='{peerip}'
    """)
    peerip = cur.fetchall()[0]
    table_peerip_id = get_table_id_in_anvil(table3_wg)
    peerip_pk = f'[{table_peerip_id},{peerip["_id"]}'




    # 插入到数据库
    cur.execute(f"""
                insert into {table4_m2m} (job_id,imei_id,node_0000_id,status_node) values ('{job_pk}','{imei_pk}','{peerip_pk}','已分配')
        """)
    conn.commit()










