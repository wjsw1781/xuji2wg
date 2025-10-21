from ._anvil_designer import up_dataant_infoTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil

from ..utils import *




class up_dataant_info(up_dataant_infoTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.grid = nearest_datagrid(self)
        self.repeat = self.grid.get_components()[1]
        self.table_name = find_table_exact(self.grid,all_table_scahma)
        self.table_obj = getattr(app_tables,self.table_name)
        
        self.repeat.items = list(self.table_obj.search())



    def add_one_row_click(self, **event_args):
        """This method is called when the button is clicked"""
        # 获取当前数据库表的名称和字段

        row = quick_add_row(self.grid)
        
        if not row:
            return
            
        self.table_obj.add_row(**row)
        
        self.grid.get_components()[1].items = list(self.table_obj.search())


    def query_click(self, **event_args):
        self.grid.get_components()[1].items = list(self.table_obj.search())









