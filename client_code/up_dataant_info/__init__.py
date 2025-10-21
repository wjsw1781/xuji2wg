from ._anvil_designer import up_dataant_infoTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil



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
            data[c['data_key']] = ""
        return data

    if isinstance(row_dict, anvil.DataGrid):
        row_dict = get_scahma_by_grid(row_dict)
        
    row_set = set(row_dict.keys())
    for table, cols in schema_map.items():
        if row_set == set(cols):          # 完全一致（忽略顺序）
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
        
        if not row:
            return
            
        table_name = find_table_exact(row,all_table_scahma)

        table_obj = getattr(app_tables,table_name)

        table_obj.add_row(**row)


    def query_click(self, **event_args):
        sender = event_args['sender'] 
        grid = nearest_datagrid(sender)
        table_name = find_table_exact(grid,all_table_scahma)
        print(table_name)

        
        
        pass

