import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import pytest

# pytest.main(['-s', '--alluredir=reports/', '--clean-alluredir', '--reruns=2','--reruns-delay=3' ])  # 生成allure报告
#pytest.main(['-s', '--alluredir=reports/', '--clean-alluredir'])  # 生成allure报告
pytest.main(["-v","-s","--clean-alluredir","--alluredir=reports/"])