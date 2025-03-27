
# 项目简介

这是一个基于 **Selenium** 和 **PyQt5** 的图形化自动化脚本，旨在帮助用户实现 **健身房** 和 **羽毛球馆** 的预约。用户可以通过图形界面进行配置，并在预设的时间自动完成场馆的预约操作。

## 使用方法

### 发行版本

本项目提供了可执行文件版本，便于用户直接运行。如果是第一次运行，建议先选择 **游泳馆** 进行测试。

日志文件会保存在 `log.txt` 中，便于用户查看程序的运行情况和调试信息。

### 关闭程序

如果程序运行时窗口被隐藏且没有命令行可用，可以通过以下方式关闭程序：

    
1. **任务管理器**：
    
    - Ctrl + Shift + Esc打开任务管理器。
        
    - 找到 **python.exe** 或者**Chromemain.exe**进程
        
    - 结束进程。

    - 或者不用关也行，小脚本对内存占用较低
        

### 不使用打包文件

如果你不想使用打包版本，可以通过以下步骤进行源码运行：

1. 克隆仓库：
    
    ```bash
    git clone https://github.com/script-develop/XMU_Reservation-script.git
    ```
    
2. 安装依赖：
    
    ```bash
    pip install -r requirements.txt
    ```
    
3. 配置环境：确保你已经安装了 **Selenium** 和 **PyQt5** 等依赖包。
    
4. 运行程序：
    
    ```bash
    python Chromemain.py
    ```
    
## 贡献
本项目由@jadeproheshan和@NEO-114514共同开发

欢迎大家提出改进建议和贡献代码！如果你有任何问题或发现 bug，请在 GitHub 上提交 issue 或直接创建 Pull Request。
[这里是我们的下一步迭代计划](#下一步迭代计划），欢迎大家提交PR

---

# 技术文档概述版

## 项目概述

本项目实现了一个智能化的配置和预约管理模块，主要由以下三个核心部分组成：

- **配置模块**：用于图形界面的展示和配置管理。
    
- **驱动初始化模块**：负责浏览器驱动的初始化。
    
- **预约模块**：根据用户的需求进行预约操作。
    

## 配置模块

配置模块由两个主要文件组成：

1. **configui.py**：负责图形界面展示，基于 `PyQt5` 实现。
    
    - **功能**：
        
        - 提供用户交互界面，支持输入框、下拉菜单、按钮等组件。
            
        - 通过 `exec()` 方法返回窗口的关闭状态，并触发退出逻辑。
            
        - `interact()` 方法连接用户界面和程序逻辑，更新配置。
            
    - **代码示例**：
        
        ```python
        def interact(self, callback1, callback2):
            self.confirm_button.clicked.connect(callback1)  # 与逻辑中的 confirm 绑定
            self.type_combo.currentIndexChanged.connect(callback2)  # 与更新时间选项绑定
        ```
        
2. **configlogic.py**：负责业务逻辑操作，继承自 `PyQt5` 父类。
    
    - **功能**：
        
        - 读取和保存配置数据，配置通过 `config` 属性传递给主程序。
            
    - **交互**：
        
        - `confirm()` 方法负责处理用户输入并保存配置数据。
            

## 驱动初始化模块

该模块用于简化主函数逻辑，主要功能包括：

1. 初始化浏览器驱动，并通过 `chrome_options` 配置浏览器选项。
    
2. 使用 `webdriver-manager` 自动安装和管理浏览器驱动。
    

**代码示例**：

```python
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--acceptInsecureCerts')
chrome_options.add_argument('--start-maximized')  # 启动时最大化窗口
os.environ['WDM_SSL_VERIFY'] = '0'

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
```

## 交互模块

1. **登录模块**：模拟用户登录到指定的场馆预约平台，填写用户名和密码，点击登录按钮。
    
    - **代码示例**：
        
        ```python
        driver.get("http://ids.xmu.edu.cn/authserver/login?type=userNameLogin&service=http%3A%2F%2Fcgyy.xmu.edu.cn%2Fidcallback")
        ```
        
2. **预约模块**：分为简单预约和复杂预约两类，适配不同场馆的预约需求。
    
    - **简单预约**：通过 `Selenium` 模拟点击完成预约。
        
    - **复杂预约**：对于需要验证码的场馆，使用 `ddddocr` 库进行验证码识别，并模拟日期选择等操作。
        

**验证码识别**：通过 `ddddocr` 库进行验证码识别，设置最多 5 次识别尝试。

**代码示例**：

```python
from ddddocr import DdddOcr
ocr = DdddOcr()
result = ocr.classification(image_path)
```

## 下一步迭代计划

1. **支持不同浏览器**：目前仅支持 Chrome 浏览器，未来计划支持其他浏览器，如 Edge。
    
2. **细化预约功能**：进一步优化预约功能，支持更多场馆的预约需求。
    
3. **优化参数配置**：将内部硬编码的参数改为配置文件，增强扩展性。
    
4. **提高效率**：通过 Cookie 和本地缓存提高登录和预约效率。
    
5. **优化复杂预约算法**：提高复杂预约的成功率，尤其是在高并发情况下。
    
6. **封装验证码处理**：将验证码识别封装为独立模块，提高代码复用性。
    
7. **优化打包策略**：分析并优化打包策略，减少不必要的依赖，确保生成的文件体积小且高效。
    
8. **后台进程管理**：改善后台脚本管理，避免程序被意外终止。
    
