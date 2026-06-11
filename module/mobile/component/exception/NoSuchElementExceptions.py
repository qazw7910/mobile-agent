from module.mobile.component.exception.BasicException import BasicException


class NoSuchElementExceptions(BasicException):
    def __init__(self, message="NoSuchElementExceptions"):
        super().__init__(message)
