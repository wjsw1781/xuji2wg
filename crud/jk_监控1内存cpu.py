

from utils import *





"""


    表名: app_tables.sys_status
    列名: [{'column_name': '_id'}, {'column_name': 'host'}, {'column_name': 'cpu'}, {'column_name': 'memery'}, {'column_name': 'ts'}]
    

"""

import pandas as pd
import psutil,socket
import time
import datetime
import sqlalchemy as sa


engine = sa.create_engine("postgresql://anvil_user:VerySecret!@127.0.0.1:25332/anvildb")   # 改成自己的

import os, socket
HOST = (
    os.getenv("HOSTNAME")            # Docker/K8s 通常会有
    or socket.gethostname()          # 普通 Linux/macOS
    or socket.getfqdn()              # FQDN 兜底
)
TBL  = "sys_status"  



while True:
    row = {
        "host":   HOST,
        "cpu":    psutil.cpu_percent(interval=None),               # %
        "memery": psutil.virtual_memory().percent,                 # %
        "ts":     datetime.datetime.utcnow()                       # timestamptz
    }

    pd.DataFrame([row]).to_sql(TBL, engine,
                               schema="app_tables",
                               if_exists="append",
                               index=False)

    time.sleep(5)     # 5 秒采一次



