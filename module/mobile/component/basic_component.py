import inspect
from typing import TYPE_CHECKING

import pytest
import logging
from selenium.webdriver.support.select import Select

from module.mobile.component.basic_string import BasicString

if TYPE_CHECKING:
    pass

from module.mobile.component.base_object import BaseObject
from module.mobile.cube_util import CubeUtil


class BasicComponent(BaseObject):

    def __init__(self, matcher, remark):
        super().__init__()
        self.set_remark(remark)
        self.matcher = matcher

    def prerequisites(self) -> None:
        self.assert_visible(False)

    def send_keys(self, text) -> None:
        logging.info(f"{self.remark()} > 輸入({text}) ")
        self.ready()
        self.matcher().send_keys(text)

    def click(self) -> None:
        self.ready()
        logging.info(f"{self.remark()} > 點擊")
        self.matcher().click()

    @property
    def get_coordinates_and_size(self) -> dict[str, int]:
        self.ready()

        logging.info(f"{self.remark()} > 回傳 x, y 座標和長寬")
        return {
            'x': self.matcher().location['x'],
            'y': self.matcher().location['y'],
            'width': self.matcher().size['width'],
            'height': self.matcher().size['height']
        }

    @property
    def get_center_coordinates(self) -> dict[str, int]:
        self.ready()

        x = self.matcher().location['x'] + self.matcher().size['width'] * 0.5
        y = self.matcher().location['y'] + self.matcher().size['height'] * 0.5
        logging.info(f"{self.remark()} > 回傳中心點位置")
        return {
            'x': int(x),
            'y': int(y)
        }

    def tap_center(self) -> None:
        self.ready()
        logging.info(f"{self.remark()} > 點擊中心點")
        x = self.get_center_coordinates['x']
        y = self.get_center_coordinates['y']
        CubeUtil.tap([(x, y)], f"{self.remark()} > 點擊中心點")

    def clear(self):
        logging.info(f"{self.remark()} > clear")
        self.ready()
        self.matcher().clear()

    def input(self, text):
        logging.info(f"{self.remark()} > input({text}) ")
        self.ready()
        self.matcher().send_keys(text)

    @property
    def text(self) -> str:
        self.ready()
        return self.matcher().text

    @property
    def get_text(self):
        self.ready()
        logging.info(f'{self.remark()} > get string below: ')
        return BasicString(
            lambda: self.matcher().text,
            f'{self.remark()} > get string',
        )

    @property
    def value(self) -> str:
        logging.info(f"{self.remark()} > getValue ('{self.matcher().get_attribute('value')}')")
        self.ready()
        return self.matcher().get_attribute("value")

    @property
    def get_value(self):
        self.ready()
        logging.info(f'{self.remark()} > get value below: ')
        return BasicString(
            lambda: self.matcher().get_attribute("value"),
            f"{self.remark()} > string ('{self.matcher().get_attribute('value')}')"
        )

    def attribute(self, attr) -> str:
        self.ready()
        return self.matcher().get_attribute(attr)

    def get_attribute(self, attr):
        self.ready()
        return BasicString(
            lambda: self.matcher().get_attribute(attr),
            f"{self.remark()} > string ('{self.matcher().get_attribute(attr)}')"
        )

    def select(self, text):
        logging.info(f"{self.remark()} > select")
        Select(self.matcher()).select_by_visible_text(text)

    def deselectAll(self):
        logging.info(f"{self.remark()} > deselectAll")
        Select(self.matcher()).deselect_all()

    def is_visible(self) -> bool:
        return self.is_matcher(self.matcher)

    def assert_visible(self, screenshot=True) -> None:
        if not self.is_visible():
            self.save_screenshot('', f'{self.remark()} > assert visible') if screenshot else None
            raise Exception(f"{self.remark()} > not visible.")

    def assert_invisible(self, screenshot=True) -> None:
        if self.is_visible():
            self.save_screenshot('', f'{self.remark()} > assert invisible') if screenshot else None
            raise Exception(f"{self.remark()} > should be hidden.")

    def assume_visible(self) -> None:
        caller = inspect.stack()[1]
        pytest.assume(
            self.is_visible(),
            f"{self.remark()} > not visible.\n"
            f"Error occurred at {caller.filename}, line {caller.lineno}"
        )

    def assume_invisible(self) -> None:
        caller = inspect.stack()[1]
        pytest.assume(
            not self.is_visible(),
            f"{self.remark()} > should be hidden.\n"
            f"Error occurred at {caller.filename}, line {caller.lineno}"
        )

    def assume_clickable(self) -> None:
        caller = inspect.stack()[1]
        pytest.assume(
            self.is_visible() and self.is_clickable(),
            f"{self.remark()} > clickable.\n"
            f"Error occurred at {caller.filename}, line {caller.lineno}"
        )

    def assume_not_clickable(self) -> None:
        caller = inspect.stack()[1]
        pytest.assume(
            not self.is_visible() or not self.is_clickable(),
            f"{self.remark()} > Element should not be clickable or visible.\n"
            f"Error occurred at {caller.filename}, line {caller.lineno}"
        )

    def assert_width(self) -> None:
        """
        驗證網頁上方進度條是否讀取完成
        (待確認如何取得視窗寬度)
        """
        if self.matcher().size['width'] < 0.97 * CubeUtil.get_cube_window()['width']:
            logging.info('The progress bar at the top of webview has not finished loading.')
            raise Exception(f"{self.remark()} > The progress bar at the top of webview has not finished loading. ")

    def is_selected(self) -> bool:
        return self.matcher().is_selected()

    def assert_selected(self, screenshot=True) -> None:
        if self.is_visible():
            if not self.is_selected():
                self.save_screenshot('', f'{self.remark()} > assert selected') if screenshot else None
                raise Exception(f"{self.remark()} > not selected.")
        else:
            raise Exception(f"{self.remark()} > not visible.")

    def assert_not_selected(self, screenshot=True) -> None:
        if self.is_visible():
            if self.is_selected():
                self.save_screenshot('', f'{self.remark()} > assert not selected') if screenshot else None
                raise Exception(f"{self.remark()} > selected.")
        else:
            raise Exception(f"{self.remark()} > not visible.")

    def is_clickable(self) -> bool:
        return self.matcher().is_enabled()

    def assert_clickable(self, screenshot=True) -> None:
        if self.is_visible():
            if not self.is_clickable():
                self.save_screenshot('', f'{self.remark()} > assert clickable') if screenshot else None
                raise Exception(f"{self.remark()} > not clickable.")
        else:
            raise Exception(f"{self.remark()} > not visible.")

    def assert_not_clickable(self, screenshot=True) -> None:
        if self.is_visible():
            if self.is_clickable():
                self.save_screenshot('', f'{self.remark()} > assert not clickable') if screenshot else None
                raise Exception(f"{self.remark()} > clickable.")
        else:
            raise Exception(f"{self.remark()} > not visible.")

    def assume_toast_visible(self):
        """
        用既有assume_visible，即使toast有出現也會報錯
        """
        caller = inspect.stack()[1]
        pytest.assume(
            self.is_handle_matcher(self.matcher),
            f"{self.remark()} > not visible.\n"
            f"Error occurred at {caller.filename}, line {caller.lineno}"
        )
