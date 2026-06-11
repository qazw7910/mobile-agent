import os
import shutil
import logging

# 此處函數不要帶參數，避免刪除別份檔案


def remove_logs():
    dir = './log'
    os.makedirs(dir, exist_ok=True)
    limit = 10
    try:
        file_list = os.listdir(dir)
        len_file_list = len(file_list)
        if len_file_list > limit:
            logging.warning(f'🟡 資料夾 {dir} 中超過 {limit} 份log檔案，依照檔名時間戳開始刪除最舊的 {limit} 份')
            sorted_files = sorted(file_list)
            oldest_files = sorted_files[:limit]
            for index, filename in enumerate(oldest_files, 1):
                index = str(index).zfill(2)
                file_path = os.path.join(dir, filename)
                try:
                    os.remove(file_path)
                    logging.warning(f'🟡✅ 從資料夾 {dir} 中成功刪除 log檔案{index} {filename}')
                except BaseException:
                    logging.error(f'🟡❌ 從資料夾 {dir} 中刪除 log檔案{index} {filename} 時發生錯誤，請確認是否為資料夾或其他因素')
        else:
            logging.info(f'✅ 資料夾 {dir} 中目前檔案數量為 {len_file_list} 份，尚未超過上限 {limit} 份，不刪除任何log檔案')
    except BaseException:
        logging.error(f'❌ 有其餘非預期錯誤，請再次確認')


def remove_reports():
    dir = './reports'
    os.makedirs(dir, exist_ok=True)
    limit = 10
    try:
        file_list = os.listdir(dir)
        if '.DS_Store' in file_list:
            file_list.remove('.DS_Store')
            logging.warning(f'🟡 資料夾 {dir} 中存在 .DS_Store 檔案，已從候選列表移除')
        else:
            logging.info(f'✅ 資料夾 {dir} 中不存在 .DS_Store 檔案')
        if 'allure_tmp' in file_list:
            file_list.remove('allure_tmp')
            logging.warning(f'🟡 資料夾 {dir} 中存在 allure_tmp 資料夾，已從候選列表移除')
        else:
            logging.info(f'✅ 資料夾 {dir} 中不存在 allure_tmp 資料夾')

        len_file_list = len(file_list)
        if len_file_list > limit:
            logging.warning(f'🟡 資料夾 {dir} 中超過 {limit} 份report資料夾，依照資料夾時間戳開始刪除最舊的 {limit} 份')
            sorted_files = sorted(file_list)
            oldest_files = sorted_files[:limit]
            for index, filename in enumerate(oldest_files, 1):
                index = str(index).zfill(2)
                file_path = os.path.join(dir, filename)
                try:
                    shutil.rmtree(file_path)
                    logging.warning(f'🟡✅ 從資料夾 {dir} 中成功刪除 report資料夾{index} {filename} ')
                except BaseException:
                    logging.error(f'🟡❌ 從資料夾 {dir} 中刪除 report資料夾{index} {filename} 時發生錯誤，請確認是否為檔案或其他因素')
        else:
            logging.info(f'✅ 資料夾 {dir} 中目前report資料夾數量為 {len_file_list} 份，尚未超過上限 {limit} 份，不刪除任何report資料夾')
    except BaseException:
        logging.error(f'❌ 刪除時發生錯誤，請再確認操作是否正確')


def remove_allure_tmp():
    dir = './reports'
    os.makedirs(dir, exist_ok=True)
    limit = 10
    try:
        file_list = os.listdir(dir)
        # 完全刪除 allure_tmp 資料夾
        if 'allure_tmp' in file_list:
            allure_tmp_path = os.path.join(dir, 'allure_tmp')
            try:
                shutil.rmtree(allure_tmp_path)
                logging.warning(f'🟡✅ 已完全刪除 {allure_tmp_path} 資料夾')
            except BaseException:
                logging.error(f'❌ 刪除 {allure_tmp_path} 資料夾失敗')
            file_list.remove('allure_tmp')
        if '.DS_Store' in file_list:
            file_list.remove('.DS_Store')
            logging.warning(f'🟡 資料夾 {dir} 中存在 .DS_Store 檔案，已從候選列表移除')
        else:
            logging.info(f'✅ 資料夾 {dir} 中不存在 .DS_Store 檔案')
        len_file_list = len(file_list)
        if len_file_list > limit:
            logging.warning(f'🟡 資料夾 {dir} 中超過 {limit} 份report資料夾，依照資料夾時間戳開始刪除最舊的 {limit} 份')
            sorted_files = sorted(file_list)
            oldest_files = sorted_files[:limit]
            for index, filename in enumerate(oldest_files, 1):
                index = str(index).zfill(2)
                file_path = os.path.join(dir, filename)
                try:
                    shutil.rmtree(file_path)
                    logging.warning(f'🟡✅ 從資料夾 {dir} 中成功刪除 report資料夾{index} {filename} ')
                except BaseException:
                    logging.error(f'❌ 刪除 {file_path} 失敗')
        else:
            logging.info(f'✅ 資料夾 {dir} 中目前僅有 {len_file_list} 份，不需刪除')
    except BaseException:
        logging.error(f'❌ 有其餘非預期錯誤，請再次確認')

