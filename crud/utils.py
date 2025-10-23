
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
print(table_names)

for table_one in table_names:
    # 获取这个表的列名用 f""
    table_one = dict(table_one)['table_name']
    cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_one}';")
    column_names = list(map(dict,cur.fetchall()))
    print(f"""

    表名: {table_prefix}.{table_one}
    列名: {column_names}

    """)
