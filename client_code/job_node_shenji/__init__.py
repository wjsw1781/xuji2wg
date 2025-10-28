from ._anvil_designer import job_node_shenjiTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil

from ..utils import *


from ..FilterBar import FilterBar


class job_node_shenji(job_node_shenjiTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.grid = nearest_datagrid(self)
        self.repeat = self.grid.get_components()[1]

        self.table_name = self.__class__.__name__
        self.table_obj = getattr(app_tables, self.table_name)

        if "page_by_route_url" in properties:
            # 额外的操作 必须禁止 移除 或者额外请求一些东西添加一些组件  左右分栏
            self.nav_1.remove_from_parent()
            pass
        self.add_component(FilterBar(self), index=0)
