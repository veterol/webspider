import json
import time
import os
import requests
import pandas as pd
import draw_world
import draw_china

def get_html(Url, header):
    try:
        r = requests.get(url=Url, headers=header)
        r.encoding = r.apparent_encoding
        status = r.status_code
        # 将原始数据类型转换为json类型，方便处理
        data_json = json.loads(r.text)
        print(status)
        return data_json
    except:
        print("爬取失败")


def get_data(data, info_list):
    # "date"
    info = pd.DataFrame(data)[info_list]
    today_data = pd.DataFrame([province["today"] for province in data])
    today_data.columns = ["today_" + i for i in today_data.columns]
    total_data = pd.DataFrame([province["total"] for province in data])
    total_data.columns = ["total_" + i for i in total_data.columns]
    return pd.concat([info, today_data, total_data], axis=1)


def save_data(data, name):
    """定义保存数据的函数"""
    # 保存的文件名名称
    file_name = name + "_" + time.strftime("%Y_%m_%d", time.localtime(time.time())) + ".csv"

    data.to_csv(file_name, index=None, encoding="utf_8_sig")

    # 检查是否保存成功，并打印提示文本
    if os.path.exists(file_name):
        print(file_name + " 保存成功")
    else:
        print('保存失败')

def days_data(url, headers):
    datas = get_html(url, headers)
    data_days = datas["data"]["list"]
    all_data = get_data(data_days, ["date"])
    save_data(all_data, "days")

def province_data(url, headers):
    datas = get_html(url, headers)
    data_province = datas["data"]["areaTree"][2]["children"]
    all_data = get_data(data_province, ["id", "name", "lastUpdateTime"])
    save_data(all_data, "today_province")

def world_data(url, headers):
    datas = get_html(url, headers)
    world_data = datas["data"]["areaTree"]
    worlds_data = get_data(world_data, ["id", "name", "lastUpdateTime"])
    save_data(worlds_data, "today_worlds")


if __name__ == "__main__":
    # 这里面有全世界的疫情数据，每个国家分为today[7]和total[6],国家的children就是各省/州
    url_world = "https://c.m.163.com/ug/api/wuhan/app/data/list-total"
    # 下面是各国的每日数据,通过修改url爬取不同国家的data
    url = "https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode=6&t=1637505196126"
    # 设置请求头，伪装为浏览器
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    }
    # 这是某个国家的每日数据，可以生成折线图
    days_data(url, headers)
    # 这是各个省份当前的数据
    province_data(url_world, headers)
    # 世界总体疫情信息
    world_data(url_world, headers)

    # 画图
    draw_world.draw_world_map()
    draw_china.draw_china()


