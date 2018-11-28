import os
import time
from dotenv import load_dotenv
from random import randrange

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import *


# === Config ===
load_dotenv()
HEADLESS = False
SEARCH_KEYWORD = None
DOWNLOAD_PATH = os.path.realpath("download")

NAVER_LOGIN_URL = "https://nid.naver.com/nidlogin.login"
NAVER_ID_TAG_NAME = "id"
NAVER_PW_TAG_NAME = "pw"
NAVER_XPATH_LOGIN_BTN = '//*[@id="frmNIDLogin"]/fieldset/input'
NAVER_USER_ID = os.getenv("NAVER_USER_ID")        # NAVER_PASSWORD TARGETPICK_USER_ID
NAVER_PASSWORD = os.getenv("NAVER_PASSWORD")      # NAVER_PASSWORD TARGETPICK_USER_ID

TP_LOGIN_URL = "http://www-dev.targetpick.co.kr/login"
TP_ID_TAG_NAME = "email"
TP_PW_TAG_NAME = "password"
TP_XPATH_LOGIN_BTN = '//*[@id="login-form"]//*[@type="submit"]'
TP_USER_ID = os.getenv("TP_USER_ID")        # NAVER_PASSWORD TARGETPICK_USER_ID
TP_PASSWORD = os.getenv("TP_PASSWORD")      # NAVER_PASSWORD TARGETPICK_USER_ID

FB_LOGIN_URL = "https://www.facebook.com/"
FB_ID_TAG_NAME = "email"
FB_PW_TAG_NAME = "pass"
FB_XPATH_LOGIN_BTN = '//*[@id="login_form"]//*[@type="submit"]'
FB_USER_ID = os.getenv("FB_USER_ID")        # NAVER_PASSWORD TARGETPICK_USER_ID
FB_PASSWORD = os.getenv("FB_PASSWORD")      # NAVER_PASSWORD TARGETPICK_USER_ID

LOGIN_TYPE = "tp"
# ============


class LoginData:
    def __init__(self, login_url, id_tag_name, pw_tag_name, xpath_login_btn, user_id, password):
        self.login_url = login_url
        self.id_tag_name = id_tag_name
        self.pw_tag_name = pw_tag_name
        self.xpath_login_btn = xpath_login_btn
        self.user_id = user_id
        self.password = password


class SimpleLoginDaemon:
    def __init__(self):
        self.driverPath = os.path.realpath('/program/chromedriver_win32/chromedriver.exe')
        self.driver = None

    def __del__(self):
        pass

    def driver_check(targetFunction):
        def wrapper(self, *args, **kwargs):
            if self.driver == None:
                print("Driver not ready, calling SetDriver()...")
                self.set_driver()
            return targetFunction(self, *args, **kwargs)
        return wrapper

    def set_driver(self):
        options = webdriver.ChromeOptions()
        options.headless = HEADLESS
        preferences = {
            "download.default_directory": DOWNLOAD_PATH,
            "directory_upgrade": True,
            "safebrowsing.enabled": True,
            "profile.default_content_setting_values.automatic_downloads": 2
        }
        options.add_experimental_option("prefs", preferences)
        self.driver = webdriver.Chrome(executable_path = self.driverPath, chrome_options = options)
        self.driver.set_page_load_timeout(15)
        self.driver.set_window_size(1000, 500)
        self.driver.set_window_position(200, 200)
        print("Driver Setting Completed")


    @driver_check
    def login(self, type="naver"):
        try:
            # 0. VAR SET
            if type == "fb":
                login_data = LoginData(FB_LOGIN_URL, FB_ID_TAG_NAME, FB_PW_TAG_NAME, FB_XPATH_LOGIN_BTN, FB_USER_ID, FB_PASSWORD)
            elif type == "naver":
                login_data = LoginData(NAVER_LOGIN_URL, NAVER_ID_TAG_NAME, NAVER_PW_TAG_NAME, NAVER_XPATH_LOGIN_BTN, NAVER_USER_ID, NAVER_PASSWORD)
            else:
                login_data = LoginData(TP_LOGIN_URL, TP_ID_TAG_NAME, TP_PW_TAG_NAME, TP_XPATH_LOGIN_BTN, TP_USER_ID, TP_PASSWORD)

            login_uri = login_data.login_url
            tag_id = login_data.id_tag_name
            tag_pw = login_data.pw_tag_name
            xpath_login_btn = login_data.xpath_login_btn
            user_id = login_data.user_id
            password = login_data.password

            # 1. LAND TO LOGIN PAGE
            self.driver.get(login_uri)
            self.driver.implicitly_wait(5)

            # 2. TYPE ID/PW
            el_id = self.driver.find_element_by_name(tag_id)
            for character in user_id:
                el_id.send_keys(character)
                time.sleep(randrange(1, 5)/10)
            #self.driver.find_element_by_name('id').send_keys(userId)
            time.sleep(randrange(2, 5))

            el_pw = self.driver.find_element_by_name(tag_pw)
            for character in password:
                el_pw.send_keys(character)
                time.sleep(randrange(2, 6)/10)
            #self.driver.find_element_by_name("pw").send_keys(password)
            time.sleep(randrange(2, 4))

            # 3. TRY TO LOGIN
            self.driver.find_element_by_xpath(xpath_login_btn).click()

            try:
                self.driver.find_element_by_class_name('link_login_help')
            except NoSuchElementException:
                pass
            else:
                print("Login failed: Captcha Occured, Try Later")
                return False

        except Exception as e:
            print("Login failed: Unknown Exception")
            return False
        else:
            print("Login Success")
            return True


def main():
    daemon = SimpleLoginDaemon()
    daemon.login(LOGIN_TYPE)
    input("[*] Press Enter to exit")


if __name__ == '__main__':
    main()



