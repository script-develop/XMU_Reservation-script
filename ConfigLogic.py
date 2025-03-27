from PyQt5.QtWidgets import  QMessageBox
from PyQt5.QtCore import Qt
import os
import json
import sys
sys.stdout = open('log.txt', 'w')

class ConfigLogic():
    def __init__(self, ui):
        self.ui = ui  # 将 UI 实例传入到逻辑类中
        self.config = None  # 初始化配置为空
        self.load_config()

        # 绑定事件
        self.ui.interact(self.confirm,self.update_time_options)
     
    def update_time_options(self):  # 逻辑处理部分
        self.ui.time_combo.clear()  # 清空时间选项
        
        # 获取类型
        type_text = self.ui.type_combo.currentText()
        # 根据不同预约类型更新时间选项
        if type_text == '游泳馆':
            self.ui.time_combo.addItems(['请选择', '09:30-11:00', '12:00-14:00', '14:30-16:00', '16:30-18:00', '18:30-20:30'])
            self.hide_partner(True)
        elif type_text == '健身房':
            self.ui.time_combo.addItems(['请选择', '10:30-12:00', '12:00-13:30', '13:30-15:00', '15:00-16:30', '16:30-18:00', '18:00-19:30', '19:30-21:00'])
            self.hide_partner(True)
        elif type_text == '羽毛球':
            self.ui.time_combo.addItems(['请选择'] + [f'{hour:02d}{minute:02d}' for hour in range(9, 21) for minute in (0, 30)])
            self.hide_partner(False)
        else:
            self.ui.time_combo.addItem('请选择')
            self.hide_partner(True)
        
    def load_config(self):  # 加载配置并填充到 UI
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as config_file:
                config = json.load(config_file)
                self.ui.account_input.setText(config.get('username', ''))
                self.ui.password_input.setText(config.get('password', ''))
                self.ui.phone_input.setText(config.get('phone_number', ''))
                self.ui.type_combo.setCurrentText(config.get('reservation_type', '请选择'))
                self.ui.partner_name_input.setText(config.get('partner_name', ''))
                self.ui.partner_id_input.setText(config.get('partner_id', ''))
                self.update_time_options()
                self.ui.time_combo.setCurrentText(config.get('desired_time_slot', '请选择'))

    def confirm(self):
        account = self.ui.account_input.text()
        password = self.ui.password_input.text()
        phone = self.ui.phone_input.text()
        reservation_type = self.ui.type_combo.currentText()
        desired_time_slot = self.ui.time_combo.currentText()
        partner_name = self.ui.partner_name_input.text()
        partner_id = self.ui.partner_id_input.text()

        # 如果没有变量值就提示输入
        

        self.config = {
            'username': account,
            'password': password,
            'phone_number': phone,
            'reservation_type': reservation_type,
            'desired_time_slot': desired_time_slot,
            'partner_name': partner_name,
            'partner_id': partner_id
        }

        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_path, 'w', encoding='utf-8') as config_file:
            json.dump(self.config, config_file, indent=4)

        QMessageBox.information(self.ui, '配置确认', '配置已保存。')
        
        if not account or not password or not phone or reservation_type == '请选择' or desired_time_slot == '请选择':
            self.ui.rejected()
            return
        
        self.ui.accept()

    

    def hide_partner(self, show):
        if show:
            self.ui.partner_name_label.hide()
            self.ui.partner_name_input.hide()
            self.ui.partner_id_label.hide()
            self.ui.partner_id_input.hide()
        else:
            self.ui.partner_name_label.show()
            self.ui.partner_name_input.show()
            self.ui.partner_id_label.show()
            self.ui.partner_id_input.show()
