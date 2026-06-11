import pytest

from framework import global_adapter
from module.mobile.appium_manager import AppiumManager
from module.mobile.device_manager import DeviceManager
import logging


@pytest.fixture(scope='session', autouse=True)
def appium_server(pytestconfig):
    """
    根據 pytest 指令列參數初始化對應平台的 Appium 服務
    """
    platform = global_adapter.CommonVar.PLATFORM.lower()
    # platform = 'android'
    appium = None
    
    if platform == 'android':
        appium = AppiumManager(4723)
        appium.start()
        logging.info('🟢 Appium server for Android started on port 4723')

    elif platform == 'ios':
        appium = AppiumManager(4723)
        appium.start()
        logging.info('🟢 Appium server for iOS started on port 4723')

    else:
        pytest.exit("請使用 --platform=android 或 --platform=ios 啟動測試")
    
    yield
    
    if appium:
        appium.stop()
        logging.info('🔴 Appium server stopped')


@pytest.fixture(autouse=True)
def teardown_driver():
    """
    測試後自動關閉 Appium driver（單裝置 + 多裝置都支援）
    """
    yield

    #  關閉多裝置 drivers（role drivers）
    drivers = getattr(DeviceManager, "DRIVERS", None)
    if isinstance(drivers, dict) and drivers:
        for role, d in list(drivers.items()):
            try:
                d.quit()
            except Exception as e:
                logging.warning(f"Failed to quit driver for role {role}: {e}")
        DeviceManager.DRIVERS = {}

    #  關閉單裝置 STATIC_DRIVER
    driver = getattr(DeviceManager, "STATIC_DRIVER", None)
    if driver is not None:
        try:
            driver.quit()
        except Exception as e:
            logging.warning(f"Failed to quit STATIC_DRIVER: {e}")
        DeviceManager.STATIC_DRIVER = None

    #  清掉多裝置模式的設定（避免影響下一個 testcase）
    if hasattr(DeviceManager, "DEVICES_CONF"):
        DeviceManager.DEVICES_CONF = None
    if hasattr(DeviceManager, "DEFAULT_ROLE"):
        DeviceManager.DEFAULT_ROLE = None

    logging.info("🧹 Teardown complete")
