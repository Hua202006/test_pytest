# -*- coding: utf-8 -*-
'''
==================================================
  @Time : 2020/5/20 17:21
  @Auth : Hua_
  @File : handle_parameterize.py
  @IDE  : PyCharm
  @Motto: 人生苦短，我学Python！
  @Email: 1403589704@qq.com
==================================================
'''
# 导入re模块
import re


# 创建全局数据池类
# 存储全局数据（三个账号、未注册手机号等）
class GlobalData:
    pass


class Parameterize:
    @staticmethod
    def to_param(src):
        result = re.findall(r"\${.*?}", src)  # 把src字符串中的${}查询出来，返回一个列表
        for item in result:
            data = getattr(GlobalData, item)  # 从全局数据池中读取参数
            src = src.replace(item, str(data))  # 替换指定的数据，然后将原始字符串src覆盖
        return src


if __name__ == '__main__':
    two_str = '{"mobile_phone": "${invest_user_tel}", "pwd": "12345678", "reg_name": "KeYou"}'
    setattr(GlobalData, "${not_existed_tel}", "18911112222")
    setattr(GlobalData, "${user_id}", "3333")
    setattr(GlobalData, "${invest_user_tel}", "18911114444")
    print(Parameterize.to_param(two_str))
