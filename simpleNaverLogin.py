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
USER_ID = os.getenv("NAVER_USER_ID")
PASSWORD = os.getenv("NAVER_PASSWORD")
LOGIN_URL = "https://nid.naver.com/nidlogin.login"
# ============

class NaverSimpleLogin():
    def __init__(self):
        self.driverPath = os.path.realpath('/program/chromedriver_win32/chromedriver.exe')
        self.driver = None

    def __del__(self):
        pass

    def DriverCheck(targetFunction):
        def wrapper(self, *args, **kwargs):
            if self.driver == None:
                print("Driver not ready, calling SetDriver()...")
                self.SetDriver()
            return targetFunction(self, *args, **kwargs)
        return wrapper

    def SetDriver(self):
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


    @DriverCheck
    def Login(self, userId, password):
        try:
            self.driver.get("http://www.naver.com")
            self.driver.implicitly_wait(5)
            print("Trying to Login : %s" % (LOGIN_URL))
            self.driver.get(LOGIN_URL)
            self.driver.implicitly_wait(5)
            time.sleep(randrange(2,5))

            self.driver.find_element_by_name('id').send_keys(userId)
            time.sleep(1)
            self.driver.find_element_by_name("pw").send_keys(password)
            time.sleep(randrange(2,4))
            self.driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
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
    daemon = NaverSimpleLogin()
    daemon.Login(USER_ID, PASSWORD)

    input("[*] Press Enter to exit")

if __name__ == '__main__':
    main()



