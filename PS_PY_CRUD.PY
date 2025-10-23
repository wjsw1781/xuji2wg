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
    print(f"\n====== {t} ======")

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

    # 2.2 计算需要显式赋值的列（非系统列、NOT NULL、无默认）
    need_cols, need_vals = [], []
    for name, dtype, nullable, default in cols:
        if name.startswith('_'):          # 跳过 _row_id,_created 等系统列
            continue
        if nullable == 'YES' or default:
            continue                      # 可空或有默认值，跳过
        need_cols.append(sql.Identifier(name))
        # 给必填字段准备简单示例值
        if dtype in ('integer', 'bigint', 'smallint'):
            need_vals.append(sql.Literal(random.randint(1, 100)))
        elif dtype in ('boolean',):
            need_vals.append(sql.Literal(True))
        else:                             # text、varchar、json、timestamp等
            sample = 'demo_' + ''.join(random.choices(string.ascii_lowercase, k=5))
            need_vals.append(sql.Literal(sample))

    # 2.3 插入
    if need_cols:
        ins = sql.SQL("INSERT INTO {tbl} ({cols}) VALUES ({vals}) RETURNING _row_id").format(
            tbl=full_tbl,
            cols=sql.SQL(',').join(need_cols),
            vals=sql.SQL(',').join(need_vals),
        )
    else:
        ins = sql.SQL("INSERT INTO {tbl} DEFAULT VALUES RETURNING _row_id").format(tbl=full_tbl)

    cur.execute(ins)
    row_id = cur.fetchone()[0]
    print("插入 _row_id =", row_id)

    # 2.4 查询整表
    cur.execute(sql.SQL("SELECT * FROM {tbl}").format(tbl=full_tbl))
    rows = cur.fetchall()
    print("所有记录:", rows)

    # 2.5 找第一个文本列做 UPDATE（如果有）
    text_col = None
    for name, dtype, *_ in cols:
        if not name.startswith('_') and dtype in ('text', 'character varying'):
            text_col = name
            break
    if text_col:
        upd = sql.SQL("UPDATE {tbl} SET {col}=%s WHERE _row_id=%s").format(
            tbl=full_tbl, col=sql.Identifier(text_col)
        )
        cur.execute(upd, ('updated', row_id))
        print("更新行数:", cur.rowcount)
    else:
        print("无文本列可更新，跳过 UPDATE")

    # 2.6 删除刚才插入的行
    cur.execute(sql.SQL("DELETE FROM {tbl} WHERE _row_id=%s").format(tbl=full_tbl),
                (row_id,))
    print("删除行数:", cur.rowcount)

# ─── 3. 结束 ──────────────────────────────────────────────
cur.close()
conn.close()
print("\n✅  脚本执行完毕")
