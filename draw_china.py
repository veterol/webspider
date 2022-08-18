import time
import json
import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.charts import Bar, Map, Line, Pie

# from pyecharts.globals import CurrentConfig, NotebookType
# CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_LAB


# 加载数据，
data = pd.read_csv("./today_province_2021_11_18.csv")

# 查看该数据的头五行部分，初步了解
# data.head()

# 填充空值
data = data.fillna(0)

# 查看填充后数据的最后五行
# data.tail()

# 这里也是地图可视化需要的数据

# 将提取的数据进行排序

total_data = data[["name", "total_confirm"]].sort_values(by="total_confirm", ascending=False)
# print(total_data[:5])

map = (
    Map()
    .add("累计确诊人数", [list(z) for z in zip(total_data["name"], total_data["total_confirm"])], "china")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="中国各省新冠确诊人数数据可视化"),
        legend_opts=opts.LegendOpts(is_show=False),
        visualmap_opts=opts.VisualMapOpts(
            type_="color",
            min_=np.min(total_data["total_confirm"].tolist()),
            max_=np.max(total_data["total_confirm"].tolist()),
            range_text=["High", "Low"],
            is_piecewise=True,
            # split_number = 5,
            pieces=[{"min": 0, "max": 100, "label": "< 100"}, {"min": 100, "max": 500, "label": "100 - 500"},
                    {"min": 500, "max": 1000, "label": "500 - 1000"},
                    {"min": 1000, "max": 10000, "label": "1000 - 10000"},
                    {"min": 10000, "max": 20000, "label": "10000 - 20000"}, {"min": 20000, "label": "> 20000"}]),
    )

)

# map.render_notebook()
# map.render(path='./china.html')


def draw_china():
    map.render(path='./china.html')
