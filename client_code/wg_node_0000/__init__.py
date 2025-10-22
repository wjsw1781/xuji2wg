from ._anvil_designer import wg_node_0000Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil

from ..utils import *




class wg_node_0000(wg_node_0000Template):
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
                if 'http' in text:
                    node.innerHTML = f'<a href="{text}" target="_blank" >{text}</a>'
                    
                # 图片处理
                if 'img' in (col_info.get('data_key') or ''):
                    b64 = (comp.text or "").strip()
    

                    # 1) 生成一个 Link 组件替换掉原来的 Label
                    btn = anvil.Button(text="查看图", tooltip="点击查看原图")
                    # 3) 用同一列位置替换组件
                    row_tpl.add_component(btn, column=col_info['id'])
                    comp.remove_from_parent()  

    

                    # 2) 单行省略号 + 定宽 70px
                    # link.set_event_handler(
                    #     "click",
                    #     lambda **e, l=link: anvil.alert(
                    #         anvil.Image(source=f"data:image/png;base64,{l.tag.b64}",
                    #                     max_height=400, max_width=400),
                    #         large=True,
                    #         title="查看图片")
                    # )

         # 把旧的 Label 删掉       
        
            

        # 产生自动下拉框
        self.dropdowns = {}  # {字段名: DropDown}
        if self.rows:
            filter_row = FlowPanel()
            for col in dict(self.rows[0]).keys():  # 每一个字段
                dd = DropDown(placeholder=col,width=100)
                dd.items = [("全部", None)] + [  # 去重后的唯一值
                    (str(v), v)
                    for v in sorted({r[col] for r in self.rows if r[col] is not None})
                ]
                filter_row.add_component(dd)
                self.dropdowns[col] = dd
            self.add_component(filter_row,index = 0)

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
