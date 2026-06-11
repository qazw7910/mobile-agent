import logging
import os
import time

import logging

from framework import common, path
from module.mobile.device_manager import DeviceManager
from module.mobile.globalvar import GlobalVar


class CubeUtil:

    @staticmethod
    def tap(positions, remark: str = "", duration=None):
        logging.info(remark)
        DeviceManager.get_driver().tap(
            positions=positions,
            duration=duration
        )

    @staticmethod
    def get_env():
        return common.read_json_by(
            path.Data.JSON_APP_ENV,
            GlobalVar.PLATFORM, GlobalVar.PRODUCT, GlobalVar.ENV
        )

    @staticmethod
    def android_get_device_json(key: str):
        device_json = os.path.join(path.Data.JSON_ANDROID, 'device_caps.json')
        data = common.read_json_by(device_json, key)
        return data

    @staticmethod
    def android_my_account_json(key: str):
        user_json = os.path.join(path.Data.JSON_ANDROID, 'cube/account.json')
        data = common.read_json_by(
            user_json,
            key
        )
        return data

    @staticmethod
    def android_cathay(key: str):
        user_json = os.path.join(path.Data.JSON_ANDROID, 'cube/cathay.json')
        data = common.read_json_by(
            user_json,
            key
        )
        return data

    @staticmethod
    def android_cube_bonus_json(key: str):
        user_json = os.path.join(path.Data.JSON_ANDROID, 'cube/cube_bonus.json')
        data = common.read_json_by(
            user_json,
            key
        )
        return data

    @staticmethod
    def android_login_remember_json(key: str):
        user_json = os.path.join(path.Data.JSON_ANDROID, 'cube/login_remember.json')
        data = common.read_json_by(
            user_json,
            key
        )
        return data

    @staticmethod
    def android_user_otp_json(key: str):
        user_json = os.path.join(path.Data.JSON_ANDROID, 'cube/user_otp.json')
        data = common.read_json_by(
            user_json,
            key
        )
        return data

    @staticmethod
    def android_gesture_user_csv(key: str):
        user_csv = os.path.join(path.Data.CSV_ANDROID, 'cube/account_gesture.csv')
        data = common.read_csv_by(user_csv, key='type', value=key)
        return data[0]

    @staticmethod
    def android_gesture_csv():
        return os.path.join(path.Data.CSV_ANDROID, 'cube/account_gesture.csv')

    @staticmethod
    def android_login_skip_popup_account_gesture_csv(key, username_length=10):
        user_id = common.generate_username(username_length)
        user_csv = os.path.join(path.Data.CSV_ANDROID, 'cube/account_gesture.csv')
        data = common.read_csv_by(user_csv, key='type', value=key)
        # common_android.login_skip_all_alert(data[0]['id'], data[0]['password'])
        return data[0]

    @staticmethod
    def ios_json_cube_user(key: str):
        return common.read_json_by(
            path.Data.JSON_IOS_CUBE_USER,
            key
        )

    @staticmethod
    def ios_json_cube_cathay(key: str):
        return common.read_json_by(
            path.Data.JSON_IOS_CUBE_CATHAY,
            key
        )

    @staticmethod
    def debug_print(log) -> None:
        logging.info(log)

    @staticmethod
    def debug_print_error(log) -> None:
        logging.error(log)

    @staticmethod
    def sleep(seconds, info="") -> None:
        for number in range(1, seconds + 1):
            logging.info(f"Sleep second({number})/{seconds}s, {info}")
            time.sleep(1)

    @staticmethod
    def retry_sleep(seconds: float, current_retry: int, total_retry: int, info="") -> None:
        if seconds % 1 == 0:  # 如果是整數
            for number in range(1, int(seconds) + 1):
                logging.info(f"⏳ Retry {current_retry}/{total_retry} ({number}s / {int(seconds)}s) {info}")
                time.sleep(1)
        else:
            interval = 0.1  # 設定每次的間隔為 0.1 秒
            total_attempts = int(seconds / interval)  # 計算總共的嘗試次數
            for attempt in range(total_attempts):
                current_cumulative_wait_time = (attempt + 1) * interval  # 目前累積等待時間
                logging.info(
                    f"⏳ Retry {current_retry}/{total_retry} ({current_cumulative_wait_time:.1f}s / {seconds:.1f}s) {info}")  # 格式化輸出
                time.sleep(interval)  # 每次間隔 0.1 秒

    @staticmethod
    def screenshot(path="screenshot.png") -> None:
        DeviceManager.get_driver().save_screenshot(path)

    @staticmethod
    def scroll_to_element(element):
        DeviceManager.get_driver().execute_script(
            "arguments[0].scrollIntoView();",
            element
        )

    @staticmethod
    def file_count(directory):
        files = [file for file in os.listdir(directory) if file != '.gitkeep']
        file_count = len(files)
        return file_count

    @staticmethod
    def get_cube_window():
        return DeviceManager.get_driver().get_window_size()

    @staticmethod
    def activate_app(app_id: str):
        """
        Appium API.
        Activates the application if it is not running
        or is running in the background.

        Args:
            app_id: the application id to be activated
        """
        return DeviceManager.get_driver().activate_app(app_id)

    @staticmethod
    def reload_page():
        logging.info('🕹️ Drag down to reload current page.')
        area = DeviceManager.get_driver().get_window_size()
        start_x = area['width'] / 2
        start_y = area['height'] * 0.35
        end_x = start_x
        end_y = area['height'] * 0.8
        duration = 2000
        DeviceManager.get_driver().swipe(start_x, start_y, end_x, end_y, duration)
        time.sleep(1)



