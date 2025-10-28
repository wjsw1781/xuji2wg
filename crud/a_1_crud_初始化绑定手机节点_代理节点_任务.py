from itertools import cycle
mobiles = [1, 2, 3, 4, 5]           # 5 台手机
proxies = [101, 102]                # 2 个代理

pairs = list(zip(mobiles, cycle(proxies)))

for mobile, proxy in pairs:
    print(f"手机 {mobile} 绑定代理 {proxy}")


from utils import *

# http://127.0.0.1:9627/shell/getDeviceId

"""

    表名: app_tables.imei_node
    列名: [{'column_name': '_id'}, {'column_name': 'type_zhenji_or_xuji'}, {'column_name': 'imei_url'}, {'column_name': 'imei_name'}]

"""

# 提取所有的 imei 数据
sql = f"select * from app_tables.imei_node"
cur.execute(sql)
imei_nodes = cur.fetchall()
print(imei_nodes)
