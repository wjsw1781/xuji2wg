from ._anvil_designer import wg_node_9898Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil

from ..utils import *


from ..FilterBar import FilterBar


class wg_node_9898(wg_node_9898Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.grid = nearest_datagrid(self)
        self.repeat = self.grid.get_components()[1]

        self.table_name = self.__class__.__name__
        self.table_obj = getattr(app_tables, self.table_name)

        # 头部筛选数据框
        self.add_component(FilterBar(self), index=0)



app_tables.wg_node_0000.search()