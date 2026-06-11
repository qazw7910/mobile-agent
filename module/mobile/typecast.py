import re
from datetime import datetime, date

import logging
from module.mobile.dollar import D


def amt_to_grp(amt: str) -> str:
    """
    將金額字串去掉$和空格，轉為分位字串
    """
    try:
        grp = amt.replace('$', '').replace(' ', '')
        logging.info(f'amount: "{amt}"')
        logging.info(f'amount to GROUPING: "{grp}"\n')
        return grp
    except BaseException:
        logging.error(f'❌ 發生轉換錯誤 請先確認參數設定是否有誤')


def amt_to_num(amt: str, log: bool = True) -> int | float:
    """
    將金額字串去掉$、分位符和空格，轉為數值型態(int|float)
    """
    try:
        digit = amt.replace('$', '').replace(',', '').replace(' ', '')
        num = float(digit) if '.' in digit else int(digit)
        if log:
            logging.info(f'amount: "{amt}", digit: "{digit}"')
            logging.info(f'amount to NUMERIC: {num}, type: {type(num)}\n')
        return num
    except BaseException:
        logging.error(f'❌ 發生轉換錯誤 請先確認參數設定是否有誤')


def amt_to_ams(amt: str) -> str:
    """
    將amount金額符後加上空格
    """
    try:
        if ('+' in amt) or ('-' in amt):
            return amt[:2] + ' ' + amt[2:]
        return amt[:1] + ' ' + amt[1:]
    except BaseException:
        logging.error(f'❌ 發生轉換錯誤 請先確認參數設定是否有誤')


def amt_to_dlr(amount: str, dollar: str = D.TWD, space: bool = True) -> str:
    """
    將金額字串去掉$和空格，轉為dlr+grp
    """
    try:
        grouping = amount.replace('$', '').replace(' ', '')
        space = ' ' if space else ''
        dollar_grouping = dollar + space + grouping
        logging.info(f'amount: "{amount}"')
        logging.info(f'result: "{dollar_grouping}"\n')
        return dollar_grouping
    except BaseException:
        logging.error(f'❌ 發生轉換錯誤 請先確認參數設定是否有誤')


def grp_to_amt(grp: str, ams=False, pos=False) -> str:
    """
    將分位字串最左側附加 "$" 或 "$ "，轉為金額字串
    """
    try:
        pure_grp = grp.replace('+', '').replace('-', '').replace(' ', '')
        amt_sign = '$ ' if ams else '$'
        if '-' in grp:
            return '-' + amt_sign + pure_grp
        pos_sign = '+' if pos else ''
        return pos_sign + amt_sign + pure_grp
    except BaseException:
        logging.error(f'❌ 發生轉換錯誤 請先確認參數設定是否有誤')


def grp_to_num(grp: str) -> int | float:
    """
    將分位字串去掉分位符，轉為數值型態(int|float)
    """
    try:
        digit = grp.replace(',', '').replace(' ', '')
        num = float(digit) if '.' in digit else int(digit)
        logging.info(f'grouping: "{grp}", digit: "{digit}"')
        logging.info(f'grouping to NUMERIC: {num}, type: {type(num)}\n')
        return num
    except BaseException:
        logging.error(f'❌ 發生轉換錯誤 請先確認參數設定是否有誤')


def num_to_amt(num: int | float, ams=False, fmt_2f=False, pos=False) -> str:
    """
    將數值(int|float)轉為金額字串
    """
    try:
        grp = format(num, ',.2f') if fmt_2f else format(num, ',')
        amt_sign = '$ ' if ams else '$'
        if num < 0:
            return '-' + amt_sign + grp
        pos_sign = '+' if pos else ''
        return pos_sign + amt_sign + grp
    except BaseException:
        logging.error(f'❌ 發生轉換錯誤 請先確認參數設定是否有誤')


def num_to_grp(num: int | float, fmt_2f=False, pos=False, trailing_zeros=True) -> str:
    """
    將數值(int|float)轉為分位字串
    """
    try:
        if trailing_zeros:
            grp = format(num, ',.2f') if fmt_2f else format(num, ',')

        # 例如：num = 997712.8，小數點最後位數為0時，不用補0
        else:
            f_num = round(num, 2)
            if fmt_2f:
                grp = format(f_num, ',')
                # 判斷是否為小數點最後為0的狀況 例：123.0
                s = grp.split('.')
                if s[1] == '0':
                    grp = s[0]
            else:
                grp = format(num, ',')
        if num < 0:
            return '-' + grp
        pos_sign = '+' if pos else ''
        return pos_sign + grp
    except BaseException:
        logging.error(f'❌ 發生轉換錯誤 請先確認參數設定是否有誤')


