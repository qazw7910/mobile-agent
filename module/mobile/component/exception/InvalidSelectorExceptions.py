from module.mobile.component.exception.BasicException import BasicException


class InvalidSelectorExceptions(BasicException):
    def __init__(self, message="InvalidSelectorExceptions"):
        super().__init__(message)
