import inspect
import re

import pytest
import logging

from framework import datetime_utility as dt
from module.mobile.component.base_object import BaseObject


class BasicString(BaseObject):

    def __init__(self, matcher, remark):
        super().__init__()
        self.matcher = matcher
        self.set_remark(remark)

    """
    LessThan & MoreThan
    """

    def is_less_than(self, expecting) -> bool:
        return int(self.matcher()) < int(expecting)

    def is_more_than(self, expecting) -> bool:
        return int(self.matcher()) > int(expecting)

    def assert_lass_than(self, expecting) -> None:
        if not self.is_less_than(expecting):
            self.save_screenshot('', f"{self.remark()} > assert lass than")
            raise Exception(
                f"AssertLessThan: Actual= {self.matcher()} !< Expected= {expecting}"
            )

    def assert_more_than(self, expecting) -> None:
        if not self.is_more_than(expecting):
            self.save_screenshot('', f"{self.remark()} > assert more than")
            raise Exception(
                f"AssertMoreThan: Actual= {self.matcher} !> Expected= {expecting}"
            )

    def assume_less_than(self, expecting) -> None:
        pytest.assume(
            self.is_less_than(expecting),
            f"AssumeLessThan: Actual= {self.matcher()} !< Expected= {expecting}"
        )

    def assume_more_than(self, expecting) -> None:
        pytest.assume(
            self.is_more_than(expecting),
            f"AssumeMoreThan: Actual= {self.matcher()} !> Expected= {expecting}"
        )

    """
    Equls & NotEquls
    """

    def is_equals(self, expecting) -> bool:
        logging.info(f"{self.matcher()}")
        return self.matcher() == expecting

    def assert_equals(self, expecting) -> None:
        if not self.is_equals(expecting):
            self.save_screenshot('', f"{self.remark()} > assert equals")
            raise Exception(
                "AssertEqual: Actual= {}, Expected= {}".format(
                    self.matcher(),
                    expecting
                )
            )

    def assert_not_equals(self, expecting) -> None:
        if self.is_equals(expecting):
            self.save_screenshot('', f"{self.remark()} > aassert not equals")
            raise Exception(
                f"AssertNotEqual: Actual= {self.matcher()}, Expected= {expecting}"
            )

    def assume_equals(self, expecting) -> None:
        caller = inspect.stack()[1]
        pytest.assume(
            self.is_equals(expecting),
            f"AssumeEqual: Actual= {self.matcher()}, Expected= {expecting}\n"
            f"Error occurred at {caller.filename}, line {caller.lineno}"
        )

    def assume_not_equals(self, expecting) -> None:
        pytest.assume(
            not self.is_equals(expecting),
            f"AssumeNotEqual: Actual= {self.matcher()}, Expected= {expecting}"
        )

    """
    Greater or Equals
    """

    def is_greater_or_equals(self, expecting) -> bool:
        logging.info(f" {self.remark()} > isGreaterOrEquals({expecting})")
        return self.matcher() >= expecting

    def assert_greater_or_equals(self, expecting) -> None:
        if not self.is_greater_or_equals(expecting):
            self.save_screenshot('', f"{self.remark()} > assert greater or equals")
            raise Exception(
                f"AssertGreaterOrEquals: Actual= {self.matcher()} !< Expected= {expecting}"
            )

    def assume_greater_or_equals(self, expecting) -> None:
        pytest.assume(
            self.is_greater_or_equals(expecting),
            f"AssumeGreaterOrEquals: Actual= {self.matcher()} !< Expected= {expecting}"
        )

    """
    in , contain
    """

    def is_contain(self, msg):
        logging.info(f" {self.remark()} > Contain ({msg})")
        return msg in self.matcher()

    def is_not_contain(self, msg):
        logging.info(f" {self.remark()} > Not Contain ({msg})")
        return msg not in self.matcher()

    def is_in(self, msg):
        logging.info(f" {self.remark()} > In ({msg})")
        return self.matcher() in msg

    def is_not_in(self, msg):
        logging.info(f" {self.remark()} > Not In ({msg})")
        return self.matcher() not in msg

    def assert_in(self, msg) -> None:
        """
        斷言 if Object is in [msg]
        Case中斷
        """
        if not self.is_in(msg):
            self.save_screenshot('', f"{self.remark()} > assert in")
            raise Exception(
                f"{msg} <== Not In ==> {self.matcher()}"
            )

    def assume_in(self, msg) -> None:
        """
        斷言 if Object is in [msg]
        Case繼續執行
        """
        caller = inspect.stack()[1]
        pytest.assume(
            self.is_in(msg),
            f"{msg} <== Not In == > {self.matcher()}\n"
            f"Error occurred at {caller.filename}, line {caller.lineno}"
        )

    def assume_not_in(self, msg):
        """
        斷言 if Object not in [msg]
        Case繼續執行
        """
        pytest.assume(
            self.is_not_in(msg),
            f"{msg} <== In == > {self.matcher()}"
        )

    def assert_not_in(self, msg):
        """
        斷言 if Object not in [msg]
        Case中斷
        """
        if not self.is_not_in(msg):
            self.save_screenshot('', f"{self.remark()} > assert not in")
            raise Exception(
                f"{msg} <== In ==> {self.matcher()}"
            )

    def assume_contain(self, msg):
        """
        斷言 if Object contain [msg]
        Case繼續執行
        """
        caller = inspect.stack()[1]
        pytest.assume(
            self.is_contain(msg),
            f"{self.matcher()} <== Not Contain == > {msg}\n"
            f"Error occurred at {caller.filename}, line {caller.lineno}"
        )

    def assert_contain(self, msg):
        """
        斷言 if Object contain [msg]
        Case中斷
        """
        if not self.is_contain(msg):
            self.save_screenshot('', f"{self.remark()} > asassert contain")
            raise Exception(
                f"{self.matcher()} <== Not Contain ==> {msg}"
            )

    def assume_not_contain(self, msg):
        """
        斷言 if Object not contain [msg]
        Case繼續執行
        """
        caller = inspect.stack()[1]
        pytest.assume(
            self.is_not_contain(msg),
            f"{self.matcher()} <== Contain == > {msg}\n"
            f"Error occurred at {caller.filename}, line {caller.lineno}"
        )

    def assert_not_contain(self, msg):
        """
        斷言 if Object not contain [msg]
        Case中斷
        """
        if not self.is_not_contain(msg):
            self.save_screenshot('', f"{self.remark()} > assert not contain")
            raise Exception(
                f"{self.matcher()} <== Contain ==> {msg}"
            )

    """
    驗證格式
    """

    def is_match_pattern(self, pattern):
        logging.info(f" {self.remark()} > Match ({pattern})")
        return bool(re.match(pattern, self.matcher()))

    def is_time_match_now(self, buffer_minutes):
        logging.info(f" {self.remark()} > is time:{self.matcher()} match now")
        return bool(dt.is_time_match_now_within_buffer(self.matcher(), buffer_minutes))

    def assert_pattern(self, pattern):
        if not self.is_match_pattern(pattern):
            self.save_screenshot('', f"{self.remark()} > assert pattern")
            raise Exception(
                f"{self.matcher()} <== assert pattern ==> {pattern}"
            )

    def assume_pattern(self, pattern):
        caller = inspect.stack()[1]
        pytest.assume(
            self.is_match_pattern(pattern),
            f"{self.matcher()}  <== assume pattern ==> {pattern}\n"
            f"Error occurred at {caller.filename}, line {caller.lineno}"
        )

    def assume_time_match_now(self, current_time=dt.datetime_now(), buffer_minutes=3):
        # 如果因環境因素導致有時時間上的延遲，可依需求調整buffer_minutes
        caller = inspect.stack()[1]
        pytest.assume(
            self.is_time_match_now(buffer_minutes),
            f"{self.matcher()}  <== assume pattern ==> now:{current_time}, buffer_min:{buffer_minutes}\n"
            f"Error occurred at {caller.filename}, line {caller.lineno}"
        )
