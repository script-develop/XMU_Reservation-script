#这个模块用来初始化浏览器，进行相应的调整
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

#浏览器初始化配置选项
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--acceptInsecureCerts')
chrome_options.add_argument('--start-maximized')  # 启动时最大化窗口
# chrome_options.add_argument('--headless')

def start(username,password):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service,options=chrome_options)
    driver.get("http://ids.xmu.edu.cn/authserver/login?type=userNameLogin&service=http%3A%2F%2Fcgyy.xmu.edu.cn%2Fidcallback")


    username_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "username"))) #按id等待用户名块出现
    username_input.send_keys(username)

    password_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "passwordText")))
    password_input.send_keys(password)

    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "login_submit")))
    login_button.click()

    try:
    # 等待页面中出现指定的元素，表示登录成功
        login_success_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "blank_zone"))
        )
        print("登录成功")
        return driver
    except:
        # 如果出现错误提示元素，输出报错信息并延迟5秒退出脚本
        error_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "formErrorTip"))
        )
        if error_element:
            print("您提供的用户名或者密码有误，请检查后重试")
            time.sleep(5)
            driver.quit()
            exit()
    
        