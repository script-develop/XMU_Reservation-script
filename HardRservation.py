from datetime import datetime, timedelta
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import ddddocr
import sys
sys.stdout = open('log.txt', 'w')


def hard_reservation(driver, config):
    # 日期预处理，一个保留前导零访问网页，一个去掉访问子链接
    reservation_date = datetime.now() + timedelta(days=5)
    reservation_date_for_url = reservation_date.strftime("%m/%d")  # 这个可以正常使用
    reservation_date_for_xpath = reservation_date.strftime("%m/%d").lstrip('0').replace("/0", "/")  # 处理前导零

    #加载
    driver.get(f"https://cgyy.xmu.edu.cn/room_reservations/{reservation_date_for_url}")
  
    # 等待页面加载完毕（等待body元素加载出来）
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # 遍历 15 到 19，寻找可预约的乒乓球馆
    for i in range(6, 14):
        try:
            # 等待预约链接出现（动态加载时有效）
            reservation_links = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, f'//a[contains(@href, "/node/add/room-reservations-reservation/") and contains(@href, "/{reservation_date_for_xpath}/") and contains(@href, "/{i}")]')
                )
            )

            if reservation_links:
                first_link = reservation_links[0]
                reservation_url = first_link.get_attribute("href")
                print(f"找到可预约场地: {reservation_url}")

                # 立即点击预约
                driver.get(reservation_url)
                break  # 预约成功，停止循环
        except Exception as e:
            print(f"场地 {i} 预约失败或未找到链接，尝试下一个...")

    print("成功点击时间块")

     # 等待页面加载完成
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "edit-reservation-length-und")))
    
    # 找到下拉选择框并选择时间最长的选项
    select_element = Select(driver.find_element(By.ID, "edit-reservation-length-und"))
    options = select_element.options
    max_option = max(options, key=lambda option: int(option.get_attribute('value')))
    select_element.select_by_value(max_option.get_attribute('value'))
    
    print(f"选择了时间最长的选项: {max_option.text}")

    # 找到文本框元素并填写内容
    partner_id = config['partner_id']
    partner_name = config['partner_name']
    text_area = driver.find_element(By.ID, "edit-field-members-und-0-value")
    text_area.send_keys(f"{partner_id} {partner_name}")
    
    print(f"填写了文本框内容: {partner_id} {partner_name}")

    # 找到电话输入框元素并填写内容
    phone_number = config['phone_number']
    phone_input = driver.find_element(By.ID, "edit-field-telephone-und-0-value")
    phone_input.send_keys(phone_number)
    
    print(f"填写了电话输入框内容: {phone_number}")



    # 使用ddddocr识别验证码并提交，最多尝试5次
    ocr = ddddocr.DdddOcr()
    ocr.set_ranges(6)
    attempts = 0
    max_attempts = 5
    while attempts < max_attempts:
        # 找到图形验证码图片元素并获取验证码
        captcha_image = driver.find_element(By.XPATH, "//img[@class='img-responsive']")
        captcha_image.screenshot('captcha.png')

        with open('captcha.png', 'rb') as f:
            image = f.read()
        result = ocr.classification(image)

        # 找到验证码输入框并填写验证码
        captcha_input = driver.find_element(By.ID, "edit-captcha-response")
        captcha_input.clear()
        captcha_input.send_keys(result)
        
        print(f"填写了验证码: {result}")

        # 找到提交按钮并点击
        submit_button = driver.find_element(By.ID, "edit-submit")
        submit_button.click()
        
        print("点击了提交按钮")

        # 检查是否出现错误信息，如果出现则重新识别并输入验证码
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='alert alert-block alert-dismissible alert-danger messages error']"))
            )
            print("验证码错误，重新识别并输入验证码")
            attempts += 1
        except:
            print("验证码正确，继续执行")
            break

    if attempts == max_attempts:
        print("尝试次数过多，未能成功识别验证码")

    return result