import os
import sys

import pytest

from scripts.handle_log import do_log
from scripts.handle_mysql import HandleMysql
from scripts.handle_parameterize import GlobalData
from scripts.handle_request import HandleRequest
from scripts.handle_user import generate_three_user
from scripts.handle_yaml import do_yaml

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))


# @pytest.fixture(scope="session")  # scope 默认为function，每个函数运行一次，class 每个类运行一次浏览器，session 每个会话运行一次 ，可根据需求修改参数。
# def browser():
#     """启动浏览器和关闭浏览器"""
#     driver = webdriver.Chrome()
#     driver.implicitly_wait(config.IMPLICTLY_WAIT_TIMEOUT)
#     driver.maximize_window()
#     yield driver
#     driver.quit()

@pytest.fixture(scope='session', autouse=True)  # autouse=True 自动调用此方法
def start():
    do_log.info("开始执行用例")
    generate_three_user()
    do_request = HandleRequest()

    do_request.add_headers(do_yaml.get_data('api', 'api_version'))
    do_mysql = HandleMysql()
    # 在每条用例执行之前，获取未注册的手机号码，然后更新全局数据池
    setattr(GlobalData, "${not_existed_tel}", do_mysql.create_not_existed_mobile())
    setattr(GlobalData, "${not_existed_tel_01}", do_mysql.create_not_existed_mobile())
    # 创建一个不存在的用户id，并加入到全局数据池中
    setattr(GlobalData, "${not_existed_id}", do_mysql.get_not_existed_user_id())
    # 创建一个不存在的loan id，并加入到全局数据池中
    setattr(GlobalData, "${not_existed_loan_id}", do_mysql.get_not_existed_loan_id())

    yield do_request, do_mysql  # 后置

    do_request.close()
    do_mysql.close()
    do_log.info("用例执行结束")
