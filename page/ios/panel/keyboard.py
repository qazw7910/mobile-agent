import logging
from appium.webdriver.common.appiumby import AppiumBy

from module.mobile.component.base_object import BaseObject
from module.mobile.component.basic_component import BasicComponent
from module.mobile.device_manager import DeviceManager
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver

TupleCoordinate = tuple[int, int, int, int] | tuple[float, float, float, float]
Coordinate = TupleCoordinate | dict[str, int] | dict[str, float]


class Offset:
    """
    Used in Page and Element to set the `offset` action for `swipe_by` and `flick_by`.
    You can set the preferred offset by assigning values to these variables,
    or create another Offset class based on your test scenario.
    """
    UP = (0.5, 0.75, 0.5, 0.25)
    DOWN = (0.5, 0.25, 0.5, 0.75)
    LEFT = (0.75, 0.5, 0.25, 0.5)
    RIGHT = (0.25, 0.5, 0.75, 0.5)
    UPPER_LEFT = (0.75, 0.75, 0.25, 0.25)
    UPPER_RIGHT = (0.25, 0.75, 0.75, 0.25)
    LOWER_LEFT = (0.75, 0.25, 0.25, 0.75)
    LOWER_RIGHT = (0.25, 0.25, 0.75, 0.75)


class Area:
    """
    Used in Page and Element to set the `area` action for `swipe_by` and `flick_by`.
    You can set the preferred area by assigning values to these variables,
    or create another Area class based on your test scenario.
    """
    FULL = (0.0, 0.0, 1.0, 1.0)


