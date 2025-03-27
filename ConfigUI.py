from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QComboBox, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class ConfigUI(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()
        
    def initUI(self): #ui函数
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
        left_layout.addWidget(self.type_label)
        left_layout.addWidget(self.type_combo)

        # 预约时间
        self.time_label = QLabel('预约时间:')
        self.time_combo = QComboBox()
        left_layout.addWidget(self.time_label)
        left_layout.addWidget(self.time_combo)

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
        right_layout.addWidget(self.confirm_button)

        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        self.setLayout(layout)

        #同伴窗口先隐藏，直到预约类型是羽毛球才显示
        self.partner_name_label.hide()
        self.partner_name_input.hide()
        self.partner_id_label.hide()
        self.partner_id_input.hide()

    #这玩意应该是qt自带，如果event发生了，就触发
    def closeEvent(self, event):
        event.accept()
        self.rejected()
        QApplication.quit()  # 关闭整个 Qt 应用



    #这是ui跟logic的交互区
    def interact(self, callback1,callback2):
        self.confirm_button.clicked.connect(callback1) #logic里
        self.type_combo.currentIndexChanged.connect(callback2)

        

     


  