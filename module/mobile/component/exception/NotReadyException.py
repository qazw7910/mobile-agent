from module.mobile.component.exception.BasicException import BasicException


class NotReadyException(BasicException):

    def __init__(self, message):
        super().__init__(message)
