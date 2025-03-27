from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import re
import sys
sys.stdout = open('log.txt', 'w')

def easy_reservation(driver, config):

    reservation_type = config['reservation_type']

    if reservation_type == '健身房':
        # 等待并点击健身房预约链接
        reservation_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/room/1" and @title=""]')))
    elif reservation_type == '游泳馆':
        # 等待并点击游泳馆预约链接
        reservation_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/room/2" and @title=""]')))
    else:
        raise ValueError("Invalid reservation type")

    reservation_link.click()

    # 等待页面加载完成
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'slot-list')))

    # 计算 6 天后的日期，少一次遍历
    target_date = (datetime.now() + timedelta(days=6)).strftime("%Y-%m-%d")

    # 获取页面中的所有日期元素
    slot_list_items = driver.find_elements(By.XPATH, '//li[contains(@class, "slot")]')

    # 读取配置中用户期望的时间段
    desired_time_slot = config['desired_time_slot']  

    # 遍历所有日期块，找到最新日期的块
    for slot_item in slot_list_items:
        date_element = slot_item.find_element(By.CLASS_NAME, "date-info")
        date_text = date_element.text.strip()

        date_text = re.sub(r'\s?[（(].*[）)]', '', date_text)
        #date_text = date_text.split("(")[0]  # 取括号前的部分

        if date_text == target_date:  # 只匹配 6 天后的日期
            # 查找目标日期下的所有可预约时间段
            time_slots = slot_item.find_elements(By.XPATH, './/span[@class="time-slot"]/a')
            
            for time_slot in time_slots:
                if time_slot.text.strip() == desired_time_slot:
                    time_slot.click()
                    print(f"成功预约 {target_date} 的 {desired_time_slot}")
                    break
            else:
                print(f"目标时间 {desired_time_slot} 不可预约")
            break  # 找到目标日期后，不需要再遍历其他日期块
    else:
        print(f"页面上找不到 {target_date} 这一天的预约选项")


    text_to_input = config['phone_number']  # 从配置文件中读取手机号码
    # 查找文本框并输入字符
    input_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "edit-field-tel-und-0-value")))
    input_box.send_keys(text_to_input) #找输电话按钮的和确认按钮
    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "edit-submit")))
    login_button.click()
