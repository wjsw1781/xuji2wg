from ._anvil_designer import z_jiankongTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from plotly import graph_objs as go
import datetime
import random


class z_jiankong(z_jiankongTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

            # Any code you write here will run before the form opens.
        # 1) 生成 100 条假数据
        n = 100
        x_vals = [datetime.datetime.utcnow() - datetime.timedelta(minutes=i)
                for i in reversed(range(n))]
        y_vals = [random.uniform(20, 80) for _ in range(n)]
    
        # 2) 构造 Plotly trace 和 layout
        trace  = go.Scatter(x=x_vals, y=y_vals,
                            mode="lines+markers",
                            name="RTT (ms)")
        layout = go.Layout(title="Simulated RTT",
                        xaxis=dict(title="Time"),
                        yaxis=dict(title="RTT (ms)"))
    
        # 3) 动态创建 Plot 组件并加入界面
        plot = Plot(data=[trace], layout=layout,
                    width="100%", height=400)   # 可调尺寸
        self.add_component(plot)                # 放到当前 Form 的最底部