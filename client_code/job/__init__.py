from ._anvil_designer import jobTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil

from ..utils import *


class job(jobTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.grid = nearest_datagrid(self)
        self.repeat = self.grid.get_components()[1]

        self.table_name = self.__class__.__name__
        self.table_obj = getattr(app_tables, self.table_name)

        self.repeat.items = list(self.table_obj.search())

        self.rows = self.repeat.items

        # 样式控制 文字单元格太长都省略掉
        for row_tpl in self.repeat.get_components():
            for comp in row_tpl.get_components():
                # 给 DOM 节点加 class
                if not isinstance(comp, anvil.Label):
                    continue

                node = anvil.js.get_dom_node(comp).querySelector("span")
                node.style.whiteSpace = "nowrap"
                node.style.overflow = "hidden"
                node.style.textOverflow = "ellipsis"
                node.style.maxWidth = "70px"

        # 产生自动下拉框
        self.dropdowns = {}  # {字段名: DropDown}
        if self.rows:
            filter_row = FlowPanel()
            for col in dict(self.rows[0]).keys():  # 每一个字段
                dd = DropDown(placeholder=col, width=100)
                dd.items = [("全部", None)] + [  # 去重后的唯一值
                    (str(v), v)
                    for v in sorted({r[col] for r in self.rows if r[col] is not None})
                ]
                filter_row.add_component(dd)
                self.dropdowns[col] = dd
            self.add_component(filter_row, index=0)

    def add_one_row_click(self, **event_args):
        """This method is called when the button is clicked"""
        # 获取当前数据库表的名称和字段

        row = quick_add_row(self.grid)

        if not row:
            return
        self.table_obj.add_row(**row)
        self.table_obj.list_columns()

        self.repeat.items = list(self.table_obj.search())

    def query_click(self, **event_args):
        cond = {
            c: dd.selected_value
            for c, dd in self.dropdowns.items()
            if dd.selected_value is not None
        }  # 只取被选择的字段

        self.repeat.items = list(
            self.table_obj.search(**cond) if cond else self.table_obj.search()
        )
