import re

import logging


class ID:
    ACCOUNT16 = r'^(\d{16})$'
    ACCOUNT12 = r'^(\d{12})$'
    ACCOUNT11 = r'^(\d{11})$'


class PHONE:
    NUM10 = r'^(\d{10})$'


class AMT:
    O_INT = r'^(\$\d{1,3}(,\d{3})*)$'
    O_FLT = r'^(\$\d{1,3}(,\d{3})*\.\d+)$'
    O_FLT2 = r'^(\$\d{1,3}(,\d{3})*\.\d{2})$'
    O_INT_FLT2 = r'^(\$\d{1,3}(,\d{3})*(\.\d{2})?)$'

    FIND_O_INT = r'(\$\d{1,3}(?:,\d{3})*)'

    OP_INT = r'^(\+?\$\d{1,3}(,\d{3})*)$'
    OP_FLT = r'^(\+?\$\d{1,3}(,\d{3})*\.\d+)$'
    OP_FLT2 = r'^(\+?\$\d{1,3}(,\d{3})*\.\d{2})$'

    ON_INT = r'^(\-?\$\d{1,3}(,\d{3})*)$'
    R_ON_INT = r'^(\$\-?\d{1,3}(,\d{3})*)$'
    ON_FLT = r'^(\-?\$\d{1,3}(,\d{3})*\.\d+)$'
    ON_FLT2 = r'^(\-?\$\d{1,3}(,\d{3})*\.\d{2})$'

    PN_INT = r'^([+-]\$\d{1,3}(,\d{3})*)$'
    PN_FLT = r'^([+-]\$\d{1,3}(,\d{3})*\.\d+)$'
    PN_FLT2 = r'^([+-]\$\d{1,3}(,\d{3})*\.\d{2})$'

    OPN_INT = r'^([+-]?\$\d{1,3}(,\d{3})*)$'
    R_OPN_INT = r'^(\$\[+-]?\d{1,3}(,\d{3})*)$'
    OPN_FLT = r'^([+-]?\$\d{1,3}(,\d{3})*\.\d+)$'
    OPN_FLT2 = r'^([+-]?\$\d{1,3}(,\d{3})*\.\d{2})$'


class AMS:
    O_INT = r'^(\$\s\d{1,3}(,\d{3})*)$'

    TWD_O_INT = r'^(TWD\s\d{1,3}(,\d{3})*)$'
    USD_O_INT = r'^(USD\s\d{1,3}(,\d{3})*)$'


class GRP:
    O_INT = r'^(\d{1,3}(,\d{3})*)$'
    O_FLT = r'^(\d{1,3}(,\d{3})*\.\d+)$'
    O_FLT2 = r'^(\d{1,3}(,\d{3})*\.\d{2})$'
    O_FLT_2T4 = r'^(\d{1,3}(,\d{3})*\.\d{2,4})$'
    O_INT_FLT_1T4 = r'^(\d{1,3}(,\d{3})*(\.\d{1,4})?)$'
    O_INT_FLT_1T2 = r'^(\d{1,3}(,\d{3})*(\.\d{1,2})?)$'
    O_INT_FLT = r'^(\d{1,3}(,\d{3})*(\.\d+)?)$'

    FIND_O_INT = r'(\d{1,3}(?:,\d{3})*)'
    FIND_O_INT_FLT = r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)'

    FIND_DLR_GRP = r'([A-Z]{3}\s\d{1,3}(?:,\d{3})*)'

    OP_INT = r'^(\+?\d{1,3}(,\d{3})*)$'
    OP_FLT = r'^(\+?\d{1,3}(,\d{3})*\.\d+)$'
    OP_FLT2 = r'^(\+?\d{1,3}(,\d{3})*\.\d{2})$'

    ON_INT = r'^(\-?\d{1,3}(,\d{3})*)$'
    ON_FLT = r'^(\-?\d{1,3}(,\d{3})*\.\d+)$'
    ON_FLT2 = r'^(\-?\d{1,3}(,\d{3})*\.\d{2})$'

    OPN_INT = r'^([+-]?\d{1,3}(,\d{3})*)$'
    OPN_FLT = r'^([+-]?\d{1,3}(,\d{3})*\.\d+)$'
    OPN_FLT2 = r'^([+-]?\d{1,3}(,\d{3})*\.\d{2})$'


