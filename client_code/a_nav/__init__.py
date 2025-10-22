from ._anvil_designer import a_navTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class a_nav(a_navTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    def primary_color_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('job')

    def primary_color_2_click(self, **event_args):
        """This method ia_
        s called when the button is clicked"""
        open_form('wg_node_0000')

    def primary_color_3_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('imei_node')
