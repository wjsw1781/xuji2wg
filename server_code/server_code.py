
import anvil.tables as tables
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


from loguru import logger

@anvil.server.http_endpoint("/add", methods=["POST","GET"], authenticate_users=False)
def wg_server_public_ip_update(**kw):
    print(kw)
    data = anvil.server.request.body_json      # 这里拿到 JSON 数据
    return data



@anvil.server.http_endpoint("/c_table_json", methods=["POST","GET"], authenticate_users=False)
def update_table_json(**kw):
    logger.success(f'----->  {kw}' , )
    table = kw['table']
    kw.pop('table')

    table_obj = getattr(app_tables,table)
    
    row = table_obj.add_row(**kw)
    id  = row.get_id()  
    return_data = dict(row)
    return_data['id'] = id
    return return_data

@anvil.server.http_endpoint("/r_table_json", methods=["POST","GET"], authenticate_users=False)
def reade_table_json(**kw):
    logger.success(f'----->  {kw}' , )
    table = kw['table']
    kw.pop('table')

    table_obj = getattr(app_tables,table)
    row = table_obj.search(**kw)
    if not row:
        return []
    row = list(map(dict,row))
    return row


@anvil.server.http_endpoint("/u_table_json", methods=["POST","GET"], authenticate_users=False)
def update_table_json(**kw):
    data = anvil.server.request.body_json      # 这里拿到 JSON 数据
    id = data['id']
    data.pop('id')
    table = data['table']
    data.pop('table')

    table_obj = getattr(app_tables,table)
    row = table_obj.get(id=id)
    row.update(**data)
    return dict(row)




@anvil.server.http_endpoint("/d_table_json", methods=["POST","GET"], authenticate_users=False)
def delete_table_json(**kw):
    data = anvil.server.request.body_json      # 这里拿到 JSON 数据
    id = data['id']
    table = data['table']
    table_obj = getattr(app_tables,table)
    row = table_obj.get(id=id)
    row.delete()
    return dict(row)




    
