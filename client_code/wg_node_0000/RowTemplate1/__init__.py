from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate1(RowTemplate1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    def primary_color_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        cp = anvil.ColumnPanel()     # 临时容器
    
        for key, b64 in self.item.items():
            if 'img' not in  key:                     # 空值跳过
                continue
            # 如果字段里存的是纯 base64 字符串（不含 data:image/png;base64, 前缀）
            src = f"data:image/png;base64,{b64}"
    
            img = anvil.Image(source=src, height=200)
            lbl = anvil.Label(text=key, align='center')
    
            cp.add_component(lbl)
            cp.add_component(img)
    
        anvil.alert(cp, large=True, title="二维码/图片", buttons=[("关闭", False)])
