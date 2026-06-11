# Functions to support entire framework

import json
import os
import random
import string
from datetime import datetime

import pandas as pd
import yaml

from framework import datetime_utility as dt
import logging

# string 彙整
WHITESPACE = string.whitespace
LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
LETTERS = string.ascii_letters
DIGITS = string.digits
HEXDIGITS = string.hexdigits
OCTDIGITS = string.octdigits
PUNCTUATION = string.punctuation
PRINTABLE = string.printable


def generate_tw_ids(quantity: int = 1) -> list[str]:
    """
    隨機生成多筆台灣身分證字號
    """

    # 城市代碼
    CITY_CODES = {
        'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 34, 'J': 18, 'K': 19, 'L': 20,
        'M': 21, 'N': 22, 'O': 35, 'P': 23, 'Q': 24, 'R': 25, 'S': 26, 'T': 27, 'U': 28, 'V': 29, 'W': 32, 'X': 30,
        'Y': 31, 'Z': 33}

    def generate_tw_id():

        # 隨機選擇一個城市代碼
        city_code = random.choice(list(CITY_CODES.keys()))

        # 隨機選擇性別代碼（1代表男性，2代表女性）
        gender_code = random.choice(['1', '2'])

        # 隨機生成後面的數字部分
        numbers = ''.join([str(random.randint(0, 9)) for _ in range(7)])

        # 組合成完整的身份證號碼
        id_number = city_code + gender_code + numbers

        # 計算最後一位檢查碼
        total = CITY_CODES[city_code] // 10 + (CITY_CODES[city_code] % 10) * 9
        total += int(gender_code) * 8
        for i, digit in enumerate(numbers, start=2):
            total += int(digit) * (9 - i)
        check_code = (10 - (total % 10)) % 10

        # 添加檢查碼並返回完整的身份證號碼
        return id_number + str(check_code)

    return [generate_tw_id() for _ in range(quantity)]


def generate_email(min_: int = 5, max_: int = 10, domain: str = "gmail.com", hidden_code: bool = False) -> str:
    """
    隨機生成電子郵件字串
    - hidden_code 同時產生含隱碼(***)和不含隱碼的電子郵件
    """
    length = random.randint(min_, max_)
    username = ''.join(random.choice(LOWERCASE) for _ in range(length))
    visible_mail = username + "@" + domain
    if hidden_code:
        hidden_mail = username[:-3] + '***@' + domain
        return visible_mail, hidden_mail
    else:
        return visible_mail


def generate_username(min_: int = 6, max_: int = 12) -> str:
    """
    隨機生成大小寫英數組合字串，確保至少包含一個字母和一個數字。
    """
    length = random.randint(min_, max_)

    # 確保至少有一個字母和一個數字
    letters = string.ascii_letters  # 大小寫字母
    digits = string.digits  # 數字
    username = [random.choice(letters), random.choice(digits)]

    # 填充剩餘的字符
    chars = letters + digits
    username += [random.choice(chars) for _ in range(length - 2)]

    # 打亂字符順序以增加隨機性
    random.shuffle(username)

    return ''.join(username)


def generate_letters(lower: bool = True, upper: bool = True, min_: int = 1, max_: int = 10) -> str:
    """
    生成一定位數內的隨機大小寫英文組合字串
    姓名 組織名 地址都可以使用
    """
    length = random.randint(min_, max_)
    chars = None
    if lower:
        chars += LOWERCASE
    if upper:
        chars += UPPERCASE
    if chars is None:
        raise ValueError('Both lower and upper are False. At least one of them should be True.')
    return ''.join(random.choice(chars) for _ in range(length))


def generate_adult_year():
    """
    Get Adult year (This year - 21year )
    Return - string - year
    """
    datetime_now = dt.datetime_now()
    adult_year = str(int(dt.datetime_attr(datetime_now, 'year')) - 21)
    logging.info(f'generate_adult_year: {adult_year}')
    return adult_year


