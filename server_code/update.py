updateimport anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
# @anvil.server.route('/add',methods=['post'])
@anvil.server.http_endpoint("/add", methods=["POST","GET"], authenticate_users=False)
def wg_server_public_ip_update(**kw):
    data = anvil.server.request.body_json      # 这里拿到 JSON 数据
    return data



@anvil.server.http_endpoint("/add_table_json", methods=["POST","GET"], authenticate_users=False)
def update_table_json():
    data = anvil.server.request.body_json      # 这里拿到 JSON 数据
    return data

@anvil.server.http_endpoint("/update_table_json", methods=["POST","GET"], authenticate_users=False)
def update_table_json():
    data = anvil.server.request.body_json      # 这里拿到 JSON 数据
    return data

    
