from module.mobile.navigator import Navigator
import logging

def login_process_android():
    navigator = Navigator().android.zh
    navigator.gmb_login_page.pre_login().assert_visible()
    navigator.gmb_login_page.login_slogan().assert_visible()
    navigator.gmb_login_page.id_input().is_visible()
    navigator.gmb_login_page.id_input().send_keys("65141474")
    navigator.gmb_login_page.user_name().send_keys("admin01")
    navigator.gmb_login_page.user_pwd().send_keys("Ab123456")
    navigator.gmb_login_page.login_btn().click()
    logging.info("✅ 成功登入GMB Android")

def login_process_ios():
    navigator = Navigator().ios.zh
    navigator.ios_login_page.login_slogan().assert_visible()
    navigator.ios_login_page.id_input().is_visible()
    navigator.ios_login_page.id_input().click()
    navigator.ios_login_page.id_input().send_keys("65141474")
    navigator.ios_login_page.user_name().send_keys("admin01")
    navigator.ios_login_page.user_pwd().send_keys("Ab123456")
    navigator.ios_overview_page.save_screenshot(case='photo', name='輸入使用者資訊', attach_jpg=True, remove=True)
    navigator.ios_login_page.login_btn().click()
    logging.info("✅ 成功登入GMB iOS")