def generate_tw_mobile_number(hidden_code: bool = False) -> str:
    """
    隨機生成台灣手機號碼
    注意開頭4碼僅48種組合
    """

    # 閉包，重整range規則，包含上下界並回傳為list[int]
    def range_(start: int, end: int | None = None) -> list[int]:
        end = (end + 1) if isinstance(end, int) else (start + 1)
        return list(range(start, end))

    # 09xx 當中的 xx 限制
    pool = range_(10, 19) + range_(20, 29) + range_(30, 39) \
        + range_(52, 56) + range_(58) + range_(60, 61) + range_(63) + range_(68) \
        + range_(70, 72) + range_(82) + range_(86, 89)

    first4 = '09' + str(random.choice(pool))
    last6 = str(random.randint(0, 999999)).zfill(6)
    phone_visible = first4 + last6
    if hidden_code:
        phone_hidden = phone_visible[:4] + '***' + phone_visible[7:]
        return phone_visible, phone_hidden
    else:
        return phone_visible


def generate_account_id(visible_digital: int = 16, acture_digital: int = 12) -> str:
    """
    隨機生成10到16碼銀行帳號id

    args:
    - visible_digital: 希望顯示的帳號位數，需>=實際位數並<=16
    - acture_digital: 實際位數，只有10, 11, 12, 13, 14碼的選項
    """
    if 10 <= acture_digital <= 14:
        if acture_digital <= visible_digital <= 16:
            digital_start = '1' + '0' * (acture_digital - 1)
            digital_end = '9' + '9' * (acture_digital - 1)
            return str(random.randint(int(digital_start), int(digital_end))).zfill(visible_digital)
        else:
            logging.info('參數錯誤')

    else:
        logging.info('參數錯誤')


def generate_landline_phone(zone=False):
    """
    隨機生成8碼市話號碼
    """
    last7 = str(random.randint(0, 9999999)).zfill(7)
    first = str(random.choice([2, 3, 5, 6, 7, 8]))
    zone_code = random.choice(['02', '03', '037', '04', '049', '05', '06', '07', '08', '089', '082', '0826', '0836'])
    return first + last7 if not zone else zone_code + first + last7


def generate_int(min_: int, max_: int) -> int:
    """
    生成指定範圍的整數亂數
    """
    try:
        return random.randint(min_, max_)
    except Exception:
        # 辨認所有可能的exception
        raise


def generate_round2(start: int | float, end: int | float) -> int:
    """
    生成指定範圍的數值亂數，小數位數最多到兩位
    """
    try:
        return round(random.uniform(start, end), 2)
    except Exception:
        # 辨認所有可能的exception
        raise


def half_to_full(half: str) -> str:
    """
    將半形字符轉換為全形字符
    """
    mapping = str.maketrans(
        '0123456789',
        '０１２３４５６７８９'
    )
    full = half.translate(mapping)
    return full


def write_txt_by(file, data):
    with open(file, 'w') as f:
        f.write(data)


def read_txt_by(file):
    with open(file, 'r') as f:
        data = f.read()
    return data


def read_csv_by(file, key, value, dtype=str) -> list[dict]:
    """
    讀取csv，將篩選後的資料轉成list[dict]型態
    """
    df = pd.read_csv(file, dtype=dtype)
    df_filtered = df.loc[df[key] == value]
    return df_filtered.to_dict('records')


def write_csv_by(file, condition_key, condition_value, modify_key, modify_value, dtype=str) -> None:
    """
    寫入csv，將篩選後的資料寫入同一份csv
    """
    df = pd.read_csv(file, dtype=dtype)
    df.loc[df[condition_key] == condition_value, modify_key] = modify_value
    df.to_csv(file, index=False)


def read_yaml_by(file, *keys):
    """
    讀取yaml檔案，並可以任意設定讀到哪個鍵值\\
    比如 *keys = 'ios', 'cube', 'uat'，則可以讀取到'uat'的值
    """
    with open(file, 'r', encoding="utf-8") as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
        for key in keys:
            data = data[key]
    return data


def read_json_by(file, *keys):
    """
    讀取json檔案，並可以任意設定讀到哪個鍵值\\
    :param *keys: 依照欄位階層順序，最後一個欄位即為欲讀取到的欄位值\\
        比如 *keys = 'ios', 'cube', 'uat'，則可以讀取到ios內的cube內的uat欄位值
    """
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for key in keys:
            data = data[key]
    return data


