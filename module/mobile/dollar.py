import logging

class D:
    TWD = 'TWD'
    SGD = 'SGD'
    AUD = 'AUD'
    JPY = 'JPY'
    EUR = 'EUR'
    USD = 'USD'
    HKD = 'HKD'
    CNY = 'CNY'
    CAD = 'CAD'
    SEK = 'SEK'
    ZAR = 'ZAR'
    GBP = 'GBP'
    DKK = 'DKK'
    THB = 'THB'
    NZD = 'NZD'
    CHF = 'CHF'


class Dollar:

    MAP = {
        'TWD': '新台幣',
        'SGD': '新加坡幣',
        'AUD': '澳幣',
        'JPY': '日幣',
        'EUR': '歐元',
        'USD': '美元',
        'HKD': '港幣',
        'CNY': '人民幣',
        'CAD': '加拿大幣',
        'SEK': '瑞典幣',
        'ZAR': '南非幣',
        'GBP': '英鎊',
        'DKK': '丹麥幣',
        'THB': '泰國銖',
        'NZD': '紐西蘭幣',
        'CHF': '瑞士法郎',
        'TRY': '土耳其里拉'
    }

    EG = list(MAP.keys())
    ZH = list(MAP.values())
    ZHEG = [f'{value} {key}' for key, value in MAP.items()]

    INTDLR = [D.TWD, D.JPY]

    def twd_to_frd(twd: int, fxr: int | float, frdeg: str) -> (int | float):
        """
        計算臺幣換匯後的外幣金額
        :param twd_iamount: 轉出的臺幣金額
        :param frd_nrate: 外幣對臺幣匯率
        :param frd_eng: 外幣英文幣別
        """
        if frdeg in Dollar.INTDLR:
            frd = round(twd / fxr)
        else:
            frd = round(twd / fxr, 2)
            if frd.is_integer():
                frd = int(frd)
        logging.info(f'frdeg: {frdeg}')
        logging.info(f'twd: {twd}, type: {type(twd)}')
        logging.info(f'fxr: {fxr}, type: {type(fxr)}')
        logging.info(f'frd: {frd}, type: {type(frd)}\n')
        return frd

    def frd_to_twd(frd: int | float, fxr: int | float) -> int:
        """
        計算臺幣換匯後的外幣金額
        :param twd_iamount: 轉出的臺幣金額
        :param frd_nrate: 外幣對臺幣匯率
        :param frd_eng: 外幣英文幣別
        """
        twd = round(frd * fxr)
        logging.info(f'frd: {frd}, type: {type(frd)}')
        logging.info(f'fxr: {fxr}, type: {type(fxr)}')
        logging.info(f'twd: {twd}, type: {type(twd)}\n')
        return twd

    def frd_to_frd(src: int | float, fxr: int | float, dsteg: str) -> int | float:
        """
        注意這邊匯率計算並沒有統一
        """
        if dsteg in Dollar.INTDLR:
            dst = round(src * fxr)
        else:
            dst = round(src * fxr, 2)
            if dst.is_integer():
                dst = int(dst)
        logging.info(f'frdeg: {dsteg}')
        logging.info(f'src: {src}, type: {type(src)}')
        logging.info(f'fxr: {fxr}, type: {type(fxr)}')
        logging.info(f'frd: {dst}, type: {type(dst)}\n')
        return dst
