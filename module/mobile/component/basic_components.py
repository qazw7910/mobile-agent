import inspect
from typing import TYPE_CHECKING

import pytest

from module.mobile.component.basic_string import BasicString

if TYPE_CHECKING:
    pass

from module.mobile.component.base_object import BaseObject
from module.mobile.component.basic_component import BasicComponent


class BasicComponents(BaseObject):

    def __init__(self, matchers, remark):
        super().__init__()
        self.set_remark(remark)
        self.matchers = matchers

    def prerequisites(self) -> None:
        self.assert_all_visible(False)

    @property
    def texts(self) -> list[str]:
        self.ready()
        return [element.text for element in self.matchers()]

    @property
    def get_quantity(self):
        """
        取得元素數量
        """
        self.ready()
        return BasicString(
            lambda: len(self.texts),
            f'{self.remark()} > get quantity',
        )

    @property
    def quantity(self):
        """
        回傳元素素量
        """
        return len(self.texts)

    def find(self, index: int) -> BasicComponent:
        return BasicComponent(lambda: self.matchers()[index], remark=self.remark() + f", index: {index}")

    def are_all_visible(self) -> bool:
        return self.is_matchers(self.matchers)

    def assert_all_visible(self, screenshot=True) -> None:
        if not self.are_all_visible():
            self.save_screenshot('', f'{self.remark()} > assert visible') if screenshot else None
            raise Exception(f"{self.remark()} > not visible.")

    def assert_all_invisible(self, screenshot=True) -> None:
        if self.are_all_visible():
            self.save_screenshot('', f'{self.remark()} > assert invisible') if screenshot else None
            raise Exception(f"{self.remark()} > should be hidden.")

    def assume_all_visible(self) -> None:
        caller = inspect.stack()[1]
        pytest.assume(
            self.are_all_visible(),
            f"{self.remark()} > not visible."
            f"Error occurred at {caller.filename}, line {caller.lineno}"
        )

    def assume_all_invisible(self) -> None:
        caller = inspect.stack()[1]
        pytest.assume(
            not self.are_all_visible(),
            f"{self.remark()} > should be hidden."
            f"Error occurred at {caller.filename}, line {caller.lineno}"
        )

    @property
    def get_center_coordinates(self) -> list[dict[str, int]]:
        """
        返回所有匹配元素的中心座標，格式為 {'x': value, 'y': value}。
        """
        self.ready()
        elements = self.matchers()
        return [
            {
                'x': int(element.location['x'] + element.size['width'] / 2),
                'y': int(element.location['y'] + element.size['height'] / 2)
            }
            for element in elements
        ]
