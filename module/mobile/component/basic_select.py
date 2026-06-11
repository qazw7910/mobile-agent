import pytest
import logging
from selenium.webdriver.support.select import Select

from module.mobile.component.base_object import BaseObject


class BasicWebSelect(BaseObject):

    def __init__(self, label, matcher):
        super().__init__()
        self.set_remark(label)
        self.matcher = matcher

    def select(self, text):
        logging.info(f"{self.remark()} > select")
        Select(self.matcher()).select_by_visible_text(text)

    def deselectAll(self):
        logging.info(f"{self.remark()} > deselectAll")
        Select(self.matcher()).deselect_all()

    def is_visible(self):
        return self.is_matcher(self.matcher)

    def assert_visible(self) -> None:
        if not self.is_visible():
            raise Exception(f"{self.remark()} > not visible.")

    def assert_invisible(self) -> None:
        if self.is_visible():
            raise Exception(f"{self.remark()} > should be hidden.")

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
