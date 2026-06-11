import logging
from datetime import datetime, date, time, timedelta
import re

YEAR = '%Y'
MONTH = '%m'
MONTH_SGL = '%-m'
DAY = '%d'
DAY_SGL = '%-d'
HOUR = '%H'
HOUR_SGL = '%-H'
MINUTE = '%M'
MINUTE_SGL = '%-M'
SECOND = '%S'
SECOND_SGL = '%-S'

DATETIME_ISO = '%Y-%m-%d %H:%M:%S'
DATETIME_COM = '%Y/%m/%d %H:%M:%S'
DATETIME_SGL = '%Y/%-m/%-d %-H:%-M:%-S'
DATETIME_UDS = '%Y%m%d_%H%M%S'
DATETIME_RMK = '%y%m%d%H%M%S'
DATETIME_ISO_MMDD_HHMM = '%m-%d %H:%M'
DATETIME_COM_MMDD_HHMM = '%m/%d %H:%M'
DATETIME_COM_MMDD = '%m/%d'
DATETIME_COM_YYYYMMDD_HHMM = '%Y/%m/%d %H:%M'
DATETIME_COM_YYYYMMDD_HHMM_STR = '(19[0-9]{2}|20[0-9]{2})/(0?[1-9]|1[0-2])/(0?[1-9]|[12][0-9]|3[01])\\s([01]?[0-9]|2[0-3]):([0-5][0-9])'

DATE_ISO = '%Y-%m-%d'
DATE_COM = '%Y/%m/%d'
DATE_COM_STR = '(19[0-9]{2}|20[0-9]{2})/(0?[1-9]|1[0-2])/(0?[1-9]|[12][0-9]|3[01])'
DATE_SGL = '%Y/%-m/%-d'
DATE_YMZH = '%Y 年 %-m 月'
DATE_YMZH_FILL = '%Y 年 %m 月'
DATE_YMZH_NO_SPACE = '%Y年%-m月'
DATE_YMZH_FILL_NO_SPACE = '%Y年%m月'
DATE_YMDZH_NO_SPACE = '%Y年%-m月%-d日'
DATE_YMDZH_FILL_NO_SPACE = '%Y年%m月%d日'
DATE_MDZH = '%-m 月 %-d 日'
DATE_MDZH_NO_SPACE = '%-m月%-d日'
DATE_MMDD = '%m/%d'
DATE_ENG = '%b %d, %Y'

TIME_ISO = '%H:%M:%S'
TIME_SGL = '%-H:%-M:%-S'
TIME_RMK = '%H%M%S'
TIME_HHMM = '%H:%M'

TIME_12HOUR = '(0[1-9]|1[0-2]):[0-5][0-9] (AM|PM)'

TEST_START_TIME = datetime.now().strftime(DATETIME_UDS)


def datetime_now() -> datetime:
    """
    取得datetime型別的現在時間，省略ms
    """
    return datetime.now().replace(microsecond=0)


def datetime_attr(
        datetime: datetime,
        attr: str, ) -> datetime | date | time | int:
    """
    取得datetime的時間屬性
    """
    if attr == 'date':
        return datetime.date()
    elif attr == 'time':
        return datetime.time()
    elif attr == 'year':
        return datetime.year
    elif attr == 'month':
        return datetime.month
    elif attr == 'day':
        return datetime.day
    elif attr == 'hour':
        return datetime.hour
    elif attr == 'minute':
        return datetime.minute
    elif attr == 'second':
        return datetime.second
    else:
        return datetime


def datetime_to_str(
        datetime_attr: datetime | date | time | int,
        fmt_datetime=DATETIME_ISO,
        fmt_date=DATE_ISO,
        fmt_time=TIME_ISO,
        zfill=True) -> str:
    """
    依照datetime型別轉為對應的日期時間字串型別
    """
    if isinstance(datetime_attr, datetime):
        return datetime_attr.strftime(fmt_datetime)
    elif isinstance(datetime_attr, date):
        return datetime_attr.strftime(fmt_date)
    elif isinstance(datetime_attr, time):
        return datetime_attr.strftime(fmt_time)
    elif isinstance(datetime_attr, int):
        str_datetime_attr = str(datetime_attr)
        if len(str_datetime_attr) != 4 and zfill:
            return str(datetime_attr).zfill(2)
        else:
            return str_datetime_attr
    else:
        return ""


def str_to_datetime(
        str_datetime: str,
        attr: str = 'datetime',
        fmt_datetime=DATETIME_COM,
        fmt_date=DATE_COM,
        fmt_time=TIME_ISO) -> datetime | date | time | int:
    """
    將日期時間字串轉回對應的datetime型別
    """
    if attr == 'datetime':
        return datetime.strptime(str_datetime, fmt_datetime)
    elif attr == 'date':
        return datetime.strptime(str_datetime, fmt_date).date()
    elif attr == 'time':
        return datetime.strptime(str_datetime, fmt_time).time()
    elif attr in ['year', 'month', 'day', 'hour', 'minute', 'second']:
        return int(str_datetime)
    else:
        return 0