def write_json_by(file, modify_value, *keys):
    """
    修改json檔中特定欄位的值，一次只能修改一個欄位的值
    :param modify_value: 欲修改成的值
    :param *keys: 依照欄位階層順序，最後一個欄位即為欲修改到的欄位值\\
        比如 *keys = 'depo1', 'main'，則可以修改到depo1內的main內的欄位值
    """
    with open(file, 'r') as f:
        data = json.load(f)

    parent = data  # pointer
    for key in keys[:-1]:
        parent = parent[key]
    parent[keys[-1]] = modify_value

    with open(file, 'w') as f:
        json.dump(data, f, indent=4)  # 縮排4個空格


def modify_string(string, replace_string, index) -> str:
    """
    將字串內指定位置開始替換成別的字串
    :param string: 初始字串
    :param replace_str: 欲替換成的字串
    :param index: 從原本字串的第幾個字元後開始替換，\\
    比如 string='123456789', replace_str='***', index=3, 將會輸出'123***789'
    如果 replace_str 超過原本字串長度也可以，即輸出index後所有replace_string
    """
    new_string = string[:index] + replace_string + string[index + len(replace_string):]
    return new_string


def json_file_to_dict(file_path: str, key=None, value=None) -> dict:
    """
    give file path
    optional: key
    return dict object
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            if value:
                data = get_json_by_key_or_value(file.read(), key, value)
            elif key:
                data = get_json_by_key_or_value(file.read(), key)
            else:
                data = json.loads(file.read())
            return data
    except FileNotFoundError as err:
        logging.error(f"Cannot find json file: {file_path}")


def get_files(folder_path: str) -> list:
    """
    give folder path
    return files
    """
    files = []
    try:
        for (_, _, file_names) in os.walk(folder_path):
            files.extend(file_names)
        return files
    except FileNotFoundError as err:
        logging.error(f"Cannot find folder: {folder_path}")


def rand_num(start, end):
    """
    1. 隨機產生特定範圍內的整數，供輸入轉帳金額使用
    2. 避免出現使用相同轉出/入帳戶與金額，觸發當日重複交易提醒而影響腳本執行
    """

    data = random.randint(start, end)
    return data


def get_json_by_key_or_value(json_repr: bytes, key: str, value: str = None) -> list:
    """
    given key and json binary,  value is optional
    return json list
    """
    results = []

    def _decode_dict(result_dict):
        try:
            if value:
                if result_dict[key] == value:
                    results.append(result_dict)
            elif result_dict[key]:
                results.extend(result_dict[key])
        except KeyError:
            # this code would occur error until find the object with correct key
            # so that would not log any info
            pass
        return result_dict

    json.loads(json_repr, object_hook=_decode_dict)
    return results


# 應放在對應情境或測案
def count_of_weekdays(start_date: str, end_date: str, days: list[str], default_format='%Y/%m/%d'):
    """
    目前只能處理只選擇單一weekday的情況
    例：一週只能選一天，不能選多個(週一、週二都選)
    """
    dates = pd.to_datetime([start_date, end_date], format=default_format)
    result = pd.date_range(dates[0], dates[1], freq='1d').day_name().value_counts()[days]
    return result

# 應放在對應情境或測案


def find_next_weekdays(start_date: str, end_date: str, days: list[str], default_format='%Y/%m/%d'):
    """
    目前只能處理只選擇單一weekday的情況
    例：一週只能選一天，不能選多個(週一、週二都選)
    """
    dates = pd.to_datetime([start_date, end_date], format=default_format)
    find_dates = pd.date_range(dates[0], dates[1], freq='1d')
    dates_day_name = pd.date_range(dates[0], dates[1], freq='1d').day_name()
    days_len = len(days)
    i = 0

    for index, weekday in enumerate(dates_day_name):
        if i < days_len:
            if weekday == days[i]:
                result = find_dates[index].strftime("%Y/%m/%d")
                i = i + 1
    return result
