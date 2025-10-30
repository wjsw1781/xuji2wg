
import psycopg2, random, string, json
import psycopg2.extras          # 这行必须有


# ─── 0. 连接 ───────────────────────────────────────────────
conn = psycopg2.connect(
    dbname   ="anvildb",
    user     ="anvil_user",
    password ="VerySecret!",
    host     ="127.0.0.1",
    port     =25332,
    cursor_factory=psycopg2.extras.RealDictCursor   # 关键点

)
conn.autocommit = True
cur = conn.cursor()

table_prefix = 'app_tables'
# 打印所有表名
cur.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema='{table_prefix}';")
table_names = cur.fetchall()
table_names_import = []

for table_one in table_names:
    # 获取这个表的列名用 f""
    table_one = dict(table_one)['table_name']
    cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_one}';")
    column_names = list(map(dict,cur.fetchall()))
    print(f"""

    表名: {table_prefix}.{table_one}
    列名: {column_names}
    """)
    table_names_import.append(f"{table_prefix}.{table_one}")



# anvil 运行时维护的对象 pip install anvil 
import anvil.server
from anvil.tables import app_tables
KEY = "server_G5LS4NKQI44CSJSY73GRKMRG-F4ZBMGWQBKSHSVYA"
ws_url = "ws://localhost:59001/_/uplink"
anvil.server.connect(KEY,url = ws_url)


print('wss success')


def get_table_id_in_anvil(table_name):
    dev_table = table_name.split('.')[-1]
    getattr(app_tables, dev_table)
    table_id = app_tables.cache[dev_table]._spec['id'][1]
    return table_id

def get_table_obj_in_anvil(table_name):
    dev_table = table_name.split('.')[-1]
    table_obj = getattr(app_tables, dev_table)
    return table_obj

# 删除表
def drop_table(table_name):
    cur.execute(f"""
        select count(*) from {table_name}
        """)
    print(cur.fetchall())
    
    cur.execute(f"""
            delete from {table_name} 
        """
    )
    conn.commit()

    # 统计数量
    cur.execute(f"""
        select count(*) from {table_name}
        """)
    print(cur.fetchall())
    