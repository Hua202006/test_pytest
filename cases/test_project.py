import json
import pytest
from scripts.handle_request import HandleRequest
from scripts.handle_excel import HandleExcel
from scripts.handle_user import generate_three_user
from scripts.handle_yaml import do_yaml
from scripts.handle_log import do_log
from scripts.handle_mysql import HandleMysql
from scripts.handle_parameterize import Parameterize, GlobalData
import allure

class TestProject:
    do_excel = HandleExcel(do_yaml.get_data("excel", "filename"), "project")
    testcases_data = do_excel.read_excel()  # 嵌套用例对象的列表
    
    do_request = HandleRequest()

    do_request.add_headers(do_yaml.get_data('api', 'api_version'))

    @allure.title("{one_testcase.name}")
    @pytest.mark.parametrize("one_testcase", testcases_data)
    def test_project(self, one_testcase):
        # 创建HandleMysql对象
        self.do_mysql = HandleMysql()
        new_data = Parameterize.to_param(one_testcase.data)  # 将excel中读取的请求参数进行参数化
        new_url = do_yaml.get_data('api', 'base_url') + one_testcase.url
        check_sql = one_testcase.check_sql  # 从表格中获取sql语句
        if check_sql and one_testcase.name != '借款人加标':  # 判断语句，不存在check_sql，不执行
            check_sql = Parameterize.to_param(check_sql)  # 参数化
            mysql_data = self.do_mysql.get_one_value(sql=check_sql)
            amount_before = float(mysql_data['leave_amount'])
        res = self.do_request.send(one_testcase.method, new_url, json=new_data)  # 发起请求
        actual_value = res.json()  # 响应值转化为字典
        expect_result = json.loads(one_testcase.expected_value)
        try:
            for expect in expect_result.keys():
                assert expect_result[expect] == actual_value[expect]
            if check_sql and one_testcase.name != '借款人加标':  # 判断语句，不存在check_sql，不执行
                check_sql = Parameterize.to_param(check_sql)
                mysql_data = self.do_mysql.get_one_value(sql=check_sql)
                amount_after = float(mysql_data['leave_amount'])  # 数据库中金额数量（充值后的）
                one_dict = json.loads(new_data, encoding='utf-8')  # 将json字符串转化为字典
                currrent_recharge_amount = float(one_dict['amount'])  # 取出充值的金额
                actual_amount = amount_before + currrent_recharge_amount  # 实际金额总数=充值前+充值的金额
                assert actual_amount == amount_after


        except AssertionError as e:
            do_log.error(f"{one_testcase.name}:具体异常为{e}")
            self.do_excel.write_excel(one_testcase, res.text, '失败')
            print(f"用例：{one_testcase.name}---测试失败")
            raise e
        else:
            # 如果响应报文中含有token_info，说明当前用例为登录接口用例
            # 从响应报文中获取token，然后添加至请求头中
            if 'token_info' in res.text:
                token = actual_value["data"]["token_info"]["token"]
                headers = {"Authorization": "Bearer " + token}  # 格式参考接口文档
                self.do_request.add_headers(headers)  # 添加请求头到会话中，后续的充值操作无需再传
            check_sql_str = one_testcase.check_sql
            if one_testcase.name == '借款人加标':
                # 将check_sql json格式的字符串转化为字典
                check_sql_dict = json.loads(check_sql_str, encoding='utf-8')
                if "loan_id" in check_sql_dict:
                    # 获取查询loan id的sql语句
                    loan_id_sql = check_sql_dict.get('loan_id')
                    # 将sql语句进行参数化
                    loan_id_sql = Parameterize.to_param(loan_id_sql)
                    mysql_data = self.do_mysql.get_one_value(sql=loan_id_sql)

                    load_id = mysql_data['id']  # 获取loan_id
                    # 设置loan_id为GlobalData的类属性
                    setattr(GlobalData, '${loan_id}', load_id)
            self.do_excel.write_excel(one_testcase, res.text, '成功')
            print(f"用例：{one_testcase.name}---测试通过")

if __name__ == '__main__':
    pytest.main(["-s"])
