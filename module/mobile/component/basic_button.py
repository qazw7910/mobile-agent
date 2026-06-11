import inspect

import pytest
import logging
from module.mobile.component.base_object import BaseObject
from module.mobile.component.basic_string import BasicString


class BasicButton(BaseObject):

    def __init__(self, matcher, remark):
        super().__init__()
        self.set_remark(remark)
        self.matcher = matcher

    def prerequisites(self) -> None:
        self.assert_visible(False)

    def click(self) -> None:
        self.ready()
        logging.info(f"{self.remark()} > 點擊")
        self.matcher().click()

    @property
    def text(self):
        self.ready()
        return self.matcher().text

    @property
    def get_text(self):
        self.ready()
        return BasicString(
            lambda: self.matcher().text,
            f'{self.remark()} > get string'

        )

    def get_attr(self, attr):
        self.ready()
        return BasicString(
            lambda: self.matcher().get_attribute(attr),
            f"{self.remark()} > string ('{self.matcher().get_attribute(attr)}')"
        )

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

    def assume_visible(self) -> None:
        pytest.assume(
            self.is_visible(),
            f"{self.remark()} > not visible."
        )

    def assume_invisible(self) -> None:
        pytest.assume(
            not self.is_visible(),
            f"{self.remark()} > should be hidden."
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
        )
