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
        # 修改外键 id 为具体的内容
        # print(self.item)
        for key in self.item:
            value = self.item[key]
            if str(value) == '<LiveObject: anvil.tables.Row>':
                all_key = list(dict(value).keys())
                key_name = None
                for name_find in all_key:
                    if 'name'  in name_find:
                        key_name = name_find
                        break
                if key_name:
                    self.item[key] =  self.item[key][key_name] 


        # Any code you write here will run before the form opens.

