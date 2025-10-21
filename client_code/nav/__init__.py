from ._anvil_designer import navTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class nav(navTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    def primary_color_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('job')

    def primary_color_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('node')