class Keyboard(BaseObject):

    # def __init__(self):
    #     self.set_remark("鍵盤")
    #     self.driver = DeviceManager.get_driver()
    def __init__(self, role=None):
        super().__init__()
        self.set_remark("鍵盤-多裝置測試")
        self.role = role
        self.driver = DeviceManager.get_driver(role=self.role)

    @property
    def earth(self):
        return BasicComponent(
            lambda: self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, '下一個鍵盤'),
            f"{self.remark()} > 下一個鍵盤"
        )

    @property
    def tool_bar(self):
        return BasicComponent(
            lambda: self.driver.find_element(AppiumBy.IOS_CLASS_CHAIN,
                                             '**/XCUIElementTypeToolbar[`label == "工具列" OR label =="Toolbar"`]'),
            f"{self.remark()} > 工具列"
        )

    @property
    def space(self):
        return BasicComponent(
            lambda: self.driver.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeKey[`name IN {"space", "空格"}`]'),
            f"{self.remark()} > 空格鍵"
        )

    @property
    def space_zh(self):
        return BasicComponent(
            lambda: self.driver.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeKey[`name == "空格"`]'),
            f"{self.remark()} > 空格鍵 (中文)"
        )

    @property
    def space_en(self):
        return BasicComponent(
            lambda: self.driver.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeKey[`name == "space"`]'),
            f"{self.remark()} > 空格鍵 (英文)"
        )

    @property
    def a(self):
        return BasicComponent(
            lambda: self.driver.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeKey[`name == "a"`]'),
            f"{self.remark()} > 鍵盤字母 A"
        )

    # @dynamic
    # def alphabet(self, alphabet_: str = 'a'):
    #     return BasicComponent(
    #         lambda: self.driver.find_element(AppiumBy.IOS_CLASS_CHAIN, f'**/XCUIElementTypeKey[`name == "{alphabet_}"`]'),
    #         f"{self.remark()} > 鍵盤英文字母 {alphabet_}"
    #     )

    @property
    def done(self):
        return BasicComponent(
            lambda: self.driver.find_element(AppiumBy.IOS_PREDICATE, 'name IN {"Done", "完成"}'),
            f"{self.remark()} > 完成按鍵"
        )

    @property
    def search(self):
        return BasicComponent(
            lambda: self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Search'),
            f"{self.remark()} > 搜尋按鍵"
        )

    @property
    def one(self):
        return BasicComponent(
            lambda: self.driver.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeKey[`name == "1"`]'),
            f"{self.remark()} > 數字 1"
        )

    @property
    def two(self):
        return BasicComponent(
            lambda: self.driver.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeKey[`name == "2"`]'),
            f"{self.remark()} > 數字 2"
        )

    @property
    def three(self):
        return BasicComponent(
            lambda: self.driver.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeKey[`name == "3"`]'),
            f"{self.remark()} > 數字 3"
        )

    @property
    def four(self):
        return BasicComponent(
            lambda: self.driver.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeKey[`name == "4"`]'),
            f"{self.remark()} > 數字 4"
        )

    @property
    def five(self):
        return BasicComponent(
            lambda: self.driver.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeKey[`name == "5"`]'),
            f"{self.remark()} > 數字 5"
        )

    @property
    def six(self):
        return BasicComponent(
            lambda: self.driver.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeKey[`name == "6"`]'),
            f"{self.remark()} > 數字 6"
        )

    @property
    def seven(self):
        return BasicComponent(
            lambda: self.driver.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeKey[`name == "7"`]'),
            f"{self.remark()} > 數字 7"
        )

    @property
    def eight(self):
        return BasicComponent(
            lambda: self.driver.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeKey[`name == "8"`]'),
            f"{self.remark()} > 數字 8"
        )

    @property
    def nine(self):
        return BasicComponent(
            lambda: self.driver.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeKey[`name == "9"`]'),
            f"{self.remark()} > 數字 9"
        )

    @property
    def zero(self):
        return BasicComponent(
            lambda: self.driver.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeKey[`name == "0"`]'),
            f"{self.remark()} > 數字 0"
        )

    @property
    def delete(self):
        return BasicComponent(
            lambda: self.driver.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeKey[`name IN {"刪除", "delete"}`]'),
            f"{self.remark()} > 刪除按鍵"
        )

    # @dynamic
    # def number(self, number_: str = '0'):
    #     return BasicComponent(
    #         lambda: self.driver.find_element(AppiumBy.IOS_CLASS_CHAIN, f'**/XCUIElementTypeKey[`name == "{number_}"`]'),
    #         f"{self.remark()} > 鍵盤數字 {number_}"
    #     )

    @property
    def paste_button(self):
        return BasicComponent(
            lambda: self.driver.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeMenuItem[`label == "貼上"`]'),
            f"{self.remark()} > 貼上按鈕"
        )

    @property
    def slide_bar(self):
        return BasicComponent(
            lambda: self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, '主畫面指示符號'),
            f"{self.remark()} > 滑動橫條"
        )

    @property
    def number_btn(self):
        return BasicComponent(
            lambda: self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'more'),
            f"{self.remark()} > 數字鍵盤切換鍵"
        )

    def get_window_rect(self) -> dict:
        """
        Gets the x, y coordinates of the window as well as height and width of the current window.

        Return is rearranged, for example:
        {'x': 0, 'y': 0, 'width': 500, 'height': 250}

        Note that the value type is the same as official.
        """
        rect = self.driver.get_window_rect()
        return {'x': rect['x'], 'y': rect['y'], 'width': rect['width'], 'height': rect['height']}

    def __get_coordinate(
            self,
            coordinate: Coordinate,
            name: str
    ) -> TupleCoordinate:

        # Check coordinate type.
        if not isinstance(coordinate, (dict, tuple)):
            raise TypeError(f'"{name}" should be dict or tuple.')
        if isinstance(coordinate, dict):
            coordinate = tuple(coordinate.values())

        # Check all values in coordinate should be int or float.
        if not (all(isinstance(c, int) for c in coordinate) or all(isinstance(c, float) for c in coordinate)):
            raise TypeError(f'All "{name}" values should be "int" or "float".')

        # If float, all should be (0 <= x <= 1).
        if isinstance(coordinate[0], float) and not all(0 <= abs(c) <= 1 for c in coordinate):
            raise ValueError(f'All "{name}" values are floats and should be between "0.0" and "1.0".')

        return coordinate

    def __get_offset(
            self,
            offset: Coordinate,
            area: tuple[int, int, int, int]
    ) -> tuple[int, int, int, int]:

        start_x, start_y, end_x, end_y = self.__get_coordinate(offset, 'offset')

        if isinstance(start_x, float):
            area_x, area_y, area_width, area_height = area
            start_x = area_x + int(area_width * start_x)
            start_y = area_y + int(area_height * start_y)
            end_x = area_x + int(area_width * end_x)
            end_y = area_y + int(area_height * end_y)

        offset = (start_x, start_y, end_x, end_y)
        logging._info(f'offset: {offset}')
        return offset

    def __get_area(self, area: Coordinate) -> tuple[int, int, int, int]:

        area_x, area_y, area_width, area_height = self.__get_coordinate(area, 'area')

        if isinstance(area_x, float):
            window_x, window_y, window_width, window_height = self.get_window_rect().values()
            area_x = window_x + int(window_width * area_x)
            area_y = window_y + int(window_height * area_y)
            area_width = int(window_width * area_width)
            area_height = int(window_height * area_height)

        area = (area_x, area_y, area_width, area_height)
        logging._info(f'area: {area}')
        return area

    def __get_offset(
            self,
            offset: Coordinate,
            area: tuple[int, int, int, int]
    ) -> tuple[int, int, int, int]:

        start_x, start_y, end_x, end_y = self.__get_coordinate(offset, 'offset')

        if isinstance(start_x, float):
            area_x, area_y, area_width, area_height = area
            start_x = area_x + int(area_width * start_x)
            start_y = area_y + int(area_height * start_y)
            end_x = area_x + int(area_width * end_x)
            end_y = area_y + int(area_height * end_y)

        offset = (start_x, start_y, end_x, end_y)
        logging._info(f'offset: {offset}')
        return offset

    def swipe_by(
            self,
            offset: Coordinate = Offset.UP,
            area: Coordinate = Area.FULL,
            duration: int = 1000,
            times: int = 1
    ) -> AppiumWebDriver:

        global driver
        area = self.__get_area(area)
        offset = self.__get_offset(offset, area)

        for _ in range(times):
            driver = self.driver.swipe(*offset, duration)

        return driver
