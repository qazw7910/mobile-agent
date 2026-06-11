import re
import time
from datetime import datetime

import pytest

import logging

from framework import common, path, global_adapter
from framework import global_adapter as ga
from module.mobile.globalvar import GlobalVar


def pytest_addoption(parser):
    """
    設置pytest custom sys args
    """
    # GlobalVar.PLATFORM = "ios"

    parser.addoption('--allure', action='store', default='allure', type=str, help="CI用，設置allure在執行機器的絕對路徑")
    parser.addoption('--platform', action='store', default='android', choices=['ios', 'android'], type=str,
                     help="設定測試平台")
    parser.addoption('--product', action='store', default='cube', choices=['cube'], type=str, help="設定測試產品")
    parser.addoption('--env', action='store', default='uat', choices=['stg', 'uat', 'ut'], type=str,
                     help="設定測試環境")
    parser.addoption('--aws', action='store_true', default=False, help="執行 aws device farm 流程")
    parser.addoption('--app_path', action='store', type=str, help="APP檔案路徑")


@pytest.fixture(scope='session', autouse=True)
def allure(pytestconfig):
    """
    CI用，設置allure在執行機器的絕對路徑
    此處因 xdist 全域變數衝突問題改成紀錄於 txt 內
    """
    allure_path = pytestconfig.getoption('--allure')
    common.write_txt_by(path.Base.ALLURE_PATH_TXT, allure_path)
    return allure_path


@pytest.fixture(scope='session')
def env(pytestconfig):
    """
    取得測試環境appid
    """
    platform = pytestconfig.getoption('--platform')
    product = pytestconfig.getoption('--product')
    env = pytestconfig.getoption('--env')
    GlobalVar.PRODUCT = product
    GlobalVar.ENV = env
    return common.read_json_by(path.Data.JSON_APP_ENV, platform, product, env)


def pytest_configure(config):
    """
    初始化 ElasticSearch 連線
    """
    global_adapter.CommonVar.PLATFORM = config.getoption('--platform').lower()
    global_adapter.CommonVar.APP_PATH = config.getoption('--app_path')


@pytest.fixture(scope='session', autouse=True)
def aws(pytestconfig):
    """
    aws device farm 流程
    """
    aws = pytestconfig.getoption('--aws')
    GlobalVar.AWS = aws
    return aws


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    收集測試結果
    :terminalreporter: 內部使用的終端測試報告對象
    :exitstatus: 返回操作系統的返回碼
    :config: pytest設定資料
    """
    settings = {
        'platform': 'mmb',
        'product': 'cube',
        'priority': 'p1'
    }
    marker = config.option.markexpr
    marker_list = re.sub(r'\band\b', '', marker).split()
    for marker in marker_list:
        if marker.lower() in ['ios', 'android']:
            settings['platform'] = marker
        elif marker.lower() in ['p1', 'p2', 'p3']:
            settings['priority'] = marker

    iso_date = datetime.now().isoformat() + "+0800"
    test_start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(terminalreporter._sessionstarttime))
    test_end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    test_duration = f'{round(time.time() - terminalreporter._sessionstarttime, 2)}s'
    total_cases = int(terminalreporter._numcollected - len(terminalreporter.stats.get("deselected", [])))  # 實際執行case總數
    pass_cases = len([item for item in terminalreporter.stats.get(
        "passed", []) if item.when != "teardown"])  # case結果為pass的數量
    fail_cases = len([item for item in terminalreporter.stats.get(
        "failed", []) if item.when != "teardown"])  # case結果為fail的數量
    error_cases = len([item for item in terminalreporter.stats.get(
        "error", []) if item.when != "teardown"])  # case結果為error的數量
    skipped_cases = len([item for item in terminalreporter.stats.get(
        "skipped", []) if item.when != "teardown"])  # case skip的數量
    pass_rate = fail_rate = 0
    if total_cases != 0:
        pass_rate = round(pass_cases / total_cases * 100, 2)  # 計算test run中所有case的成功率，四捨五入到小數點第二位
        fail_rate = round(fail_cases / total_cases * 100, 2)  # 計算test run中所有case的失敗率，四捨五入到小數點第二位
        logging.info(f"pass_rate: {pass_rate}%, fail_rate: {fail_rate}%")

    ga.DBVar.TEST_REPORT.update({
        "@timestamp": iso_date,
        "test_start_time": test_start_time,
        "test_end_time": test_end_time,
        "test_duration": test_duration,
        "platform": settings['platform'],
        "product": settings['product'],
        "test_scope": f"{settings['product']}_{settings['priority']}",
        # "allure_report_path": f"{REPORT_DATETIME_DIR}/allure_{RUN_DATETIME}.html", 因xdist執行緒特性會導致無法事前定下時間，此處待確認如何處理。
        "total_cases": total_cases,
        "pass_cases": pass_cases,
        "fail_cases": fail_cases,
        "error_cases": error_cases,
        "skipped_cases": skipped_cases,
        "pass_rate": f"{pass_rate}%",
        "fail_rate": f"{fail_rate}%"
    })


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    蒐集測試案例執行結果
    :item: 測試用例
    :call: 測試步驟
    """
    report_result = ga.DBVar.TEST_REPORT
    report = (yield).get_result()
    if report.when == "call":
        try:
            start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(call.start))  # 測案開始時間
            stop_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(call.stop))  # 測案結束時間
            duration = f"{call.duration:.3f}s"  # 測案執行時間
            capture_log = [logs for section in report.sections for logs in section]  # 抓取自己埋的log
            capture_self_log = capture_log[-1] if capture_log else ""

            if item.parent.name not in report_result:
                report_result[item.parent.name] = []
            report_result[item.parent.name].append(
                {"case_name": item.name, "node_id": report.nodeid, "test_result": report.outcome,
                 "start_time": start_time, "stop_time": stop_time, "duration": duration,
                 "report_exception_log": report.longreprtext,
                 "capture_self_log": capture_self_log})
        except Exception as e:
            logging.error(f"{e}")
