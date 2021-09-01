# -*- coding: utf-8 -*-
'''
==================================================
  @Time : 2020/5/19 20:25
  @Auth : Hua_
  @File : handle_yaml.py
  @IDE  : PyCharm
  @Motto: 人生苦短，我学Python！
  @Email: 1403589704@qq.com
==================================================
'''
import yaml,os
from scripts.handle_path import CONF_FILE_PATH,CONF_PATH


class HandleYaml:
    def __init__(self, filename=None):
        if filename is None:
            filename = CONF_FILE_PATH
        else:
            filename = os.path.join(CONF_PATH, filename)  # 将配置文件名与路径进行拼接
        with open(filename, encoding='utf-8') as file:
            self.config_data = yaml.full_load(file)  # 加载yaml文件
    def get_data(self,section,option):
        '''
        读取配置文件数据
        :param section:
        :param option:
        :return:
        '''
        return self.config_data[section][option]

do_yaml=HandleYaml() #创建实例对象，后续其他模块直接导入调用do_yaml

if __name__ == '__main__':
    print(do_yaml.get_data('report','filename'))
