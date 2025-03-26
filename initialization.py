import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def chrome_initialization():

    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--acceptInsecureCerts')
    chrome_options.add_argument('--start-maximized')  # 启动时最大化窗口
    # chrome_options.add_argument('--headless')

    os.environ['WDM_SSL_VERIFY'] = '0'

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver