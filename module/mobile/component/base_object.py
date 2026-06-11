import datetime
import os
import time
from pathlib import Path
from time import sleep

import allure
import logging
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, InvalidSelectorException
from selenium.webdriver.remote.webelement import WebElement

from module.mobile.component.exception.ElementNotVisibleExceptions import ElementNotVisibleExceptions
from module.mobile.component.exception.InvalidSelectorExceptions import InvalidSelectorExceptions
from module.mobile.component.exception.NoSuchElementExceptions import NoSuchElementExceptions
from module.mobile.component.exception.NotReadyException import NotReadyException
from module.mobile.cube_util import CubeUtil
from module.mobile.device_manager import DeviceManager
from module.mobile.globalvar import GlobalVar
import cv2 as cv



class BaseObject:
    __remark = "No settings"

    def __init__(self):
        self._page = None
        self.default_interval = 1
        self.default_max_count = 3

    def ready(self, interval: float = None, max_retry_count: int = None, screenshot=True) -> 'BaseObject':
        """
        - interval: 檢查間隔
        - max_retry_count: 總共重新檢查次數 ex: max_retry_count = 2 會重新檢查2次 共檢查3次
        """
        self.retry_method(
            lambda: self.prerequisites(),
            interval,
            max_retry_count,
            screenshot
        )
        return self

    def is_ready(self, interval: float = None, max_retry_count: int = None) -> bool:
        """
        - interval: 檢查間隔
        - max_retry_count: 總共重新檢查次數 ex: max_retry_count = 2 會重新檢查2次 共檢查3次
        """
        try:
            self.ready(
                interval,
                max_retry_count,
                False
            )
            return True

        except Exception:
            return False

    def prerequisites(self) -> None:
        pass

    def set_remark(self, remark) -> None:
        self.__remark = remark

    def remark(self) -> str:
        return self.__remark

    def is_handle_matcher(self, matcher: callable) -> bool:
        try:
            matcher()
            return True

        except InvalidSelectorException as e:
            return False

        except NoSuchElementException as e:
            return False

        except ElementNotVisibleException as e:
            return False

        except Exception as e:
            logging.error(f'{e}')
            return False

    def handle_matcher(self, matcher: callable) -> WebElement | list[WebElement]:
        try:
            return matcher()

        except InvalidSelectorException as e:
            logging.info(e.msg)
            raise InvalidSelectorExceptions(self.remark())

        except NoSuchElementException as e:
            logging.info(e.msg)
            raise NoSuchElementExceptions(self.remark())

        except ElementNotVisibleException as e:
            logging.info(e.msg)
            raise ElementNotVisibleExceptions(self.remark())

        except Exception as e:
            logging.error(f'{e}')

    def is_matcher_visible(self, matcher: callable) -> bool:
        try:
            matcher().is_displayed()
            return True

        except NoSuchElementException:
            return False

        except ElementNotVisibleException:
            return False

        except Exception as e:
            logging.error(f'{e}')
            return False

    def is_matcher(self, matcher: WebElement) -> bool:
        return self.is_matcher_visible(lambda: self.handle_matcher(matcher))

    def is_matchers_all_visible(self, matcher: callable) -> bool:

        try:
            for element in matcher():
                element.is_displayed()
            if len(matcher()) == 0:
                return False
        except NoSuchElementException:
            return False

        except ElementNotVisibleException:
            return False

        except Exception as e:
            logging.error(f'{e}')
            return False
        return True

    def is_matchers(self, matcher: WebElement) -> bool:
        return self.is_matchers_all_visible(lambda: self.handle_matcher(matcher))

    def retry_method(self, matcher, interval: float = None, max_retry_count: int = None, screenshot=True) -> None:
        if interval is not None:
            self.default_interval = interval

        if max_retry_count is not None:
            self.default_max_count = max_retry_count

        retry_count = 0
        total_waiting_times = self.default_interval * self.default_max_count

        while True:
            try:
                matcher()
                return None

            except Exception:
                if retry_count == self.default_max_count:
                    self.save_screenshot('', f'{self.remark()} failed') if screenshot else None
                    raise NotReadyException(
                        f'❌ {self.remark()} failed after {retry_count}/{self.default_max_count} retries ({self.default_interval * (retry_count):.1f}s / {total_waiting_times:.1f})')
                retry_count += 1
                CubeUtil.retry_sleep(self.default_interval, retry_count, self.default_max_count)

    def save_screenshot(
            self,
            case: str,
            name: str | None = None,
            sleep: int | float = 0.5,
            attach: bool = True,
            attach_jpg: bool = True,
            remove: bool = True
    ) -> str | None:
        """
        儲存 png 截圖，並附在 allure report 當中
x
        Args:
        - case: 設定截圖存放的資料夾, 如果沒有 name 時則變為 name
        - name: 設定截圖名稱, 並存為 png
        - sleep: 截圖前等待時間, 單位為秒(s), 使用時機譬如等待動畫結束再截圖
        - to_jpg: 是否另存 jpg 圖片
        - jpg_ratio: 另存 jpg 的圖片大小比例, 介於 0~100 之間, 比如 50 代表圖片長寬都縮至一半
        - jpg_quality: 另存 jpg 的壓縮品質, 0最差, 100最好
        - attach: 是否附加截圖於 allure report
        - attach_jpg: True, allure report 的截圖為 jpg; False 為 png
        - remove: 是否在 attach allure report 之後移除所有儲存的截圖

        Return:
        - None: 如果 remove=True, 表示要移除所有截圖, 因此不回傳任何路徑
        - 截圖路徑: 當 remove=False, 表示不移除任何截圖, 回傳最後的截圖路徑,
            當 to_jpg=True 時回傳 jpg 路徑, 否則回傳 png 路徑。
        """
        time.sleep(sleep)

        ID = 'SS' + str(Screenshot.count())
        IMAGE_PATH = Screenshot.IMAGE_PATH

        if name is None:
            name_png = f'{ID}_{case}.png'
            png_path = os.path.join(IMAGE_PATH, name_png)
        else:
            case_path = os.path.join(IMAGE_PATH, case)
            os.makedirs(case_path, exist_ok=True)
            name_png = f'{ID}_{name}.png'
            png_path = os.path.join(case_path, name_png)

        DeviceManager.get_driver().save_screenshot(png_path)

        final_path = png_path
        logging.info(f'image path: {final_path}')

        if attach:
            attach_type = allure.attachment_type.JPG if attach_jpg else allure.attachment_type.PNG
            allure.attach.file(final_path, final_path, attach_type)

        if remove:
            os.remove(final_path)
            if os.path.exists(png_path):
                os.remove(png_path)
            return None

        return png_path

    # def cv_save_screenshot(self, name: str, sleep: int = 0.5, remove: bool = False):
    #     """
    #     圖形辨識存取圖片用
    #     """
    #
    #     time.sleep(sleep)
    #
    #     CV_EXPECTED_PATH = ex_config.Screenshot.CV_EXPECTED_DIR_PATH
    #     IMAGE_PATH = os.path.join(CV_EXPECTED_PATH, f'{name}.png')
    #     DeviceManager.get_driver().save_screenshot(IMAGE_PATH)
    #
    #     if remove:
    #         os.remove(IMAGE_PATH)
    #         return None
    #
    #     return IMAGE_PATH

    def take_screenshot(self, folder_path: str = None, filename: str = None) -> str:
        """
        截圖並儲存到指定資料夾

        Args:
            folder_path: 儲存截圖的資料夾路徑
            filename: 自定義檔案名稱（可選）

        Returns:
            str: 儲存的檔案完整路徑
        """
        result = None
        if GlobalVar.SCREENSHOT_RESULT:
            result = '預期結果'
        else:
            result = '實際結果'

        if folder_path == None:
            folder_path = f"cv_screenshot/{self.remark()}"

        if filename == None:
            filename = f"{self.remark()}_{result}"

        try:
            # 轉換為 Path 物件以便處理路徑
            folder = Path(folder_path)

            # 如果資料夾不存在，建立它
            folder.mkdir(parents=True, exist_ok=True)

            # 如果沒有提供檔名，使用時間戳作為檔名
            if filename is None:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
            elif not filename.endswith('.png'):
                filename += '.png'

            # 組合完整檔案路徑
            file_path = folder / filename

            # 截圖
            sleep(1)
            DeviceManager.get_driver().save_screenshot(str(file_path))

            logging.info(f"截圖已儲存至: {file_path}")
            return str(file_path)

        except Exception as e:
            logging.error(f"截圖過程發生錯誤: {str(e)}")
            return None


class Screenshot:
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    REPORTS = os.path.join(BASE, 'reports')
    IMAGE = os.path.join(REPORTS, 'image')

    BASE_PATH = BASE
    IMAGE_PATH = IMAGE

    @staticmethod
    def counter():
        count = 1

        def inner_counter():
            nonlocal count
            count += 1
            return count

        return inner_counter

    count = counter()
