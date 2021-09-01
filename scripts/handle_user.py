# -*- coding: utf-8 -*-
'''
==================================================
  @Time : 2020/5/20 17:15
  @Auth : Hua_
  @File : handle_user.py
  @IDE  : PyCharm
  @Motto: 人生苦短，我学Python！
  @Email: 1403589704@qq.com
==================================================
'''
from scripts.handle_request import HandleRequest
from scripts.handle_mysql import HandleMysql
from scripts.handle_yaml import do_yaml
from scripts.handle_parameterize import GlobalData


def create_user(name, password=12345678, type=1):
    do_request = HandleRequest()
    do_mysql = HandleMysql()
    method = 'POST'
    URL = "http://api.lemonban.com/futureloan/member/register"
    phone_number = do_mysql.create_not_existed_mobile()
    param = {"mobile_phone": phone_number,
             "reg_name": name,
             'pwd': password,
             "type": type

             }
    headers = do_yaml.get_data("api", "api_version")
    do_request.add_headers(headers)  # 添加请求头
    res = do_request.send("POST", URL, json=param)
    user_id = res.json()["data"]["id"]  # 从响应报文中获取用户id
    # 关闭相关连接
    do_request.close()
    do_mysql.close()
    # 将用户信息添加至全局数据池中
    setattr(GlobalData, "${" + name + "_user_tel}", phone_number)
    setattr(GlobalData, "${" + name + "_user_pwd}", password)
    setattr(GlobalData, "${" + name + "_user_id}", user_id)


def generate_three_user():
    """
    创建三个用户，管理员、投资员、借款人
    :return:
    """
    create_user("admin", type=0)
    create_user("invest")
    create_user("borrow")
    pass


generate_three_user()
pass
