import psycopg2, random, string, json
from psycopg2 import sql

# ─── 0. 连接 ───────────────────────────────────────────────
conn = psycopg2.connect(
    dbname   ="anvildb",
    user     ="anvil_user",
    password ="VerySecret!",
    host     ="127.0.0.1",
    port     =25332,
)
conn.autocommit = True
cur = conn.cursor()

# ─── 1. 动态获取 app_tables 下所有表名 ─────────────────────
cur.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'app_tables'
    ORDER BY table_name;
""")
tables = [r[0] for r in cur.fetchall()]
print("发现表：", tables)

# ─── 2. 遍历每张表 ─────────────────────────────────────────
for t in tables:
    full_tbl = sql.Identifier('app_tables', t)
    print(f"\n\n\n\n\n====== {t} ======")

    # 2.1 列字段
    cur.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_schema='app_tables' AND table_name=%s
        ORDER BY ordinal_position;
    """, (t,))
    cols = cur.fetchall()

    print("字段:")
    for name, dtype, *_ in cols:
        print("  ", name)

    # 2.4 统计总数
    cur.execute(sql.SQL("SELECT COUNT(*) FROM {}").format(full_tbl))
    print("总数:", cur.fetchone()[0])

# 

# ─── 3. 结束 ──────────────────────────────────────────────
cur.close()
conn.close()
print("\n✅  脚本执行完毕")
