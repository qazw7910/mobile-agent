import os
import shutil
import sys
import logging
from datetime import datetime

import pytest

from framework import cleaning, allure_generator
from framework import path, common,logconfig

if __name__ == "__main__":

    logconfig.basic(path.Log.LOG)

    TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_dir= os.path.join(path.REPORTS,TIMESTAMP)
    report_path= os.path.join(report_dir,f"allure_{TIMESTAMP}.html")
    common.write_txt_by(path.Base.TIMESTAMP_TXT, TIMESTAMP)

    pytest.main()
    # pytest.main([
    #     '--platform','android',
    #     '-m','gmb_login'
    # ])
    # pytest.main([
    #     '--platform','ios',
    #     '-m','iWA_login',
    #     '--app_path','/Users/twinb00551192/Desktop/QA_file/iWA-DEV.app',
    #     '--alluredir','./reports/allure_tmp',
    # ])


    allure_generator.output_allure_html()
    # 複製html到根目錄
    shutil.copyfile(f"{report_path}",f"{path.BASE}/output.html")
    # 刪除report dir
    shutil.rmtree(report_dir)

    cleaning.remove_logs()
    cleaning.remove_allure_tmp()