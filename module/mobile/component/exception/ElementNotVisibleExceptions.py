from module.mobile.component.exception.BasicException import BasicException


class ElementNotVisibleExceptions(BasicException):
    def __init__(self, message="ElementNotVisibleExceptions"):
        super().__init__(message)
