from ._anvil_designer import up_dataant_infoTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil


# 动态表单

def quick_add_row(grid):
    """
  弹出⼀个临时对话框，根据传⼊ DataGrid 的列动态⽣成若干 TextBox，
  返回用户填写好的 dict；如果点 Cancel / 关闭，则返回 None
  """
    # 1) 拿到列信息
    cols = [(c['data_key'], c['title'])
            for c in grid.columns
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


def guess_table_by_keys(row_dict):
    """
    根据 row_dict 的 key 集合，在 app_tables 里找出最匹配的表
    返回 Tables.Table 对象或 None
    """
    keys = set(row_dict.keys())

    for name in dir(app_tables):
        tbl = getattr(app_tables, name)
        # 真正的 Table 对象同时满足下列两个条件
        if isinstance(tbl, tables.Table) and hasattr(tbl, "list_columns"):
            col_names = {c.name for c in tbl.list_columns()}
            if keys.issubset(col_names):
                # 找到第一张能覆盖所有 key 的表
                return tbl
    return None
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
        grid = find_in_descendants(cur.parent)
        if grid is not None:
            return grid
        # 如果没找到，就再向上一级
        cur = cur.parent
    return None

class up_dataant_info(up_dataant_infoTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    def add_one_row_click(self, **event_args):
        """This method is called when the button is clicked"""
        # 获取当前数据库表的名称和字段
        sender = event_args['sender'] 
        grid = nearest_datagrid(sender)

        row = quick_add_row(grid)
        print(row)
        print(guess_table_by_keys(row))
        self.repeating_panel_2.tag
        


    def query_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass
