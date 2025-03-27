from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import sys
sys.stdout = open('log.txt', 'w')

def login(driver, config):
    # 启动Chrome浏览器并打开登录页面
    driver.get("http://ids.xmu.edu.cn/authserver/login?type=userNameLogin&service=http%3A%2F%2Fcgyy.xmu.edu.cn%2Fidcallback")

    username_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "username")))
    username_input.send_keys(config['username'])

    password_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "passwordText")))
    password_input.send_keys(config['password'])

    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "login_submit")))
    login_button.click()

    try:
        # 等待页面中出现指定的元素，表示登录成功
        login_success_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "blank_zone"))
        )
        print("登录成功")
    except:
        # 如果出现错误提示元素，输出报错信息并延迟5秒退出脚本
        error_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "formErrorTip"))
        )
        if error_element:
            print("您提供的用户名或者密码有误，请检查后重试")
            time.sleep(5)
            driver.quit()
            exit()