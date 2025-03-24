import json
import os
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QComboBox, QVBoxLayout, QPushButton, QMessageBox

def config():
    app = QApplication(sys.argv)
    window = ConfigWindow()
    window.exec_()

    # 读取配置文件
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
    else:
        config = {}

    return config

class ConfigWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.load_config()

    def initUI(self):
        self.setWindowTitle('配置输入')
        self.setFixedWidth(300)  # 设置窗口宽度为300

        layout = QVBoxLayout()

        # 账号
        self.account_label = QLabel('账号:')
        self.account_input = QLineEdit()
        layout.addWidget(self.account_label)
        layout.addWidget(self.account_input)

        # 密码
        self.password_label = QLabel('密码:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # 电话号码
        self.phone_label = QLabel('电话号码:')
        self.phone_input = QLineEdit()
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)

        # 预约类型
        self.type_label = QLabel('预约类型:')
        self.type_combo = QComboBox()
        self.type_combo.addItems(['请选择', '游泳馆', '健身房'])
        self.type_combo.currentIndexChanged.connect(self.update_time_options)
        layout.addWidget(self.type_label)
        layout.addWidget(self.type_combo)

        # 预约时间
        self.time_label = QLabel('预约时间:')
        self.time_combo = QComboBox()
        self.update_time_options()
        layout.addWidget(self.time_label)
        layout.addWidget(self.time_combo)

        # 确认按钮
        self.confirm_button = QPushButton('确认')
        self.confirm_button.clicked.connect(self.confirm)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as config_file:
                config = json.load(config_file)
                self.account_input.setText(config.get('username', ''))
                self.password_input.setText(config.get('password', ''))
                self.phone_input.setText(config.get('phone_number', ''))
                reservation_type = config.get('reservation_type', '请选择')
                if reservation_type == 'swim':
                    self.type_combo.setCurrentText('游泳馆')
                elif reservation_type == 'gym':
                    self.type_combo.setCurrentText('健身房')
                else:
                    self.type_combo.setCurrentText('请选择')
                self.update_time_options()
                self.time_combo.setCurrentText(config.get('desired_time_slot', '请选择'))

    def update_time_options(self):
        self.time_combo.clear()
        if self.type_combo.currentText() == '游泳馆':
            self.time_combo.addItems(['请选择', '09:30-11:00', '12:00-14:00', '14:30-16:00', '16:30-18:00', '18:30-20:30'])
        elif self.type_combo.currentText() == '健身房':
            self.time_combo.addItems(['请选择', '10:30-12:00', '12:00-13:30', '13:30-15:00', '15:00-16:30', '16:30-18:00', '18:00-19:30', '19:30-21:00'])
        else:
            self.time_combo.addItem('请选择')

    def confirm(self):
        account = self.account_input.text()
        password = self.password_input.text()
        phone = self.phone_input.text()
        appointment_type = self.type_combo.currentText()
        appointment_time = self.time_combo.currentText()

        if not account or not password or not phone or appointment_type == '请选择' or appointment_time == '请选择':
            QMessageBox.warning(self, '输入错误', '请填写所有字段并选择有效的预约类型和时间。')
        else:
            if appointment_type == '游泳馆':
                reservation_type = 'swim'
            elif appointment_type == '健身房':
                reservation_type = 'gym'
            else:
                reservation_type = '请选择'

            config = {
                'username': account,
                'password': password,
                'phone_number': phone,
                'reservation_type': reservation_type,
                'desired_time_slot': appointment_time
            }
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
            with open(config_path, 'w') as config_file:
                json.dump(config, config_file, indent=4)
            QMessageBox.information(self, '配置确认', '配置已保存。')
            self.accept()