class DEPO:
    ID12 = r'^([0-9]{12})$'
    ID16 = r'^([0-9]{16})$'
    ID12_BANK_WITH_CODE = r'^\(([0-9]{3})\)([0-9]{12})$'

class TWD:
    CAP_NUM_7 = r'^([A-Z0-9]{7})$'
    FIX_NUM_INFO = r'^(共\d+筆定存)$'
    FIX_NUM_INFO_EN = r'^([1-9]\d{0,1} Term Deposit Account\(s\))$'
    INTER_OFFER_INFO = r'^(本通路剩餘跨行轉帳免手續費\s\d+\s次)$'


class FRD:
    DLRZH = r'^([\u4e00-\u9fff]{2,4})$'
    DLREG = r'^([A-Z]{3})$'
    FIXNAME = r'^([\u4e00-\u9fff]{2,4}定存)$'
    FIXIR = r'^(\d{1,3}(,\d{3})*\.\d{4}%)$'


class RATE:
    INTEREST = r'^(\+?\d{1,3}(,\d{3})*\.\d{4}%)$'


class LOAN:
    IR = r'^(\d{1,3}\.\d{2}%)$'
    IR_SPACE = r'^(\d{1,3}\.\d{2}( )?%)$'
    TERM_INFO = r'^(已繳\s?\d+\s?期，\s?共\s?\d+\s?期)$'  # 注意此處文本空格都沒有統一
    AVAIL_AMT_INFO = r'^(可動用金額 \$\d{1,3}(,\d{3})*)$'
    USED_AMT_INFO = r'^(已動用額度 \$\d{1,3}(,\d{3})*)$'
    QUOTA_AMT_INFO = r'^(貸款額度 \$\d{1,3}(,\d{3})*)$'
    ACT_INFO = r'^(最低動用 \$\d{1,3}(,\d{3})*，可動用額度 \$\d{1,3}(,\d{3})*)$'
    ACTED_MONTH_INFO = r'^(約 \$\d{1,3}(,\d{3})*)$'
    REP_INFO = r'^(最低還本 \$\d{1,3}(,\d{3})*，可還本額度 \$\d{1,3}(,\d{3})*)$'


class INVEST:
    ROI = r'^([+-]\d{1,3}(,\d{3})*(\.\d{1,2})?%)$'
    ROIRB = r'^(\([+-]\d{1,3}(,\d{3})*(\.\d{1,2})?%\))$'
    RATIO_INT_1T3 = r'^(\d{1,3}%)$'
    FIND_DATE = r'\d{4}/\d{2}/\d{2}'
    KYC_DUE_INFO = r'^(\(至\d{4}/\d{2}/\d{2}有效\))$'
    ROI_FLT2 = r'^([+-]\d{1,3}(,\d{3})*\.\d{1,2}%)$'
    YIELD_FLT2 = r'^(\d{1,3}(,\d{3})*\.\d{1,2}%)$'
    FUND_ID = r'^\d{8}$'
    FUND_NET_VALUE = r'^([A-Z]{3}) (\d{1,3})(,\d{3})*(\.\d{1,4})?$'
    FUND_ROI = r'^[+-]\d{1,3}(,\d{3})*(\.\d{1,4})?%|(--%)$'
    TSEC_TERM_DEBIT_INFO = r'^(\$\s\d+\s/\s\d+次)$'
    ASEC_TERM_SHARE_INFO = r'^(\d+股\s/\s\d+次)$'
    # 判斷包含百分比的字串是否符合規則
    # 例:(-1,234.34%)
    PERCENT_N_INCLUDE_PARENTHESES = r'^\((-)?\d{1,3}(,\d{3})*\.\d{2}%\)$'
    # 例:(+1,234.34%)
    PERCENT_PN_INCLUDE_PARENTHESES = r'^\([+-]?\d{1,3}(,\d{3})*\.\d{2}%\)$'
    # 例:(-1234.34%)
    PERCENT_N_INCLUDE_NO_COMMA_PARENTHESES = r'^\((-)?\d+\.\d{2}%\)$'
    # 例:(+1234.34%)
    PERCENT_PN_INCLUDE_NO_COMMA_PARENTHESES = r'^\([+-]?\d+\.\d{2}%\)$'


