from module.mobile.android import Android
from module.mobile.ios import Ios


class Navigator:

    @property
    def android(self) -> Android:
        return Android()

    @property
    def ios(self) -> Ios:
        return Ios()
