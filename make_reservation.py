from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import ddddocr

def make_reservation(driver, config):
    # 进入预约页面

    # 计算当前日期的后6天
    reservation_date = datetime.now() + timedelta(days=6)
    reservation_date_str = reservation_date.strftime("%m/%d")

    # 进入预约页面
    driver.get(f"https://cgyy.xmu.edu.cn/room_reservations/{reservation_date_str}")

    driver.get("https://cgyy.xmu.edu.cn/room_reservations/03/28")

    # 读取配置的预约时间
    badminton_time = config['badminton_time']

    # 获取页面源代码
    page_source = driver.page_source

    # 使用BeautifulSoup解析页面
    soup = BeautifulSoup(page_source, 'html.parser')

    # 初始化一个二维数组
    table_data = []

    # 找到id为1的div
    target_div = soup.find('div', id='2')

    if target_div:
        # 找到所有的列
        columns = target_div.find_all('div', class_='grid-column')

        # 遍历每一列
        for column in columns:
            column_data = []
            # 找到列中的所有单元格
            cells = column.find_all('li')
            for cell in cells:
                cell_class = cell.get('class', [])
                if 'room-info' in cell_class:
                    column_data.append(cell.get_text(strip=True))
                elif 'timeslot' in cell_class:
                    column_data.append(cell.get('time', ''))
                elif 'reservable' in cell_class:
                    link = cell.find('a')
                    if link:
                        column_data.append(link.get('href', ''))
                elif 'closed' in cell_class or 'booked' in cell_class:
                    column_data.append('unreservable')
                else:
                    column_data.append(cell.get_text(strip=True))
            table_data.append(column_data)

    # 查找所有badminton_time对应的reservable的href
    hrefs = []
    for column in table_data:
        for i, cell in enumerate(column):
            if badminton_time in cell:
                if i + 1 < len(column) and column[i + 1] != 'unreservable' and column[i] != badminton_time:
                    hrefs.append(column[i])

    # 计算每个href在二维数组中所在列在多少个元素后出现unreservable
    href_unreservable_counts = {}
    for href in hrefs:
        for column in table_data:
            for i, cell in enumerate(column):
                if cell == href:
                    for j in range(i + 1, len(column)):
                        if column[j] == 'unreservable':
                            href_unreservable_counts[href] = j - i
                            break
                    if href in href_unreservable_counts:
                        break
            if href in href_unreservable_counts:
                break

    # 打印表格数据
    # for row in table_data:
    #     print(row)

    # 打印表格数据
    # for row in table_data:
    #     print(row)
    #     print(row)
    #     print(row)
    #     print(row)

    print("hrefs:")
    for href in hrefs:
        print(f"{href}")

    print("href_unreservable_counts:")
    for href, count in href_unreservable_counts.items():
        print(f"{href}: {count}")


    # 优先点击count大于2的href，如果只有count等于2的href就点击最后一个href
    selected_href = None
    for href, count in href_unreservable_counts.items():
        if count > 2:
            selected_href = href
            break
    if not selected_href:
        for href, count in href_unreservable_counts.items():
            if count == 2:
                selected_href = href

    if selected_href:
        full_url = f"https://cgyy.xmu.edu.cn{selected_href}"
        print(f"点击链接: {full_url}")
        driver.get(full_url)
    else:
        print("没有找到合适的链接进行点击")

     # 等待页面加载完成
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "edit-reservation-length-und"))
    )
    
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


    # 找到图形验证码图片元素并获取验证码
    captcha_image = driver.find_element(By.XPATH, "//img[@class='img-responsive']")
    # captcha_src = captcha_image.get_attribute('src')
    captcha_image.screenshot('captcha.png')

    # 使用ddddocr识别验证码
    ocr = ddddocr.DdddOcr()
    
    
    with open('captcha.png', 'rb') as f:
        image = f.read()
    result = ocr.classification(image)

    # 找到验证码输入框并填写验证码
    captcha_input = driver.find_element(By.ID, "edit-captcha-response")
    captcha_input.send_keys(result)
    
    print(f"填写了验证码: {result}")

    # 找到提交按钮并点击
    submit_button = driver.find_element(By.ID, "edit-submit")
    submit_button.click()
    
    print("点击了提交按钮")

    return result