from ._anvil_designer import z_jiankongTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js import window
import math, random


class z_jiankong(z_jiankongTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # 空曲线
              # 最多保留的点数

        self.plot_1.data = [go.Scatter(x=[], y=[], mode='lines')]
        self.t = 0      # 自增时间

    def timer_1_tick(self, **e):
        y = math.sin(self.t/5) + random.random()*0.1
        # 关键：extend_traces(update_dict, trace_index_list, max_points)
        MAX =100
        self.plot_1.extend_traces(
            {"x": [[self.t]], "y": [[y]]},   # 只追加一个点
            [0],                             # 第 0 条曲线
        )

        self.t += 1
        # ② 如果想让坐标轴也跟着滚动（可选）
        if self.t >= MAX:
            self.plot_1.relayout({"xaxis.range":[self.t-MAX+1, self.t]})
    