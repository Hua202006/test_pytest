# -*- coding: utf-8 -*-
'''
==================================================
  @Time : 2020/5/19 20:25
  @Auth : Hua_
  @File : handle_log.py
  @IDE  : PyCharm
  @Motto: 人生苦短，我学Python！
  @Email: 1403589704@qq.com
==================================================
'''
import logging, os
from scripts.handle_yaml import do_yaml
from scripts.handle_path import LOG_PATH


class HandleLog:
    def __init__(self, name=None):
        if name is None:
            self.my_logger = logging.getLogger('testcase')  # 创建日志工具
        else:
            self.my_logger = logging.getLogger(name)  # 创建日志工具

        self.my_logger.setLevel(do_yaml.get_data("log", "logger_level"))  # 设置日志等级
        console_handle = logging.StreamHandler()  # 创建日志输出渠道，日志输出到控制台
        #console_handle.setLevel('WARNING')  # 控制台的日志等级，若不写，则遵循上面的等级
        log_full_path = os.path.join(LOG_PATH, do_yaml.get_data('log', 'log_filename'))  # log保存地址
        file_handle = logging.FileHandler(log_full_path, encoding="utf-8")  # 日志输出到文件
        # 创建日志的显示样式（格式）并与渠道进行关联
        formater = logging.Formatter('%(asctime)s - [%(levelname)s] - [msg]: %(message)s - %(name)s - %(lineno)d')
        console_handle.setFormatter(formater)
        file_handle.setFormatter(formater)
        # 日志器对象与日志输出渠道（展示的地方）进行关联
        self.my_logger.addHandler(console_handle)
        self.my_logger.addHandler(file_handle)

    def get_logger(self):
        return self.my_logger

do_log = HandleLog().get_logger() #创建实例对象，后续直接调用do_log

if __name__ == '__main__':
    do_log = HandleLog()
    my_logger = do_log.get_logger()
    my_logger.debug("这是一条debug级别的日志！")
    my_logger.info("这是一条info级别的日志！")
    my_logger.warning("这是一条warning级别的日志！")
    my_logger.error("这是一条error级别的日志！")
    my_logger.critical("这是一条critical级别的日志！")
