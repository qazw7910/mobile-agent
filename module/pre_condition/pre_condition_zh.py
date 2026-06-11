import time

import pytest
import logging

from module.mobile.cube_util import CubeUtil
from module.mobile.navigator import Navigator
from module.mobile.device_manager import DeviceManager


class PreConditionZh:
    def __init__(self):
        self.case_map = {}
        self.system = None
        self.navigator = None
        self.user = None
        self.version = None

    def setup_method(self, method):
        """
        初始化所有page, 跳過app啟動彈窗
        """
        try:
            if self.system == "ios":
                self.navigator = Navigator().ios.zh
            elif self.system == "android":
                self.navigator = Navigator().android.zh
            test_name = method.__name__
            if self.case_map.get(test_name, None) is None:
                logging.info(f"🕹️ skip_setup_method: {test_name}")
                return
            if self.system == "ios":
                self.user = CubeUtil.ios_json_cube_user(self.case_map.get(test_name))
            elif self.system == "android":
                self.user = CubeUtil.android_json_cube_user(self.case_map.get(test_name))
            self.version = CubeUtil.get_env().get('version', None)
        except Exception as e:
            logging.error(f"Setup Fail: {e}")
            # 僅記錄錯誤，不自動調用 teardown，避免測試流程混亂

    def teardown_method(self):
        driver = DeviceManager.STATIC_DRIVER
        if driver is not None:
            driver.quit()
            DeviceManager.STATIC_DRIVER = None
        DeviceManager.KEEP_APP_STATE = False

    @pytest.fixture(autouse=True)
    def auto_teardown(self):
        yield
        self.teardown_method()
