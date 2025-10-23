from ._anvil_designer import imei_nodeTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil

from ..utils import *


from ..FilterBar import FilterBar


class imei_node(imei_nodeTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.grid = nearest_datagrid(self)
        self.repeat = self.grid.get_components()[1]

        self.table_name = self.__class__.__name__
        self.table_obj = getattr(app_tables, self.table_name)

        self.repeat.items = list(map(dict,self.table_obj.search()))

        self.rows = self.repeat.items

        # 头部筛选数据框
        self.add_component(FilterBar(self.rows, self.update_table,self.on_new), index=0)
        self.update_table(self.rows)

    def on_new(self,dict):
        self.table_obj.add_row(**dict)
        self.rows+=[dict]
        self.update_table(self.rows)
        
    def update_table(self, filtered_rows):
        self.repeat.items = filtered_rows

        # 样式控制 文字单元格太长都省略掉
        for row_tpl in self.repeat.get_components():
            row_comps = row_tpl.get_components()
            cols = self.grid.columns
            for comp in row_comps:
                col_index = row_comps.index(comp)
                col_info = cols[col_index]
                if not isinstance(comp, anvil.Label):
                    continue

                node = anvil.js.get_dom_node(comp).querySelector("span")

                # 文本处理
                node.style.whiteSpace = "nowrap"
                node.style.overflow = "hidden"
                node.style.textOverflow = "ellipsis"
                node.style.maxWidth = "70px"

                # 超链接处理
                text = node.innerHTML or ""
                if "http" in text:
                    node.innerHTML = f'<a href="{text}" target="_blank" >{text}</a>'

                # 图片处理
                if "img" in (col_info.get("data_key") or ""):
                    b64 = (comp.text or "").strip()
                    src = f"data:image/png;base64,{b64}"

                    # 1) 生成一个 btn 组件替换掉原来的 Label
                    btn = anvil.Button(text="查看图", tooltip="点击查看原图")
                    btn.set_event_handler(
                        "click", lambda **x: alert(anvil.Image(source=src))
                    )

                    # 3) 用同一列位置替换组件
                    row_tpl.add_component(btn, column=col_info["id"])
                    comp.remove_from_parent()
