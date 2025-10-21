from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


from ...utils import  * 


class RowTemplate2(RowTemplate2Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    def primary_color_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.item.delete()
        self.remove_from_parent()
