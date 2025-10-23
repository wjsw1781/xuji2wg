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
    total = len(self.table_obj.search())
    data = []
    index = 0
    for i in self.table_obj.search():
        data.append(dict(i))
        index += 1
        if index%500 == 0:
            Notification(f'进度 {index} / {total}').show()
            
    self.repeat.items  = list(reversed(data))
    cache_data[table_name] = self.repeat.items 
    pass