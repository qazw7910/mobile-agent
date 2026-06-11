import inspect

import pytest

from module.mobile.component.basic_component import BasicComponent
from module.mobile.device_manager import DeviceManager


class BasicComponentUnique(BasicComponent):

    def __init__(self, locator: tuple, remark: str):
        self.driver = DeviceManager.get_driver()
        self.locator = locator
        self.matcher = lambda: self.driver.find_element(*self.locator)
        self.set_remark(remark)
        super().__init__(self.matcher, remark)

    def prerequisites(self) -> None:
        self.assert_visible(False)

    def assume_unique_visible(self):
        caller = inspect.stack()[1]
        pytest.assume(
            self.is_visible(),
            f"{self.remark()} > not visible.\n"
            f"Error occurred at {caller.filename}, line {caller.lineno}"
        )
        elements = self.driver.find_elements(*self.locator)
        count = len(elements)
        pytest.assume(
            count == 1,
            f"{self.remark()} > should only find one element, actual get {count}\n"
            f"Error occurred at {caller.filename}, line {caller.lineno}"
        )