class DBC:
    MM_YY = r'^(0[1-9]|1[0-2])\/\d{2,10}$'
    DIGIT_4 = r'^\d{4}$'


class MORE:
    TREE_POINT = r'^(0|\d{1,3}(,\d{3})*|--)$'


class CUBERELATED:
    TREE_POINT_RATE = r'^(\d{1,3}(.\d{1})*)$'
    CUBE_DISCOUNT = r'^\d+(\.(?!0+$)\d+)?$'
    POINTS_FEEDBACK_DATE_DETAIL = r'\d{4} 年 (0[1-9]|1[0-2]) 月'


class DATE:
    YYYYMMDD = r'^(\d{4}/\d{2}/\d{2})$'
    FIND_YYYYMMDD = r'\d{4}/\d{2}/\d{2}'
    YYYYMM_CHS = r"^\d{4} 年 ([1-9]|1[0-2]) 月$"



class TIME:
    # 時間格式
    TIME_24HOUR = '([0-1]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]'
    TIME_24HOUR_N_MIN = '([0-1]?[0-9]|2[0-3]):[0-5][0-9]'
    TIME_12HOUR = r'^(0[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$'


class CDC:
    # 信用卡相關
    CDC_TWD_MONTH_BILL_TEXT = r"^\d+ 月臺幣帳單$"
    CDC_STMT_TTL = r'^(\d{1,2}[\u4e00-\u9fff]+)$'
    CDC_STMT_DDL = r'^([\u4e00-\u9fff]+\d{2}\/\d{2})$'
    CDC_BILL_PAGE_TITLE = r"^(\d{4} 年 (0?[1-9]|1[0-2]) 月帳單)$"
    CDC_BILL_TOTAL_COUNT = r"^共\s\d+\s筆$"
    CDC_BILL_VALUE_DATE = r"^入帳起息日 (\d{1,2})/(\d{1,2})$"
    CDC_BILL_LAST_CARD_4NUM = r"^卡號末四碼 (\d{4})$"


# 判斷台幣帳戶之參考損益是否符合顯示規則(目前用於證券)
# 例:-TWD 3,674
STOCK_TYPE_TW_PROFIT = r'^(-)?TWD \d{1,3}(,\d{3})*$'

# 擷取用 建議不要太多的 '()?+*' 判斷，容易擷取錯誤
FIND_NUMERIC = r'\d+\.\d+|\d+'


# 字元格式相關

def findall(pattern, text, index=None) -> str | list[str]:
    """
    注意pattern內有括號就會成為捕獲組，需用(?:...)來設定非捕獲組
    例如尋找 $123,456 就要設定為 r'(\\$\\d{1,3}(?:,\\d{3})*)' ，否則會只找到 ,456
    """
    matches = re.findall(pattern, text)
    logging.info(f'pattern:  {pattern}')
    logging.info(f'text:     {text}')
    logging.info(f'matches:  {matches}')
    if index is not None:
        selected = matches[index]
        logging.info(f'index:    {index}')
        logging.info(f'selected: {selected}')
        return selected
    return matches


def stock_type_float_profit(dollar):
    """
    判斷外幣帳戶之參考損益是否符合顯示規則(目前用於證券)
    例:-USD 441,290.76
    """

    return r'^(-)?' + dollar + r' \d{1,3}(,\d{3})*\.\d{2}$'


def stock_type_int_profit(dollar):
    """
    判斷金額顯示整數格式是否符合
    例:TWD 1,875
    """

    return r'^(-)?' + dollar + r' \d{1,3}(,\d{3})*$'
