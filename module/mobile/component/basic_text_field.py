import pytest
import logging

from module.mobile.component.base_object import BaseObject
from module.mobile.component.basic_string import BasicString


class BasicWebTextField(BaseObject):

    def __init__(self, label, matcher):
        super().__init__()
        self.set_remark(label)
        self.matcher = matcher

    def prerequisites(self):
        self.assert_visible(False)

    def clear(self):
        logging.info(f"{self.remark()} > clear")
        self.ready()
        self.matcher().clear()

    def input(self, text):
        logging.info(f"{self.remark()} > input({text}) ")
        self.ready()
        self.matcher().send_keys(text)

    def getValue(self):
        logging.info(f"{self.remark()} > getValue('{self.matcher().get_attribute('value')}')")
        self.ready()
        return self.matcher().get_attribute("value")

    def get_text(self):
        return BasicString(
            f"{self.remark()} > string('{self.matcher().get_attribute('value')}')",
            lambda: self.matcher().get_attribute("value")
        )

    def click(self):
        logging.info(f"{self.remark()} > tap")
        self.ready()
        self.matcher().click()

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
