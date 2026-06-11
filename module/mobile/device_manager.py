import platform
import re
import subprocess
import sys

from typing import Optional, Dict, Any
import json

from appium import webdriver
from appium.options.common import AppiumOptions
import logging

# from module.ios.native_appid import IOS_CUBE
from module.mobile.globalvar import GlobalVar
from framework import global_adapter
import logging
from framework import path
import os


class DeviceManager:
    STATIC_IOS_DRIVER = None
    KEEP_APP_STATE = True
    STATIC_DRIVER = None
    LOCALHOST = 'http://127.0.0.1'
    PORT_4723 = ':4723'

    DEVICES_CONF: Optional[dict] = None  # 讀進來的 JSON
    DRIVERS: Dict[str, Any] = {}  # role -> driver
    DEFAULT_ROLE: Optional[str] = None  # e.g. "old"
    JSON_PATH = os.path.join(path.Data.JSON, 'devices2.json')

    @classmethod
    def load_devices(cls, config_path: Optional[str] = None):
        """
        載入 devices.json，啟用多裝置模式（lazy init）
        """
        config_path = config_path or cls.JSON_PATH
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                cls.DEVICES_CONF = json.load(f)
            cls.DEFAULT_ROLE = cls.DEVICES_CONF.get("defaultRole")
            cls.DRIVERS = {}
        except FileNotFoundError:
            logging.error(f"載入 找不到json檔: {config_path}")
        except Exception as e:
            logging.error(f"載入 devices.json 發生錯誤: {e}")

    @classmethod
    def adb_executor(cls, adb_commands: list) -> subprocess.CompletedProcess:
        """
        執行ADB命令並返回結果。

        參數:
        adb_commands (list): 要執行的ADB命令列表

        返回:
        subprocess.CompletedProcess: 包含命令執行結果的對象

        異常:
        subprocess.CalledProcessError: 當 ADB 命令執行失敗時拋出
        Exception: 當發生其他未預期的錯誤時拋出
        """

        try:
            return subprocess.run(
                adb_commands,
                shell=cls.is_windows(),
                check=True,
                capture_output=True,
                text=True
            )

        except subprocess.CalledProcessError as e:
            print(f"Error clearing UIAutomator2 server data: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise

    @classmethod
    def android_device_name(cls) -> bool:
        """
        獲取連接的 Android 型號
        例：pixel 7a
        """

        return cls.adb_executor(['adb', 'shell', 'getprop', 'ro.product.model']).stdout.strip()

    @classmethod
    def android_device_serial_number(cls):
        """
        獲取連接的 Android 設備的序列號（udid）

        返回:
        str: Android 設備的序列號
        """
        logging.info(cls.adb_executor(['adb', 'get-serialno']).stdout.strip())
        return cls.adb_executor(['adb', 'get-serialno']).stdout.strip()

    @classmethod
    def is_windows(cls) -> bool:
        """
        判斷當前操作系統是否為 Windows。

        返回:
        bool: 如果是 Windows 返回 True，否則返回 False
        """

        return platform.system() == 'Windows'

    @classmethod
    def is_package_exists(cls, package_name: str) -> bool:
        """
        檢查指定的包是否存在於連接的 Android 設備上。

        參數:
        package_name (str): 要檢查的 package_name

        返回:
        bool: 如果包存在返回 True，否則返回 False
        """

        device_name = cls.get_android_devices()
        result = cls.adb_executor(
            ["adb", "-s", device_name, "shell", "pm", "list", "packages", package_name]
        )

        if result.returncode == 0 and package_name in result.stdout:
            return True
        return False

    @classmethod
    def get_android_devices(cls):
        """
        獲取連接的 Android 設備列表。

        返回:
        list: 包含連接的 Android 設備 ID 的列表。如果只有一個設備，返回該設備 ID。
        如果沒有設備或發生錯誤，返回值可能為 None。
        """

        adb_command = cls.adb_executor(
            ["adb", "devices"]
        )

        try:
            if adb_command.returncode == 0:
                device_lines = adb_command.stdout.strip().splitlines()[1:]
                devices = [line.split()[0] for line in device_lines if "device" in line]
                # logging.info(f'Devices: {devices}')
                return devices[0]

            logging.info(f"命令執行失敗，錯誤訊息: {adb_command.stderr}")
        except Exception as e:
            logging.info(f"發生錯誤: {e}")

    @classmethod
    def get_uuid(cls) -> str:
        """
        獲取連接的 iOS 設備 UDID。

        返回:
        str: 包含連接的 iOS 設備 UDID 的列表。如果只有一個設備，返回該設備 UDID。
        如果沒有設備或發生錯誤，返回值可能為 None。
        """

        adb_command = cls.adb_executor(
            ["idevice_id", "-l"]
        )

        try:
            if adb_command.returncode == 0:
                udid = adb_command.stdout.strip()
                logging.info(f'iPhone UDID: {udid}')
                return udid

            logging.info(f"命令執行失敗，錯誤訊息: {adb_command.stderr}")
        except Exception as e:
            logging.info(f"發生錯誤: {e}")

    @classmethod
    def get_booted_simulator_udid(cls):
        """
        獲取當前啟動的 iOS 模擬器 UDID。

        返回:
        str: 當前啟動的 iOS 模擬器 UDID。如果沒有啟動的模擬器，返回 None。
        """

        try:
            result = cls.adb_executor(
                ["xcrun", "simctl", "list", "devices"],
            )

            booted_match = re.search(r'\(([\dA-F-]+)\) \(Booted\)', result.stdout)

            if booted_match:
                logging.info(booted_match.group(1))
                return booted_match.group(1)
            else:
                logging.info("沒有 Booted 設備")
                return None

        except Exception as e:
            logging.info(f"Error: {e}")
            return None

    @classmethod
    def is_debug_mode(cls) -> bool:
        if sys.gettrace():
            return True
        return False

    @classmethod
    def clear_uiautomator2_server(cls) -> None:
        """
        清除 UIAutomator2 服務器相關的 package_name。
        這個方法會嘗試移除預定義的 UIAutomator2 package_name。
        """
        UIAUTOMATOR2_PACKAGES = [
            "io.appium.uiautomator2.server",
            "io.appium.uiautomator2.server.test"
        ]

        for package in UIAUTOMATOR2_PACKAGES:
            try:
                adb_command = cls.adb_executor(
                    ["adb", "-s", cls.get_android_devices(), "shell", "pm", "uninstall", package]
                )
                if adb_command.returncode == 0 and cls.is_package_exists(package):
                    logging.info(f"adb -s {cls.get_android_devices()} shell pm uninstall {package}")
                    logging.info(f"Successfully uninstalled {package}")
            except subprocess.CalledProcessError as e:
                logging.warning(f"Failed to uninstall {package}: {e}")

    @classmethod
    def get_driver(cls, role: Optional[str] = None):
        # ✅ 有傳 role → 視為多裝置需求，自動載入 devices.json（若尚未載）
        if role is not None and cls.DEVICES_CONF is None:
            cls.load_devices()  # 使用 DEFAULT_DEVICES_JSON
            logging.info('✅ 載入 json 檔成功，啟用多裝置模式')

        # 多裝置模式
        if cls.DEVICES_CONF:
            if role is None:
                role = cls.DEFAULT_ROLE

            if role in cls.DRIVERS:
                return cls.DRIVERS[role]

            device = cls.DEVICES_CONF["devices"][role]
            platform = device["platform"].lower()
            server_url = cls.LOCALHOST+ ":"

            if platform == "android":
                driver = cls._create_android_from_device(device, server_url)
            elif platform == "ios":
                driver = cls._create_ios_from_device(device, server_url)
            else:
                raise ValueError(f"Unsupported platform: {platform}")

            cls.DRIVERS[role] = driver
            return driver

        # 單裝置模式（舊行為）
        return cls._get_single_driver()

    @classmethod
    def _get_single_driver(cls):
        """獲得當前平台的 Appium Driver"""
        if cls.STATIC_DRIVER is None:
            cls.STATIC_DRIVER = cls._create_driver()
        return cls.STATIC_DRIVER

    @classmethod
    def __is_ios_device(cls):
        """

        返回:
        bool: 如果是 iOS 實機返回 True，否則返回 False
        """

        if cls.get_uuid:
            return True
        return False

    @classmethod
    def __is_ios_simulator(cls):
        """
        判斷當前設備是否為 iOS 模擬器。

        返回:
        bool: 如果是 iOS 模擬器返回 True，否則返回 False
        """

        if cls.get_booted_simulator_udid():
            return True
        return False

    @classmethod
    def __is_android_deivces(cls) -> bool:
        """
        判斷當前設備是否為 Android 設備。
        """
        return bool(cls.get_android_devices())

    @classmethod
    def _create_driver(cls):
        """根據平台建立對應的 Driver"""
        # if GlobalVar.PLATFORM == 'ios':
        system_platform = global_adapter.CommonVar.PLATFORM.lower()
        if system_platform == 'ios':
            if cls.__is_ios_simulator():
                return cls.ios_simulator_driver()
            if cls.__is_ios_device():
                return cls.ios_driver()
        elif system_platform == 'android':
            if cls.__is_android_deivces():
                return cls.android_driver()

    @classmethod
    def android_driver(cls):
        """
        初始化並返回Android Appium WebDriver。

        此方法設置Appium所需的配置，並創建一個連接到 Android 設備的 WebDriver 實例。
        它還處理了一些預設置，如清理 UIAutomator2 服務器和設置日誌選項。

        返回:
        webdriver.Remote: 配置好的 Appium WebDriver 實例，用於控制 Android 設備。

        注意:
        - 此方法假定已經安裝了必要的Appium服務器和Android SDK。
        - 目標應用程序是 'com.cathaybk.nemo.uat'，主活動是 'com.cathaybk.nemo.android.MmbActivity'。
        """

        if not GlobalVar.AWS:
            cls.clear_uiautomator2_server()
        PATH = global_adapter.CommonVar.APP_PATH

        options = AppiumOptions()
        options.set_capability('platformName', 'Android')
        options.set_capability('udid', cls.android_device_serial_number())
        options.set_capability('deviceName', cls.android_device_name())
        options.set_capability('automationName', 'UiAutomator2')
        options.set_capability('autoGrantPermissions', True)
        options.set_capability('enableMultiWindows', True)
        options.set_capability('appPackage', 'com.cathaybk.geb.cubuat')
        options.set_capability('appActivity', 'com.cathaybk.geb.feature.BootActivity')
        # options.set_capability('appActivity', 'com.cathaybk.geb.cubuat.MainActivity')
        options.set_capability('appWaitActivity', "com.cathaybk.geb.feature.login.LoginActivity")
        options.set_capability('noReset', cls.KEEP_APP_STATE)
        options.set_capability('shouldTerminateApp', True)
        options.set_capability('disableIdLocatorAutocompletion', True)
        options.set_capability('waitForIdleTimeout', 100)
        # options.set_capability('app', PATH)
        # 動態 systemPort（平行 Android 必須唯一）
        # options.set_capability("systemPort",  8201)

        if cls.is_debug_mode():
            options.set_capability('newCommandTimeout', 1800)  # 1800 秒
            logging.info(f"Debug模式:newCommandTimeout設為 1800 秒")
        else:
            options.set_capability('newCommandTimeout', 100)  # 默認為 100 秒
            logging.info(f"非Debug模式:newCommandTimeout設為 100 秒")

        driver = webdriver.Remote(cls.LOCALHOST + ':4723', options=options)
        return driver

    @classmethod
    def ios_driver(cls):
        """
        設置並初始化一個 iOS Appium 驅動實例。

        該方法創建一個 AppiumOptions 對象，設置所需的 iOS 驅動參數，
        並使用這些參數來初始化 WebDriver 的遠程連接。

        返回:
            webdriver.Remote: 配置好的 Appium 驅動實例。
        """
        PATH = global_adapter.CommonVar.APP_PATH
        options = AppiumOptions()
        options.set_capability('platformName', 'iOS')
        options.set_capability('automationName', 'XCUITest')
        options.set_capability('udid', cls.get_uuid())
        # options.set_capability('bundleId', IOS_CUBE_STG)
        options.set_capability('noReset', cls.KEEP_APP_STATE)
        options.set_capability('forceAppLaunch', True)
        options.set_capability('includeSafariInWebviews', True)
        options.set_capability('newCommandTimeout', 3000)  # 设置新命令的超时时间，单位是秒
        options.set_capability('showXcodeLog', True)  # 顯示 Xcode 日誌
        options.set_capability('xcodeOrgId', 'cathaytqa')
        # options.set_capability('app', "/Users/twinb00551192/Desktop/QA_file/app-artifact.ipa")
        # options.set_capability('app', PATH)
        driver = webdriver.Remote(cls.LOCALHOST + cls.PORT_4723, options=options)
        return driver

    @classmethod
    def ios_simulator_driver(cls):
        """
        設置並初始化一個 iOS Appium 驅動實例。

        該方法創建一個 AppiumOptions 對象，設置所需的 iOS 驅動參數，
        並使用這些參數來初始化 WebDriver 的遠程連接。

        返回:
            webdriver.Remote: 配置好的 Appium 驅動實例。
        """
        PATH = global_adapter.CommonVar.APP_PATH
        options = AppiumOptions()
        options.set_capability('platformName', 'iOS')
        options.set_capability('automationName', 'XCUITest')
        # options.set_capability('deviceName', 'iPhone 16 Pro Max')
        # options.set_capability('udid', cls.get_booted_simulator_udid())
        options.set_capability('udid', '8BB9D897-A0D7-400E-AB9F-BC16C24DFBAC')
        # options.set_capability('bundleId', IOS_CUBE_STG)
        options.set_capability('bundleId', "com.cathaybk.iWA.ut")
        options.set_capability('noReset', cls.KEEP_APP_STATE)
        options.set_capability('forceAppLaunch', True)
        options.set_capability('includeSafariInWebviews', True)
        options.set_capability('newCommandTimeout', 3000)  # 设置新命令的超时时间，单位是秒
        options.set_capability('wdaLocalPort', 8102)
        # options.set_capability('mjpegServerPort', 9100)
        # options.set_capability('app',PATH)
        # options.set_capability('app','/Users/twinb00551192/Desktop/GMB/UAT_GlobalMyB2B.app')
        driver = webdriver.Remote(cls.LOCALHOST + cls.PORT_4723, options=options)
        return driver

    @classmethod
    def _create_android_from_device(cls, device: dict, server_url: str):
        """
        多裝置模式：由 JSON 建立 Android driver
        必填：udid, systemPort
        """
        if "udid" not in device or "systemPort" not in device:
            raise ValueError(f"Android device config 必須包含 udid/systemPort，收到：{device}")

        options = AppiumOptions()
        options.set_capability("platformName", "Android")
        options.set_capability("automationName", "UiAutomator2")

        # 多裝置必備
        options.set_capability("udid", device["udid"])
        options.set_capability("deviceName", device.get("deviceName", device["udid"]))
        # options.set_capability("systemPort", int(device["systemPort"]))

        # 你原本的固定設定（先不抽 helper，維持最小改動）
        options.set_capability("autoGrantPermissions", True)
        options.set_capability("enableMultiWindows", True)
        options.set_capability("appPackage", "com.cathaybk.geb.cubuat")
        options.set_capability("appActivity", "com.cathaybk.geb.feature.BootActivity")
        # options.set_capability("appWaitActivity", "com.cathaybk.geb.feature.login.LoginActivity")
        options.set_capability("noReset", cls.KEEP_APP_STATE)
        options.set_capability("shouldTerminateApp", True)
        options.set_capability("disableIdLocatorAutocompletion", True)
        options.set_capability("waitForIdleTimeout", 100)
        options.set_capability("newCommandTimeout", 1800 if cls.is_debug_mode() else 100)

        # return webdriver.Remote(server_url, options=options)
        return webdriver.Remote(server_url + device["appiumPort"], options=options)

    @classmethod
    def _create_ios_from_device(cls, device: dict, server_url: str):
        """
        多裝置模式：由 JSON 建立 iOS driver
        必填：udid, wdaLocalPort
        且需要 app 或 bundleId 其中一個
        """
        if "udid" not in device or "wdaLocalPort" not in device:
            raise ValueError(f"iOS device config 必須包含 udid/wdaLocalPort，收到：{device}")

        options = AppiumOptions()
        options.set_capability("appium:platformName", "iOS")
        options.set_capability("appium:automationName", "XCUITest")

        # 多裝置必備
        options.set_capability("appium:udid", device["udid"])
        options.set_capability("appium:wdaLocalPort", int(device["wdaLocalPort"]))

        # 可選
        # options.set_capability("deviceName", device.get("deviceName", "iPhone"))

        # app / bundleId 二選一（實機通常 app，模擬器通常 bundleId）
        if device.get("app"):
            options.set_capability("appium:app", device["app"])
        elif device.get("bundleId"):
            options.set_capability("appium:bundleId", device["bundleId"])
        else:
            raise ValueError("iOS device config 需要提供 app 或 bundleId 其中一個")

        # 固定設定（保留你原本常用的）
        options.set_capability("appium:noReset", cls.KEEP_APP_STATE)
        # options.set_capability("forceAppLaunch", True)
        # options.set_capability("includeSafariInWebviews", True)
        # options.set_capability("appium:newCommandTimeout", int(device.get("newCommandTimeout", 3000)))
        options.set_capability("appium:showXcodeLog", True)
        options.set_capability("appium:xcodeOrgId", 'FRJJ886SD8')
        # options.set_capability("appium:xcodeSigningId", 'Apple Development')
        # options.set_capability("appium:updatedWDABundleId", 'com.cathaytqa.WebDriverAgentRunner')
        options.set_capability("appium:updatedWDABundleId", 'com.facebook.WebDriverAgentRunner')
        options.set_capability("appium:useNewWDA", False)
        options.set_capability("appium:usePrebuiltWDA", True)

        options.set_capability("wdaLaunchTimeout", 120000)
        options.set_capability("wdaConnectionTimeout", 240000)
        # options.set_capability("wdaStartupRetries", 5)
        # options.set_capability("wdaStartupRetryInterval", 20000)

        # # 確保穩定
        # udid = device["udid"]
        # derived = os.path.expanduser(f"~/Library/Developer/Xcode/DerivedData/AppiumWDA-{udid}")
        # options.set_capability("derivedDataPath", derived)

        if "mjpegServerPort" in device:
            options.set_capability("appium:mjpegServerPort", int(device["mjpegServerPort"]))

        # return webdriver.Remote(server_url + device["appiumPort"], options=options)
        return webdriver.Remote(server_url + device["appiumPort"], options=options)


if __name__ == '__main__':
    # print(DeviceManager.get_booted_simulator_udid())
    print(DeviceManager.load_devices())
