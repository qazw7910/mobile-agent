# 因應 xdist，如不能確保目前為單一執行緒，則共用變數必須 *完全靜態* 避免發生不可預期的執行緒衝突。
# 比如此份檔案當中的路徑變數為完全靜態：
# 1. 變數必須一開始就有初始值(物件)，且不會產生新的物件(例如datetime這類會隨時間變動產生新的時間物件)。
# 2. 執行期間不得再更改變數值。

import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(BASE, 'log')
REPORTS = os.path.join(BASE, 'reports')
DATA = os.path.join(BASE, 'data')


class Base:
    ALLURE_PATH_TXT = os.path.join(BASE, 'allure_path.txt')
    TIMESTAMP_TXT = os.path.join(BASE, 'timestamp.txt')


class Log:
    LOG = os.path.join(LOG, 'log.log')


class Reports:
    IMAGE = os.path.join(REPORTS, 'image')
    ALLURE_TMP = os.path.join(REPORTS, 'allure_tmp')
    ALLURE_INDEX = os.path.join(REPORTS, 'allure_index')


class Data:
    JSON = os.path.join(DATA, 'json')
    JSON_APP_ENV = os.path.join(JSON, 'app_env.json')

    JSON_IOS = os.path.join(JSON, 'ios')
    JSON_IOS_APP = os.path.join(JSON_IOS, 'app.json')
    JSON_IOS_CAP = os.path.join(JSON_IOS, 'cap.json')
    JSON_IOS_CUBE = os.path.join(JSON_IOS, 'cube')
    JSON_IOS_CUBE_UT = os.path.join(JSON_IOS_CUBE, 'ut')
    JSON_IOS_CUBE_USER = os.path.join(JSON_IOS_CUBE, 'user.json')
    JSON_IOS_CUBE_UT_USER = os.path.join(JSON_IOS_CUBE_UT, 'user.json')
    JSON_IOS_CUBE_CATHAY = os.path.join(JSON_IOS_CUBE, 'cathay.json')

    JSON_ANDROID = os.path.join(JSON, 'android')
    JSON_ANDROID_CAPS = os.path.join(JSON_ANDROID, 'device_caps.json')

    CSV = os.path.join(DATA, 'csv')
    CSV_IOS = os.path.join(CSV, 'ios')
    CSV_ANDROID = os.path.join(CSV, 'android')

    MONGODB = os.path.join(DATA, 'mongodb')
    MONGODB_CONFIG = os.path.join(MONGODB, 'db_config.json')