def remove_str_but_datetime(str_datetime: str, attr: str = 'datetime') -> str:
    """
    去除文本中除了時間以外的文字
    - attr
      - attr = 'datetime' 匹配ex: 2024/01/30 16:45:22
      - attr = 'date' 匹配ex: 2024/01/30
      - attr = 'date_eng' 匹配ex: Jen 30, 2024
      - attr = 'time' 匹配ex: 16:45:22
    """
    if attr == 'datetime':
        try:
            return re.findall(r'\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}', str_datetime)[0]
        except IndexError:
            logging.info('沒有找到匹配格式的時間')
    elif attr == 'date':
        try:
            return re.findall(r'\d{4}/\d{2}/\d{2}', str_datetime)[0]
        except IndexError:
            logging.info('沒有找到匹配格式的時間')
    elif attr == 'date_eng':
        try:
            return re.findall(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2}, \d{4}', str_datetime)[0]
        except IndexError:
            print('沒有找到匹配格式的時間')
    elif attr == 'time':
        try:
            return re.findall(r'\d{2}:\d{2}:\d{2}', str_datetime)[0]
        except IndexError:
            logging.info('沒有找到匹配格式的時間')
    else:
        return 0


def count_of_weekdays(target_weekday: int, start_date: date, end_date: date) -> int:
    """
    取得一段時間內星期幾的總日數
    :param target_weekday: 整數 0~6 代表 一~日
    :param start_date: 開始時間
    :param start_date: 結束時間
    """

    # 記錄起始日期的星期值，注意內部邏輯為 0~6 代表 一到日
    start_weekday = start_date.weekday()

    # 調整起始日期至下一個目標星期
    offset_weekday = target_weekday - start_weekday
    offset_days = offset_weekday if offset_weekday >= 0 else 7 + offset_weekday
    offset_start_date = start_date + timedelta(days=offset_days)

    # 計算期間內有多少個目標星期
    offset_total_days = (end_date - offset_start_date).days
    result = 1 + offset_total_days // 7

    logging.info(f'start_weekday: {start_weekday}')
    logging.info(f'target_weekday: {target_weekday}')
    logging.info(f'offset_days: {offset_days}')
    logging.info(f'offset_start_date: {offset_start_date}')
    logging.info(f'count_of_weekdays: {result}')

    return result


def next_weekday_date(start_date: date, next_weekday: int) -> date:
    """
    取得某個日期的下一個星期幾是哪一天
    """

    start_weekday = start_date.weekday()
    offset_weekday = next_weekday - start_weekday
    offset_days = offset_weekday if offset_weekday >= 0 else 7 + offset_weekday
    result = start_date + timedelta(days=offset_days)

    logging.info(f'start_weekday: {start_weekday}')
    logging.info(f'next_weekday: {next_weekday}')
    logging.info(f'offset_days: {offset_days}')
    logging.info(f'offset_start_date: {result}')

    return result


def is_time_within_buffer(time_str, buffer_minutes=1):
    """
    驗證輸入的時間字串是否在當前時間的允許緩衝範圍內。

    :param time_str: 時間字串，格式為 "HH:MM AM/PM"
    :param buffer_minutes: 緩衝時間（以分鐘為單位）
    :return: True 如果時間在範圍內，False 否則
    """

    # 將時間字串轉換為 datetime 對象
    input_time = datetime.strptime(time_str, "%I:%M %p")

    # 獲取當前時間
    now = datetime.now()

    # 將當前時間與輸入的時間轉換為相同的日期，以便比較
    input_time = now.replace(hour=input_time.hour, minute=input_time.minute, second=0, microsecond=0)

    # 計算允許的時間範圍
    start_range = now - timedelta(minutes=buffer_minutes)
    end_range = now + timedelta(minutes=buffer_minutes)

    # 判斷輸入的時間是否在範圍內
    return start_range <= input_time <= end_range


def extract_time_from_string(input_string):
    """
    從字串中提取符合 12 小時制格式的時間。

    :param input_string: 包含時間的字串
    :return: 提取出的時間字串，如果不存在則返回 None
    """
    match = re.search(TIME_12HOUR, input_string)
    return match.group(0) if match else None


def is_valid_date_format(date_str, expect="%Y/%m/%d"):
    try:
        # 直接驗證日期格式和有效性
        datetime.strptime(date_str, expect)
        return True
    except ValueError:
        return False

def is_valid_posting_date(date_str, year):
    """
    檢查是否為有效的 "入帳起息日 MM/DD" 格式和有效日期
    """
    # 檢查格式是否符合正則表達式
    pattern = r"^入帳起息日 (\d{1,2})/(\d{1,2})$"
    match = re.match(pattern, date_str)

    if not match:
        return False

    year = int(year)
    month = int(match.group(1))
    day = int(match.group(2))

    # 驗證日期的有效性
    try:
        # 嘗試將日期格式化為 datetime，會自動檢查有效性
        datetime(year=year, month=month, day=day)  # 設定任意年份來檢查
        return True
    except ValueError:
        return False

def is_time_match_now_within_buffer(input_string, buffer_minutes=1):
    """
    驗證字串中的時間是否在當前時間的允許緩衝範圍內。

    :param input_string: 包含時間的字串，例如 "05:34 PM 送出"
    :param buffer_minutes: 緩衝時間（以分鐘為單位）
    :return: True 如果時間在範圍內，False 否則
    """
    # 從字串中提取時間
    time_str = extract_time_from_string(input_string)
    if not time_str:
        return False

    # 解析時間字串
    input_time = datetime.strptime(time_str, "%I:%M %p")

    # 獲取當前時間
    now = datetime.now()

    # 將當前時間與輸入的時間轉換為相同的日期，以便比較
    input_time = now.replace(hour=input_time.hour, minute=input_time.minute, second=0, microsecond=0)

    # 計算允許的時間範圍
    start_range = now - timedelta(minutes=buffer_minutes)
    end_range = now + timedelta(minutes=buffer_minutes)

    # 判斷輸入的時間是否在範圍內
    return start_range <= input_time <= end_range
