import json
import os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from datetime import datetime
from initialization import chrome_initialization
from login import login
from config import config
from reservation import reservation

# 初始化浏览器
driver = chrome_initialization()

# 读取配置文件
config = config()

# 登录预约系统
login(driver, config)

while True:
    try:
        reservation(driver, config)  # 调用 reservation 函数
        # 等待页面中出现指定的成功消息元素，表示预约成功
        success_message_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert-success'))
        )

        print("已成功预约")
        
        break
    except:
        # 如果没有出现成功消息元素，重新尝试预约
        print("预约失败，重新尝试")

time.sleep(10)
driver.quit()