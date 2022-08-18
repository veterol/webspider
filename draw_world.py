import time
import json
import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.charts import Bar, Map, Line, Pie

# 加载数据
df = pd.read_csv("./today_worlds_2021_11_20.csv")
# 填充空值
df = df.fillna(0)

# 提取出我们需要的特征列
world_data = df[["name", "lastUpdateTime", "today_confirm", "total_confirm", "total_heal", "total_dead"]]
world_data.head()

# 将其取出后储存为 name_map
with open("./country.json", 'r') as f:
    name_map = json.load(f)
# type(world_data)
# def draw_world_map():
#     world_map.render(path='./world.html')


# 以下是世界地图的绘制
world_map = (
    Map()
    .add("累计新冠确诊",
         [list(z) for z in zip(world_data["name"].tolist(), world_data["total_confirm"].tolist())],
         "world", is_map_symbol_show=False, name_map=name_map)
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="世界各国新冠确诊累计分布图"),
#         visualmap_opts=opts.VisualMapOpts(max_=200),
        visualmap_opts=opts.VisualMapOpts(
            type_="color",
            min_=np.min(world_data["total_confirm"]),
            max_=np.max(world_data["total_confirm"]),
            range_text=["High","Low"],is_piecewise=True,
            pieces=[{"min": 0, "max": 100, "label": "< 100"},
                    {"min": 100, "max": 1000, "label": "100 - 1000"},
                    {"min": 1000, "max": 10000, "label": "1000 - 10000"},
                    {"min": 10000, "max": 30000, "label": "1万 - 3万"},
                    {"min": 30000, "max": 100000, "label": "3万 - 10万"},
                    {"min": 100000, "max": 200000, "label": "10万 - 20万"},
                    {"min": 200000, "max": 500000, "label": "20万 - 50万"},
                    {"min": 500000, "max": 1000000, "label": "50万 - 100万"},
                    {"min": 1000000, "max": 5000000, "label": "100万 - 500万"},
                    {"min": 5000000, "max": 20000000, "label": "500万 - 2000万"},
                    {"min": 20000000, "label": "> 2000万"}]),
    )
)
# world_map.render(path='./world.html')

# 对数据进行排序
total_worlds = world_data[["name", "total_confirm"]].sort_values(by="total_confirm", ascending=False)
# 以下是柱形图的绘制
bar = (
    Bar()
    .add_xaxis(total_worlds["name"].tolist())
    .add_yaxis("累计确诊", total_worlds["total_confirm"].tolist())
    .set_global_opts(
        # 图形标题的设置
        title_opts=opts.TitleOpts(
            title="世界各国累计新冠肺炎确诊病例",
            pos_left="center",
            pos_top="7%"),
        # 'shadow'：阴影指示器
        tooltip_opts=opts.TooltipOpts(
            is_show=True,
            trigger="axis",
            axis_pointer_type="shadow"),
        # 图例的设置
        legend_opts=opts.LegendOpts(pos_top="12%",pos_left="45%"),
        # 视觉映射配置项
        visualmap_opts=opts.VisualMapOpts(
            type_="color",
            min_=np.min(world_data["total_confirm"]),
            max_=np.max(world_data["total_confirm"]),
            range_text=["High", "Low"],),
        # x轴坐标配置项
        xaxis_opts=opts.AxisOpts(name="国家", axislabel_opts={"interval":"0"}),
        # y轴配置项
        yaxis_opts=opts.AxisOpts(
            name="总计", min_=0,
            type_="value", axislabel_opts=opts.LabelOpts(formatter="{value} 人"),),
        # 区域缩放配置项
        datazoom_opts=opts.DataZoomOpts(range_start=0, range_end=5),
    )
)
# bar.render(path='./bar.html')
def draw_world_map():
    world_map.render(path='./world.html')
    bar.render(path='./bar.html')
