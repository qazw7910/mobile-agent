from module.mobile.navigator_android_zh import NavigatorAndroidZh


class Android:

    @property
    def zh(self) -> NavigatorAndroidZh:
        return NavigatorAndroidZh()
