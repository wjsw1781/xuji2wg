from ._anvil_designer import wg_node_0000Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil

from ..utils import *


from ..FilterBar import FilterBar

class wg_node_0000(wg_node_0000Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.grid = nearest_datagrid(self)
        self.repeat = self.grid.get_components()[1]
        
        self.table_name = self.__class__.__name__ 
        self.table_obj = getattr(app_tables, self.table_name)

        # 如果是通过自定义路由打开 只提取指定的数据  说白了就是不是全表显示
        condition_by_route = {}
        if 'condition_by_route' in properties:
            self.nav_1.remove_from_parent()
            condition_by_route = properties['condition_by_route']
            print(properties)
            
        self.add_component(FilterBar(self,{}), index=0)
 
