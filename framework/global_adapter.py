class CommonVar:
    START_TIME = ""
    PAGE_URL = ""
    PAGE_ELEMENTS = ""
    PAGE_ATTRIBUTES = ""
    SCREENSHOT_FILENAME = {
        "android": "",
        "pc": "",
        "ios": ""
    }
    PROCESS_ID = {
        "appium": "",
        "ios": "",
        "android_screenshot": "",
        "pc_screenshot": ""
    }
    START_IMG = []
    RETRY_START_IMG = []
    FUNC_NAME = []
    RETRY_FUNC_NAME = []
    PAGE_ATTRIBUTES_LIST = []
    MEMORY_STACK = []
    XML_STACK = []
    FUNC_STACK = []
    FAILED_CASE_INFO = {}
    JSON_RAW_DATA_FROM_FILE = ""
    DYNAMIC_CASE_DATA = {}
    BROWSER_COOKIE = {
        "TW": {},
    }
    FUNC_DETAIL_ARGS = {}
    STATIC_TEST_DATA = {}
    CUSTOMIZED_WATTING_PERIOD = 15
    ROOT_DIR = ""
    PRIORITY = ""
    PRODUCT = ""
    ENV = ""
    ALLURE = ""
    PAGE_PACKAGE = "com.cathaybk.nemo.uat"
    PLATFORM = ""
    APP_PATH = ""
    UDID = ""
    DEVICE_NAME = ""              # 單裝置/當前 worker 指派的裝置顯示名稱（可覆蓋）
    SIM_COUNT = 0                  # 需求的模擬器總數（由 --sim-count 設定）
    SIM_DEVICE_TYPE = ""          # 建立模擬器使用的 device type 名稱（由 --sim-device-type 設定）
    SIM_UDIDS: list[str] = []      # 本次測試可用的模擬器 UDID 列表（建立或外部指定後保存）
    CAP_OVERRIDES: dict = {}       # 允許在某些測試/fixture 動態覆蓋 capabilities (e.g. {'language':'zh-TW'})


class DateTime:
    DATETIME = ""
    YEAR = ""
    MONTH = ""
    DAY = ""
    HOUR = ""
    MINUTE = ""
    SECOND = ""


class User:
    ID = ""
    EMAIL = ""
    Phone = ""
    USER_NAME = ""
    FIRST_NAME = ""
    LAST_NAME = ""
    FULL_NAME = ""
    ORG = ""
    COMMUTE_ADDRESS = ""
    NTW_FROM_ACCOUNT = ''


class Data:
    SKIP_PRE_POPUP = 0
    DATA_JSON_DIR = ''
    DATA_JSON_APP_ENV = ''
    DATA_JSON_IOS_DIR = ''
    DATA_JSON_IOS_APP = ''
    DATA_JSON_IOS_CAP = ''
    JSON_IOS_CUBE_USER = ''
    JSON_IOS_CUBE_UT_USER = ''
    JSON_IOS_CUBE_CATHAY = ''
    DATA_JSON_ANDROID_CAPS = ''
    DATA_YAML_DIR = ''
    DATA_YAML_APP_ENV = ''
    DATA_YAML_IOS_DIR = ''
    DATA_CSV_DIR = ''
    DATA_CSV_IOS_DIR = ''
    DATA_CSV_ANDROID_DIR = ''
    DATA_JSON_ANDROID_DIR = ''
    OTP_REQUEST = 0
    CANCEL_GESTURE = False


class Log:
    LOG_FILE_NAME = ''
    DATE_DIR = ''
    LOG_DIR = ''
    BASE_DIR = ''
    REPORT_DIR = ''
    REPORT_TIME_DIR = ''
    SCREENSHOT_DIR = ''
    SCREENSHOT_COUNT = 0


class AllureMark:
    FEATURE_IOS_CUBE_REG = 'IOS CUBE REG'
    STORY_P1 = 'P1'


class AllureTitle:
    INDEX = 0


class DBVar:
    DB_RESULT = ""
    DB_TABLE_TITLE = []
    SQL_CMD = ""
    DB_CONFIG = ""
    TEST_REPORT = {}


class TrackerVar:
    CUR_UNIX_TIME = ""


class AWS:
    DeviceFarm = False
