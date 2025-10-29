
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


# 自定义路由 显示 1097 下面的一些节点
@anvil.server.route("/wg_node_0000_by_route", methods=["POST","GET"], authenticate_users=False)
def wg_node_0000_by_route(**kw):
    kw['condition_by_route']=True
    return anvil.server.FormResponse('wg_node_0000',**kw)


# 多对多显示数据 自定义路由
@anvil.server.route("/job_node_by_route", methods=["POST","GET"], authenticate_users=False)
def job_node_by_route():
    kw={}
    kw['condition_by_route']=True
    return anvil.server.FormResponse('job_node',**kw)





