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

CJ_LOGIN_URL = os.getenv("CJ_LOGIN_URL")
CJ_MAIL_URL = os.getenv("CJ_MAIL_URL")
CJ_ID_TAG_NAME = "txtID"
CJ_PW_TAG_NAME = "txtPWD"
CJ_XPATH_LOGIN_BTN = '//*[@id="frm_login"]//*[@class="btn_login"]'
CJ_USER_ID = os.getenv("CJ_USER_ID")        # CJ_PASSWORD TARGETPICK_USER_ID
CJ_PASSWORD = os.getenv("CJ_PASSWORD")      # CJ_PASSWORD TARGETPICK_USER_ID


LOGIN_TYPE = "fb"
# ============


class LoginData:
    def __init__(self, login_url, id_tag_name, pw_tag_name, xpath_login_btn, user_id, password, lazy_input_type=True):
        self.login_url = login_url
        self.id_tag_name = id_tag_name
        self.pw_tag_name = pw_tag_name
        self.xpath_login_btn = xpath_login_btn
        self.user_id = user_id
        self.password = password
        self.lazy_input_type = lazy_input_type


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
            elif type == "cj":
                login_data = LoginData(CJ_LOGIN_URL, CJ_ID_TAG_NAME, CJ_PW_TAG_NAME, CJ_XPATH_LOGIN_BTN, CJ_USER_ID, CJ_PASSWORD, False)
            else:
                login_data = LoginData(TP_LOGIN_URL, TP_ID_TAG_NAME, TP_PW_TAG_NAME, TP_XPATH_LOGIN_BTN, TP_USER_ID, TP_PASSWORD)

            login_uri = login_data.login_url
            tag_id = login_data.id_tag_name
            tag_pw = login_data.pw_tag_name
            xpath_login_btn = login_data.xpath_login_btn
            user_id = login_data.user_id
            password = login_data.password
            lazy_input_type = login_data.lazy_input_type

            # 1. LAND TO LOGIN PAGE
            self.driver.get(login_uri)
            self.driver.implicitly_wait(5)

            # 2. TYPE ID/PW
            el_id = self.driver.find_element_by_name(tag_id)
            if lazy_input_type:
                key = 0
                for character in user_id:
                    el_id.send_keys(character)
                    if key < 4:
                        time.sleep(randrange(1, 5)/10)
                    else:
                        time.sleep(randrange(1, 10)/100)
                    key += 1
            else:
                el_id.send_keys(user_id)
            time.sleep(randrange(2, 5))

            el_pw = self.driver.find_element_by_name(tag_pw)
            if lazy_input_type:
                for character in password:
                    el_pw.send_keys(character)
                    time.sleep(randrange(2, 6)/10)
            else:
                el_pw.send_keys(password)
            time.sleep(randrange(2, 4))

            # 3. TRY TO LOGIN
            self.driver.find_element_by_xpath(xpath_login_btn).click()
            self.driver.implicitly_wait(3)

            # 4. After login
            if type == "cj":
                self.driver.get(CJ_MAIL_URL)
                time.sleep(2)
                # crawl email title and print out..
                page = self.driver.page_source
                soup = BeautifulSoup(page)
                titles = soup.select(".tdSubject")
                for title in titles:
                    print(">> ## 자동 메일 스크랩 제목입니다: " + title.text)


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



