from ._anvil_designer import z_jiankongTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from anvil import Plot
import plotly.graph_objs as go

import random


_TRACE_MAP = {
    "line": go.Scatter,      # 折线/散点
    "bar":  go.Bar,          # 柱状
    "pie":  go.Pie,          # 饼
    "hist": go.Histogram     # 直方
}

class ChartWidget(Plot):
    """
    spec = {
       "type":   "line" | "bar" | "pie" | "hist",
       "series": [ {...}, {...} ],
       "layout": { ... }                 # 可省
    }
    series 元素：
      折线/柱状/直方 : { "x": [...], "y": [...], "name": "可省" }
      饼图          : { "labels": [...], "values": [...], "name": "可省" }
    """
    def __init__(self, spec, **props):
        trace_cls = _TRACE_MAP[spec["type"]]
        traces = []

        for s in spec["series"]:
            # 饼图专用字段不同，单独处理
            if spec["type"] == "pie":
                traces.append(trace_cls(labels=s["labels"],
                                        values=s["values"],
                                        name=s.get("name")))
            # 直方图
            elif spec["type"] == "hist":
                traces.append(trace_cls(x=s["x"], name=s.get("name")))
            # 折线图柱状图随时间变化
            else:
                traces.append(trace_cls(x=s["x"], y=s["y"],
                                        name=s.get("name"),
                                        mode="lines+markers" if spec["type"]=="line" else None))
        
        super().__init__(data=traces, layout=spec.get("layout", {}),**props)







class z_jiankong(z_jiankongTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

        # -------------- 1) 单折线：最近 10 分钟 RTT
        spec_line = {
            "type": "line",
            "series": [
                { "x": list(range(10)), "y": [42,58,33,40,45,39,60,55,49,52] }
            ]
        }
        
        # -------------- 2) 双折线：CPU vs MEM
        spec_double_line = {
            "type": "line",
            "series": [
                { "x": list(range(6)), "y": [30,45,55,50,40,35], "name":"CPU%" },
                { "x": list(range(6)), "y": [2.1,2.3,2.8,2.5,2.4,2.2], "name":"MEM GB" }
            ]
        }
        
        # -------------- 3) 单柱状：今天各接口错误次数
        spec_bar = {
            "type": "bar",
            "series": [
                { "x": ["auth","pay","query"], "y": [5, 12, 3] }
            ]
        }
        
        # -------------- 4) 双柱状：不同机房 QPS 对比
        spec_multi_bar = {
            "type": "bar",
            "series": [
                { "x": ["00:00","01:00","02:00"], "y": [1200,1100,900],  "name":"idc-A" },
                { "x": ["00:00","01:00","02:00"], "y": [1500,1400,1000], "name":"idc-B" }
            ]
        }
        
        # -------------- 5) 饼图：BUG 类型分布
        spec_pie = {
            "type": "pie",
            "series": [
                { "labels": ["UI","Server","DB","Other"], "values": [23,45,12,5] }
            ]
        }
        
        # -------------- 6) 直方图：接口响应时间分布
        spec_hist = {
            "type": "hist",
            "series": [
                {"x": [random.gauss(300, 50) for _ in range(400)]}
            ],
            "layout": {"title": "Latency Histogram (ms)"}
        }


        
        # 折线
        self.add_component(ChartWidget(spec_line, height=300))
        # 双折线
        self.add_component(ChartWidget(spec_double_line, height=300))
        # 单柱状
        self.add_component(ChartWidget(spec_bar, height=250))
        # 双柱状
        self.add_component(ChartWidget(spec_multi_bar, height=250))
        # 饼图
        self.add_component(ChartWidget(spec_pie, height=300, width=300))
        # 直方
        self.add_component(ChartWidget(spec_hist, height=300))
