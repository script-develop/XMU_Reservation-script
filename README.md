# XMU_Reservation-script

这是一个基于selenium的预约脚本，用于快速预约体育馆的场馆

---

## 功能
- **预约时间段**: 自动查找并选择可用的健身房或游
- **保存账号密码**: 首次运行时会提示输入账号和密码，并将其保存到 `config.json` 文件中，后续运行无需再次输入。

---

## 环境配置

### **克隆仓库**  
首先，使用 `git` 克隆本仓库：  

```bash
git clone https://github.com/script-develop/XMU_Reservation-script.git
cd XMU_Reservation-script
```
### **安装依赖**  
请确保您的环境已安装 Python，并使用以下命令安装所需依赖：  

```bash
pip install -r requirements.txt
```

`requirements.txt` 包含以下库：  
- `selenium` —— 用于浏览器自动化  
- `webdriver-manager` —— 自动管理浏览器驱动  

---

## 使用方法  

### **运行脚本**
在终端（命令行）中运行以下命令：  

```bash
python chromemain.py
```

### **账号配置**
- **首次运行** 时，脚本会提示您输入账号和密码，并将其保存至 `config.json`，后续运行无需重复输入。  
- **如果需要修改账号信息**，可直接手动编辑 `config.json` 文件。  
