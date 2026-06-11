import subprocess
import time

import logging

import requests


class AppiumManager:

    def __init__(self, port):
        self.port = port
        self.process = None

    def is_running(self):
        """檢查 Appium server 是否正在運行"""
        try:
            response = requests.get(f"http://127.0.0.1:{self.port}/status", timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    def start(self):
        """啟動 Appium server"""
        if self.process is not None and self.is_running():
            logging.info(f"🔁 Appium Server 已經在 port {self.port} 運行中")
            return

        try:
            logging.info(f"🚀 嘗試啟動 Appium Server（port {self.port}）...")
            self.process = subprocess.Popen(
                ["appium", "-p", str(self.port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8'
            )

            # 等待最多 10 秒確認 server 啟動
            for i in range(10):
                if self.is_running():
                    print(f"✅ Appium Server 已啟動在 port {self.port}")
                    logging.info(f"✅ Appium Server 已啟動在 port {self.port}")
                    return
                time.sleep(1)

            raise RuntimeError(f"❌ Appium Server 在 port {self.port} 啟動失敗")

        except subprocess.CalledProcessError as e:
            logging.error(f"🚨 啟動 Appium Server 發生 subprocess 錯誤: {e}")
            raise
        except Exception as e:
            logging.error(f"🚨 Appium Server 啟動錯誤: {e}")
            raise

    def stop(self):
        """關閉 Appium server"""
        if self.process:
            logging.info(f"🛑 正在關閉 Appium Server（port {self.port}）...")
            self.process.terminate()
            self.process.wait()
            self.process = None
            print("✅ Appium Server 已關閉")
            logging.info("✅ Appium Server 已關閉")
        else:
            logging.warning("⚠️ Appium Server 尚未啟動")

    def restart(self):
        """重新啟動 Appium server"""
        logging.info("🔄 重新啟動 Appium Server")
        self.stop()
        time.sleep(2)
        self.start()


if __name__ == '__main__':
    appium = AppiumManager(port=4801)

    # appium.start()
    # appium.restart()
    # appium.stop()
