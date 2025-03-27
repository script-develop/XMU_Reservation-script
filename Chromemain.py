import sys
import time
from PyQt5.QtWidgets import QApplication, QDialog
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from WebInitial import chrome_initialization
from Login import login
from EasyReservation import easy_reservation
from HardRservation import hard_reservation
from ConfigUI import ConfigUI
from ConfigLogic import ConfigLogic
from datetime import datetime, timedelta

sys.stdout = open('log.txt', 'w')

# 执行预约任务
def reservation_task(driver, config):
    print("开始执行预约任务")
    try:
        reservation_type = config.get('reservation_type')
        if reservation_type in ['游泳馆', '健身房']:
            easy_reservation(driver, config)
        elif reservation_type == '羽毛球':
            hard_reservation(driver, config)
        else:
            raise ValueError("Invalid reservation type")  # 健壮性

        success_message_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert-success'))
        )

        print("已成功预约")
    except Exception as e:
        print(f"预约失败: {e}")
    finally:
        driver.quit()

# 定时执行预约任务
def schedule_reservation(config):
    reservation_type = config.get('reservation_type')
    # 获取当前时间
    now = datetime.now()

    if reservation_type == '游泳馆':
        # 游泳馆不定时，直接执行预约
        print("游泳馆不定时，直接执行预约")
        driver = chrome_initialization(True)
        login(driver, config)
        reservation_task(driver, config)
    else:
        # 定时设置：健身房和羽毛球根据预约类型定时
        if reservation_type in ['健身房']:
            target_time = now.replace(hour=13, minute=0, second=0, microsecond=0)
        else:  # 羽毛球或其他类型
            target_time = now.replace(hour=12, minute=0, second=0, microsecond=0)

        if now > target_time:
            # 如果当前时间已经过了目标时间，就推迟到明天的同一时间
            target_time += timedelta(days=1)

        # 计算剩余时间
        sleep_time = (target_time - now).total_seconds()
        print(f"预约任务将在 {target_time} 执行，剩余 {sleep_time} 秒")

        # 等待直到定时执行
        time.sleep(sleep_time)

        # 定时执行预约任务
        driver = chrome_initialization(test=False)
        login(driver, config)
        reservation_task(driver, config)

if __name__ == '__main__':
    # 读取配置文件
    app = QApplication(sys.argv)
    ui = ConfigUI()  # 创建 UI 界面
    logic = ConfigLogic(ui)  # 逻辑控制

    # 启动 UI 事件循环，等待用户操作
    result = ui.exec_()
    if result == QDialog.rejected:
        exit(0)

    config = logic.config  # 获取保存的配置
    print("配置保存成功：")

    # 调用定时任务
    schedule_reservation(config)

    # 让主线程保持运行，避免程序退出
    while True:
        time.sleep(1)
