total = len(app_tables.imei_node.search({}))
# 改成进度展示

data = []
index = 0
for i in self.table_obj.search():
    data.append(dict(i))
    index += 1
    if index%100 == 0:
        N
self.repeat.items  = list(reversed(data))
