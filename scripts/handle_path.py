# -*- coding: utf-8 -*-
'''
==================================================
  @Time : 2020/5/19 18:52
  @Auth : Hua_
  @File : handle_path.py
  @IDE  : PyCharm
  @Motto: 人生苦短，我学Python！
  @Email: 1403589704@qq.com
==================================================
'''
import os
BASE_PATH=os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #获取项目绝对路径
CONF_PATH=os.path.join(BASE_PATH,'confs')
CONF_FILE_PATH=os.path.join(CONF_PATH,'testcases.yaml')
DATA_PATH=os.path.join(BASE_PATH,'data')
LOG_PATH=os.path.join(BASE_PATH,'logs')
CASES_PATH=os.path.join(BASE_PATH,'cases')
REPORTS_PATH=os.path.join(BASE_PATH,'reports')
pass
