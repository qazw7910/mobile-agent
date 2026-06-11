import time

import pytest

import logging
from module.mobile.cube_util import CubeUtil
from module.mobile.navigator import Navigator
from module.mobile.device_manager import DeviceManager


class PreConditionIosZh:
    case_map = {}

    def setup_method(self, method):
        """
        初始化所有page, 跳過app啟動彈窗
        """
        try:
            self.navigator = Navigator().ios.zh
            # self.navigator.cube.prelogin_process()
            test_name = method.__name__
            if self.case_map.get(test_name, None) is None:
                logging.info("🕹️ skip_setup_method")
                return
            self.user = CubeUtil.ios_json_cube_user(self.case_map.get(test_name))
            self.version = CubeUtil.get_env()['version']
            # self.navigator.cube.login(self.user)
        except Exception as e:
            logging.error(f"Setup Fail: {e}")
            self.teardown_method()

    def teardown_method(self):
        driver = DeviceManager.STATIC_DRIVER
        if driver is not None:
            driver.quit()
            DeviceManager.STATIC_DRIVER = None
        DeviceManager.KEEP_APP_STATE = False

    @pytest.fixture(autouse=True)
    def auto_teardown(self):
        self.teardown_method()
