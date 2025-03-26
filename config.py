import json
import os
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QComboBox, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

def config():
    app = QApplication(sys.argv)
    window = ConfigWindow()
    window.exec_()

    # 读取配置文件
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)
    else:
        config = {}

    return config

class ConfigWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.config = None  # 初始化 config 属性
        self.initUI()
        self.load_config()

    def initUI(self):
        self.setWindowTitle('配置输入')
        self.setFixedWidth(600)  # 设置窗口宽度为600

        # 将窗口设置为总是位于最前面
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)


        layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # 账号
        self.account_label = QLabel('账号:')
        self.account_input = QLineEdit()
        left_layout.addWidget(self.account_label)
        left_layout.addWidget(self.account_input)

        # 密码
        self.password_label = QLabel('密码:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        left_layout.addWidget(self.password_label)
        left_layout.addWidget(self.password_input)

        # 电话号码
        self.phone_label = QLabel('电话号码:')
        self.phone_input = QLineEdit()
        left_layout.addWidget(self.phone_label)
        left_layout.addWidget(self.phone_input)

        # 预约类型
        self.type_label = QLabel('预约类型:')
        self.type_combo = QComboBox()
        self.type_combo.addItems(['请选择', '游泳馆', '健身房', '羽毛球'])
        self.type_combo.currentIndexChanged.connect(self.update_time_options)
        right_layout.addWidget(self.type_label)
        right_layout.addWidget(self.type_combo)

        # 预约时间
        self.time_label = QLabel('预约时间:')
        self.time_combo = QComboBox()
        right_layout.addWidget(self.time_label)
        right_layout.addWidget(self.time_combo)

        # 同伴名称
        self.partner_name_label = QLabel('同伴名称:')
        self.partner_name_input = QLineEdit()
        right_layout.addWidget(self.partner_name_label)
        right_layout.addWidget(self.partner_name_input)

        # 同伴ID
        self.partner_id_label = QLabel('同伴ID:')
        self.partner_id_input = QLineEdit()
        right_layout.addWidget(self.partner_id_label)
        right_layout.addWidget(self.partner_id_input)

        # 确认按钮
        self.confirm_button = QPushButton('确认')
        self.confirm_button.clicked.connect(self.confirm)
        right_layout.addWidget(self.confirm_button)

        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        self.setLayout(layout)

        self.partner_name_label.hide()
        self.partner_name_input.hide()
        self.partner_id_label.hide()
        self.partner_id_input.hide()

        self.update_time_options()  # 确保在初始化时调用

    def load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as config_file:
                config = json.load(config_file)
                self.account_input.setText(config.get('username', ''))
                self.password_input.setText(config.get('password', ''))
                self.phone_input.setText(config.get('phone_number', ''))
                reservation_type = config.get('reservation_type', '请选择')
                if reservation_type == 'swim':
                    self.type_combo.setCurrentText('游泳馆')
                elif reservation_type == 'gym':
                    self.type_combo.setCurrentText('健身房')
                elif reservation_type == 'badminton':
                    self.type_combo.setCurrentText('羽毛球')
                    self.partner_name_label.show()
                    self.partner_name_input.show()
                    self.partner_id_label.show()
                    self.partner_id_input.show()
                    self.partner_name_input.setText(config.get('partner_name', ''))
                    self.partner_id_input.setText(config.get('partner_id', ''))
                else:
                    self.type_combo.setCurrentText('请选择')
                self.update_time_options()
                self.time_combo.setCurrentText(config.get('desired_time_slot', '请选择'))

    def update_time_options(self):
        self.time_combo.clear()
        if self.type_combo.currentText() == '游泳馆':
            self.time_combo.addItems(['请选择', '09:30-11:00', '12:00-14:00', '14:30-16:00', '16:30-18:00', '18:30-20:30'])
            self.partner_name_label.hide()
            self.partner_name_input.hide()
            self.partner_id_label.hide()
            self.partner_id_input.hide()
        elif self.type_combo.currentText() == '健身房':
            self.time_combo.addItems(['请选择', '10:30-12:00', '12:00-13:30', '13:30-15:00', '15:00-16:30', '16:30-18:00', '18:00-19:30', '19:30-21:00'])
            self.partner_name_label.hide()
            self.partner_name_input.hide()
            self.partner_id_label.hide()
            self.partner_id_input.hide()
        elif self.type_combo.currentText() == '羽毛球':
            self.time_combo.addItems(['请选择'] + [f'{hour:02d}{minute:02d}' for hour in range(9, 21) for minute in (0, 30)])
            self.partner_name_label.show()
            self.partner_name_input.show()
            self.partner_id_label.show()
            self.partner_id_input.show()
        else:
            self.time_combo.addItem('请选择')
            self.partner_name_label.hide()
            self.partner_name_input.hide()
            self.partner_id_label.hide()
            self.partner_id_input.hide()

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
            elif appointment_type == '羽毛球':
                reservation_type = 'badminton'
                partner_name = self.partner_name_input.text()
                partner_id = self.partner_id_input.text()
                if not partner_name or not partner_id:
                    QMessageBox.warning(self, '输入错误', '请填写同伴名称和ID。')
                    return
            else:
                reservation_type = '请选择'

            self.config = {
                'username': account,
                'password': password,
                'phone_number': phone,
                'reservation_type': reservation_type,
                'desired_time_slot': appointment_time
            }

            if reservation_type == 'badminton':
                self.config['partner_name'] = partner_name
                self.config['partner_id'] = partner_id

            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
            with open(config_path, 'w', encoding='utf-8') as config_file:
                json.dump(self.config, config_file, indent=4)
            QMessageBox.information(self, '配置确认', '配置已保存。')
            self.accept()

    def exec_(self):
        super().exec_()
        return self.config