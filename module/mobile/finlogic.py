# 驗證財務邏輯，比如換匯計算等等

weekday_base_list = ['週一', '週二', '週三', '週四', '週五', '週六', '週日']
weekday_each_list = ['每週一', '每週二', '每週三', '每週四', '每週五', '每週六', '每週日']
weekday_choice_eng = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_each_only_num = ['一', '二', '三', '四', '五', '六', '日']


def account_id_12to16(account_id12: str) -> str:
    """
    將12碼帳號前面補0，補至16碼為止\\
    例如: '001506213238' -> '0000001506213238'
    """
    return f'0000{account_id12}'


def account_id_16to12(account_id16: str) -> str:
    """
    將12碼帳號前面補0，補至16碼為止\\
    例如: '0000001506213238' -> '001506213238'
    """
    return account_id16[4:]


def bank_split(bank_com: str) -> dict:
    """
    """
    bank_rb = bank_com.split()[0]
    bank_zh = bank_com.split()[1]
    bank = {'rb': bank_rb, 'zh': bank_zh}
    return bank


def name_replace(name: str) -> str:
    """
    """
    return name.replace('Ｏ', 'O')


def name_replace_acc_detail(name: str) -> str:
    """
    """
    return name.replace('ｏ', '＊').replace('I', 'Ｉ').replace('D', 'Ｄ')
