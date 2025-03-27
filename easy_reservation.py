from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def easy_reservation(driver, config):

    reservation_type = config['reservation_type']

    if reservation_type == 'gym':
        # 等待并点击健身房预约链接
        reservation_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/room/1" and @title=""]')))
    elif reservation_type == 'swim':
        # 等待并点击游泳馆预约链接
        reservation_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/room/2" and @title=""]')))
    else:
        raise ValueError("Invalid reservation type")

    reservation_link.click()

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
    desired_time_slot = config['desired_time_slot']  # 从配置文件中读取时间段

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

    # 等待页面加载并找到文本框元素（假设这里是 ID 为 'inputBox' 的文本框）
    text_to_input = config['phone_number']  # 从配置文件中读取手机号码

    # 查找文本框并输入字符
    input_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "edit-field-tel-und-0-value")))
    input_box.send_keys(text_to_input)
    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "edit-submit")))
    login_button.click()
