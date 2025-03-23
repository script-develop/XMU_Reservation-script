#这是预约的关键函数
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def make_reservation(driver,desired_time_slot,phonenumber):
    # 等待并点击游泳馆预约链接
    gym_reservation_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/room/2" and @title=""]')))
    gym_reservation_link.click()

    # 等待页面加载完成
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'slot-list')))

    # 获取页面中的所有日期元素
    slot_list_items = driver.find_elements(By.XPATH, '//li[contains(@class, "slot")]')
    available_dates = []

    # 遍历所有日期并提取
    for slot_item in slot_list_items:
        date_info = slot_item.find_element(By.CLASS_NAME, "date-info").text.strip()
        available_dates.append(date_info)

    # 将日期按升序排序
    available_dates = sorted(set(available_dates))  # 去重并排序

    # 获取最新的日期
    latest_date = available_dates[-1]
    print(f"最新日期是: {latest_date}")

    # 将时间段作为参数传入
    desired_time_slot = desired_time_slot

    # 在页面中查找对应日期的时间段并进行点击
    for slot_item in slot_list_items:
        date_info = slot_item.find_element(By.CLASS_NAME, "date-info").text.strip()
        
        # 如果找到最新日期
        if date_info == latest_date:
            # 查找该日期下的所有可预约时间段
            time_slots = slot_item.find_elements(By.XPATH, './/span[@class="time-slot"]/a')
            
            # 遍历所有时间段，找到匹配的时间段并且是可预约的（排除 "closed"）
            for time_slot in time_slots:
                if time_slot.text.strip() == desired_time_slot:
                    # 如果找到匹配的可预约时间段，点击并退出循环
                    time_slot.click()
                    print(f"即将预约时间段: {desired_time_slot} 在 {latest_date}")
                    break
            break

    # 等待页面跳转或确认已预约成功
    time.sleep(3)

  
    text_to_input = phonenumber  # 从配置文件中读取手机号码

    # 查找文本框并输入字符
    input_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "edit-field-tel-und-0-value")))
    input_box.send_keys(text_to_input)
    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "edit-submit")))
    login_button.click()

    while True:
        try:
            make_reservation()
            # 等待页面中出现指定的成功消息元素，表示预约成功
            success_message_element = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'alert-success'))
            )

            print("已成功预约")
            
            break
        except:
            # 如果没有出现成功消息元素，重新尝试预约
            print("预约失败，重新尝试")

    time.sleep(10)
    driver.quit()
