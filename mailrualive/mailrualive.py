import random
import logging
import string
from .time_util import sleep
from .util import check_kill_process, gen_random_string
from .login_util import login_browser
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Remote
from socialcommons.file_manager import get_logfolder
from socialcommons.file_manager import get_workspace
from socialcommons.browser import set_selenium_local_session
from socialcommons.exceptions import SocialPyError
from .settings import Settings
import traceback
from .database_engine import get_database
from pathlib import Path


class MailruAlive:
    def __init__(
        self,
        mailru,
        mailru_password,
        headless=False,
        memory_hogging_processes=["Fire", "Chrome", "chromedriver", "DrCleaner"],
    ):
        self.mailru = mailru
        self.mailru_password = mailru_password
        self.multi_logs = True
        self.logfolder = get_logfolder(self.mailru, self.multi_logs, Settings)
        self.get_mailrualive_logger()
        for mhp in memory_hogging_processes:
            check_kill_process(mhp, self.logger)
        self.page_delay = 25
        self.use_firefox = headless
        self.headless_browser = headless
        self.disable_image_load = False
        self.browser_profile_path = None
        self.proxy_chrome_extension = None
        self.proxy_address = None
        self.proxy_address = None
        Settings.profile["name"] = self.mailru

        if not get_workspace(Settings):
            raise SocialPyError("Oh no! I don't have a workspace to work at :'(")

        get_database(Settings, make=True)
        self.set_selenium_local_session(Settings)

    def get_mailrualive_logger(self):
        self.logger = logging.getLogger(self.mailru)
        self.logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler("{}general.log".format(self.logfolder))
        file_handler.setLevel(logging.DEBUG)
        extra = {"mailru": self.mailru}
        logger_formatter = logging.Formatter(
            "%(levelname)s [%(asctime)s] [MailruAlive:%(mailru)s]  %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(logger_formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(logger_formatter)
        self.logger.addHandler(console_handler)

        self.logger = logging.LoggerAdapter(self.logger, extra)

    def set_selenium_local_session(self, Settings):
        self.browser, err_msg = set_selenium_local_session(
            self.proxy_address,
            self.proxy_address,
            self.proxy_chrome_extension,
            self.headless_browser,
            self.use_firefox,
            self.browser_profile_path,
            self.disable_image_load,
            self.page_delay,
            self.logger,
            Settings,
        )
        if len(err_msg) > 0:
            raise SocialPyError(err_msg)

    def send_a_mail(self):
        if "e.mail.ru/messages/inbox" not in self.browser.current_url:
            self.logger.info(
                "Might have encountered captcha, solve manually and press enter on terminal"
            )
            raise Exception("captcha")
            # inp = input("Solved captcha(Press enter)?")

        self.browser.get("https://e.mail.ru/messages/inbox/?back=1")
        sleep(5)

        compose_btn, pencil_btn = None, None
        try:
            compose_btn = self.browser.find_element_by_xpath(
                "//*[contains(text(), 'Написать письмо')]"
            )
        except:
            pass

        try:
            pencil_btn = self.browser.find_element_by_xpath(
                "//*[@id='app-canvas']/div/div[1]/div[1]/div/div[2]/div[1]/div/div/div[1]/div[1]/div/span"
            )
        except:
            pass

        if compose_btn:
            try:
                # compose_btn = self.browser.find_element_by_xpath(
                #     "//*[contains(text(), 'Написать письмо')]"
                # )
                ActionChains(self.browser).move_to_element(
                    compose_btn
                ).click().perform()
                self.logger.info("Clicked Написать письмо(Compose)")
                sleep(5)
                to_ele = self.browser.find_element_by_xpath(
                    "//div[1]/div/div[3]/div[1]/div/div/div[2]/div/div/div/textarea[2]"
                )
                ActionChains(self.browser).move_to_element(to_ele).click().perform()
                ActionChains(self.browser).move_to_element(to_ele).click().send_keys(
                    "ishandutta2007@gmail.com"
                ).perform()
                self.logger.info("Entered To: ishandutta2007@gmail.com")
                subjectbox_ele = self.browser.find_element_by_xpath(
                    "//input[@name='Subject']"
                )
                ActionChains(self.browser).move_to_element(
                    subjectbox_ele
                ).click().perform()
                ActionChains(self.browser).move_to_element(
                    subjectbox_ele
                ).click().send_keys(
                    "abhi hum zinda hai "
                    + gen_random_string(8, string.digits)
                    + gen_random_string(15, string.ascii_letters)
                ).perform()

                send_btn = self.browser.find_element_by_xpath(
                    "//span[contains(text(), 'Отправить')]"
                )
                ActionChains(self.browser).move_to_element(send_btn).click().perform()
                self.logger.info("Clicked Отправить(Send)")
                sleep(5)
                confirm_btn = self.browser.find_element_by_xpath(
                    "//*[@id='MailRuConfirm']/div/div[2]/form/div[2]/button[1]"
                )
                ActionChains(self.browser).move_to_element(
                    confirm_btn
                ).click().perform()
                self.logger.info("Clicked Продолжить(Confirm)")
            except Exception as e:
                traceback.print_exc()
                raise e

        if pencil_btn:
            try:
                self.logger.info("письмо is not there, lets try pencil icon")
                # pencil_btn = self.browser.find_element_by_xpath(
                #     "//*[@id='app-canvas']/div/div[1]/div[1]/div/div[2]/div[1]/div/div/div[1]/div[1]/div/span"
                # )
                ActionChains(self.browser).move_to_element(pencil_btn).click().perform()
                self.logger.info("Clicked pencil icon")
                sleep(5)

                to_ele = self.browser.find_element_by_xpath(
                    "//div[14]/div[2]/div/div[1]/div[2]/div[3]/div[2]/div/div/div[1]/div/div[2]/div/div/label/div/div/input"
                )
                ActionChains(self.browser).move_to_element(to_ele).click().perform()
                ActionChains(self.browser).move_to_element(to_ele).click().send_keys(
                    "ishandutta2007@gmail.com"
                ).perform()
                self.logger.info("Entered To: ishandutta2007@gmail.com")
                subjectbox_ele = self.browser.find_element_by_xpath(
                    "//input[@name='Subject']"
                )
                ActionChains(self.browser).move_to_element(
                    subjectbox_ele
                ).click().perform()
                ActionChains(self.browser).move_to_element(
                    subjectbox_ele
                ).click().send_keys(
                    "abhi hum zinda hai "
                    + gen_random_string(8, string.digits)
                    + gen_random_string(15, string.ascii_letters)
                ).perform()

                send_btn = self.browser.find_element_by_xpath(
                    "//span[contains(text(), 'Отправить')]"
                )
                ActionChains(self.browser).move_to_element(send_btn).click().perform()
                self.logger.info("Clicked Отправить(Send)")
                sleep(5)
                send_alert_btn = self.browser.find_element_by_xpath(
                    "//div[15]/div/div/div[2]/button[1]"
                )
                ActionChains(self.browser).move_to_element(
                    send_alert_btn
                ).click().perform()
                self.logger.info("Clicked Отправить(Send) alert")
            except Exception as e:
                traceback.print_exc()
                raise e

        sleep(5)

    def check_mail(self):
        try:
            if login_browser(
                self.mailru,
                self.mailru_password,
                self.logfolder,
                self.browser,
                self.logger,
            ):
                self.send_a_mail()
            else:
                print("Login Failed")
            if self.browser:
                self.browser.quit()
        except Exception as e:
            traceback.print_exc()
            if self.browser:
                self.browser.quit()
            raise e
