# -*- coding: utf-8 -*-
'''
==================================================
  @Time : 2020/5/20 8:20
  @Auth : Hua_
  @File : handle_mysql.py
  @IDE  : PyCharm
  @Motto: 人生苦短，我学Python！
  @Email: 1403589704@qq.com
==================================================
'''
import pymysql
from scripts.handle_yaml import do_yaml
import random


class HandleMysql:
    def __init__(self):
        self.conn = pymysql.connect(host=do_yaml.get_data('mysql', 'host'),
                                    user=do_yaml.get_data('mysql', 'user'),
                                    password=do_yaml.get_data('mysql', 'password'),
                                    database=do_yaml.get_data('mysql', 'db'),
                                    port=do_yaml.get_data('mysql', 'port'),
                                    cursorclass=pymysql.cursors.DictCursor)  # cursorclass设置为pymysql.cursors.DictCursor，后面获取数据库的值都为字典
        self.cursor = self.conn.cursor()  #创建游标

    def get_one_value(self, sql, args=None):
        '''
        获取单个值
        :param sql:
        :param args:
        :return:
        '''
        self.cursor.execute(sql, args=args)
        self.conn.commit()
        return self.cursor.fetchone()  # 获取单个值

    def get_values(self, sql, args=None):
        '''
        获取所有值
        :param sql:
        :param args:
        :return:
        '''
        self.cursor.execute(sql, args=args)
        self.conn.commit()
        return self.cursor.fetchall()  # 获取所有值

    def close(self):
        self.cursor.close()
        self.conn.close()

    @staticmethod
    def create_mobile():
        '''
        随机生成11位手机号
        :return: 返回一个手机号字符串
        '''
        mobile_head = [186, 139, 159, 188, 136]
        start_number = str(random.choice(mobile_head))  # 随机选择手机头
        end_num = ''.join(random.sample('0123456789', 8))  # 随机选择0-9中的8个数字
        return start_number + end_num

    def is_existed_mobile(self, mobile):
        '''
        判断指定的手机号是否存在于数据库中
        :param mobile:
        :return:
        '''
        sql = do_yaml.get_data('mysql', 'select_user_sql')
        if self.get_one_value(sql, args=[mobile]):  # 手机号已经存在，则返回True，否则返回False
            return True
        else:
            return False

    def create_not_existed_mobile(self):
        '''
        随机生成一个数据库不存在的手机号
        :return: 返回一个手机号字符串
        '''
        while True:
            one_mobile = self.create_mobile()  # 创建一个手机号
            if not self.is_existed_mobile(one_mobile):
                break
        return one_mobile

    def get_not_existed_user_id(self):
        # 从yaml配置文件中获取查询最大用户id的sql语句
        sql = do_yaml.get_data('mysql', 'select_max_userid_sql')
        not_existed_id = self.get_one_value(sql).get('id') + 1  # 获取数据库中id最大值并+1
        return not_existed_id

    def get_not_existed_loan_id(self):
        # 从yaml配置文件中获取查询最大用户load_id的sql语句
        sql = do_yaml.get_data('mysql', 'select_max_userid_sql')
        not_existed_load_id = self.get_one_value(sql).get('id') + 1  # 获取数据库中id最大值并+1
        return not_existed_load_id


if __name__ == '__main__':
    mobile = '13888888888'
    sql_1 = "SELECT * FROM member WHERE mobile_phone=%s"
    sql_2 = "SELECT * FROM member LIMIT 0, 10;"
    do_mysql = HandleMysql()
    do_mysql.is_existed_mobile(mobile)
    # print(do_mysql.get_not_existed_user_id())
    # res1 = do_mysql.get_one_value(sql_1, args=(mobile, ))
    # print(res1)
    # # #
    # res2 = do_mysql.get_values(sql_2)
    # print(res2)
    do_mysql.create_not_existed_mobile()
    print(do_mysql.get_not_existed_user_id())
    print(do_mysql.get_not_existed_loan_id())
    # sql_3 = "SELECT * FROM member LIMIT %s,%s;"
    # print(do_mysql.get_values(sql_3, args=(1, 5)))
    # print(do_mysql.get_values(sql_3, args=[1, 5]))
    # do_mysql.is_existed_mobile("1890000111")
