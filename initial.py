#这个模块用来初始化导入账号密码电话号码
import os
import json

user = "config.json"

def getinfo():
    #如果已经创建，那么直接读取
    if os.path.exists(user):
        with open(user,"r",encoding="utf-8") as file:
            config = json.load(file)
            username = config.get("username")
            password = config.get("password")
            phonenumber = config.get("phonenumber")
            desired_time_slot = config.get("desired_time_slot")
            if username and password and phonenumber:
                return username,password,phonenumber,desired_time_slot
    
    #否则获取输入        
    username = input("请输入账号: ")
    password = input("请输入密码: ")
    phonenumber = input("请输入电话号码")
    desired_time_slot = input("请输入理想时间段")


    with open(user, "w", encoding="utf-8") as file:
        json.dump({"username": username, "password": password,"phonenumber":phonenumber,"desired_time_slot":desired_time_slot}, file, indent=4)

    return username, password,phonenumber,desired_time_slot