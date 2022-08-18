import os
import shutil
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import random
# 用来截图的，后来感觉直接截图更方便就没用了
try:
    driver = webdriver.Chrome(r"D:\chromedriver_win32\chromedriver.exe")          # 自己现在并放到指定目录，需要自己修改
    picture_url = "./china.html"
    soup = BeautifulSoup(open("./china.html", encoding='utf-8'), features='html.parser')
    driver.get(picture_url)
    driver.maximize_window()

    print(dir(driver))

    time.sleep(1)

    soup.get_screenshot_as_file('./2.png')
    print("%s：截图成功！！！" % picture_url)
    driver.close()
except BaseException as msg:
    print(msg)
