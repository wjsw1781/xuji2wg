import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from .. import Module1
#
#    Module1.say_hello()
#


def say_hello():
    print("Hello, world")


import anvil
from anvil import *
import anvil.server


# 所有表
def get_all_table():
    try:
        app_tables.job1
    except :
        pass
    all_table_dict = {}

    for key in app_tables.cache:
        table_list = app_tables.cache[key].list_columns()
        table_key =[]

        for ii in table_list:
            table_key.append(ii['name'])
        table_key.sort()
        all_table_dict[key] = table_key
    return all_table_dict
all_table_scahma = get_all_table()


# 反向寻找dict key 通过 value 或者 grid
def find_table_exact(row_dict, schema_map):
    def get_scahma_by_grid(grid):
        data = {}
        for c in grid.columns:
            
            if 'column_' in c['data_key']:
                 continue
            
            data[c['data_key']] = ""
            
        return data

    if isinstance(row_dict, anvil.DataGrid):
        row_dict = get_scahma_by_grid(row_dict)

    row_set = set(row_dict.keys())
    # filter column_1
    row_set_good = []
    for col in row_set:
        if 'column_' not in col:
            row_set_good.append(col)
    row_set_good = set(row_set_good)       
    for table, cols in schema_map.items():
        if row_set_good == set(cols):          # 完全一致（忽略顺序）
            return table
    return None

# 动态表单
def quick_add_row(grid):
    """
  弹出⼀个临时对话框，根据传⼊ DataGrid 的列动态⽣成若干 TextBox，
  返回用户填写好的 dict；如果点 Cancel / 关闭，则返回 None
  """
    # 1) 拿到列信息
    cols = [(c['data_key'], c['title'])
            for c in grid.columns
            if 'column_' not in c['data_key']
           ]

    # 2) 临时拼⼀个 ColumnPanel，往里加 Label+TextBox
    panel   = ColumnPanel()
    inputs  = {}
    for dk, ttl in cols:
        panel.add_component(Label(text=ttl))
        tb = TextBox()
        panel.add_component(tb)
        inputs[dk] = tb

    # 3) 弹对话框
    ok = alert(
        content=panel,
        title="新增记录",
        buttons=[("OK", True), ("Cancel", False)],
        large=False
    )

    if ok:
        # 收集⽤户输⼊
        return {k: tb.text for k, tb in inputs.items()}
    else:
        return None


# 最近的数据表组件 以及 scahma
def nearest_datagrid(comp):
    def find_in_descendants(container):
        """递归在 container 的所有后代里查找 DataGrid"""
        if container is None:
            return None
        # container 可能没有 get_components（例如 DataRow）
        for c in getattr(container, 'get_components', lambda: [])():
            if isinstance(c, anvil.DataGrid):
                return c
            res = find_in_descendants(c)
            if res is not None:
                return res
        return None

    cur = comp
    if isinstance(cur, anvil.DataGrid):
        return cur

    while cur is not None:
        grid = find_in_descendants(cur)
        if grid is not None:
            return grid
        # 如果没找到，就再向上一级
        cur = cur.parent
    return None


# 缓存数据

cache_data = {}

def list_add_self_items(self):
    table_name = self.__class__.__name__ 
    
    if table_name in cache_data:
        self.repeat.items = cache_data[table_name]
        return
        
    # 进行网络请求     # 改成进度展示

    total = len(app_tables.imei_node.search({}))
    data = []
    index = 0
    for i in self.table_obj.search():
        data.append(dict(i))
        index += 1
        if index%100 == 0:
            Notification(f'进度 {index} / {total}')
    self.repeat.items  = list(reversed(data))
    cache_data[table_name] = self.repeat.items 
    pass