def num_to_pct(num: int | float, digit: int = 2, rb: bool = False, np: bool = False, pct_2f: bool = False):
    """
    將比值轉換為百分比
    """
    logging.info(f'num    : {num}')
    rb_left = '(' if rb else ''
    rb_right = ')' if rb else ''
    np_sign = ''
    num = round(num * 100, digit)
    if np:
        np_sign = '+' if num >= 0 else '-'
        num = abs(num)
    if pct_2f:
        num = format(num, '.2f')
        result = f'{rb_left}{np_sign}{num}%{rb_right}'
    else:
        result = f'{rb_left}{np_sign}{num}%{rb_right}'
    logging.info(f'result : {result}')
    return result


def dlr_to_amt(dlrgrp: str, dlr: str = 'TWD', ams: bool = False, pos: bool = False):
    """
    """
    grp = dlrgrp.replace(' ', '').replace(dlr, '')
    pure_grp = grp.replace('+', '').replace('-', '')
    amt_sign = '$ ' if ams else '$'
    if '-' in grp:
        return '-' + amt_sign + pure_grp
    pos_sign = '+' if pos else ''
    return pos_sign + amt_sign + pure_grp


def dlr_to_grp(dlrgrp: str, dlr: str = 'TWD'):
    """
    """
    grp = dlrgrp.replace(' ', '').replace(dlr, '')
    return grp


def dlr_to_num(dlrgrp: str, dlr: str = 'TWD'):
    """
    """
    grp = dlrgrp.replace(' ', '').replace(dlr, '')
    num = grp_to_num(grp)
    return num


def remove_zeros(value: str):
    """
    移除掉小數後所有的0
    """
    try:
        if '.' in value:
            value = value.rstrip('0').rstrip('.')
        return value
    except BaseException:
        logging.error(f'❌ 發生轉換錯誤 請先確認參數設定是否有誤')


def remove_rb(value: str):
    """
    移除所有括號和空格
    """
    try:
        return value.replace(' ', '').replace('(', '').replace(')', '')
    except BaseException:
        logging.error(f'❌ 發生轉換錯誤 請先確認參數設定是否有誤')


def string_to_percent(string: str) -> str:
    """
    cube中將有百分比外的字元過濾
    例如: '(-48.24%)' -> '-48.24%'
    """
    logging.info(f'int: {string}')
    result = re.sub("[^0-9%.-]", "", string)
    logging.info(f'string to percent result: {result}')
    return result


def string_to_float(string: str) -> float:
    """
    cube中將有float外的字元過濾
    例如: '(-48.24%)' -> '-48.24'
    """
    logging.info(f'int: {string}')
    result = float(re.sub("[^0-9.+-]", "", string))
    logging.info(f'string to float result: {result}')
    return result


def string_to_pattern(default_string: str, pattern):
    """
    用正則找出需要的字串
    """
    matches = re.search(pattern, default_string)

    if matches:
        result = matches.group(1)
        return result


def string_to_datetime(date_string: str, language=0):
    """
    將時間字串轉為datatime
    language:
    0=>中文： %Y年%m月%d日 %H:%M:%S
    1=>英文： %Y/%m/%d %H:%M:%S
    """
    logging.info(f'時間字串: {date_string}')

    if language == 0:
        date_format = "%Y年%m月%d日 %H:%M:%S"
    else:
        date_format = "%Y/%m/%d %H:%M:%S"
    result = datetime.strptime(date_string, date_format)
    return result


def string_to_date(date_string: str, format=0) -> str | date:
    """
    將含有日期(格式為Year/Month/Day)的字串只取出日期的部分，並且用format來判斷是否要轉換日期格式
    format:
    0: 2023/06/20 (return string)
    1: 2023-06-20 (return date)
    """
    # ToDo:之後和datetime_utility合併
    logging.info(f'字串: {date_string}')

    # 正規表示法模式
    pattern = r"(\d{4}/\d{2}/\d{2})"

    # 提取日期部分
    matches = re.search(pattern, date_string)

    # 檢查是否有找到匹配
    if matches:
        date_string = matches.group(1)
        if format == 0:
            result = date_string
        else:
            result = datetime.strptime(date_string, "%Y/%m/%d").date()

        return result
