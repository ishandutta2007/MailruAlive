import random
import os
import signal
import logging
import pickle
import re
import pprint as pp
import sqlite3
import math
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Remote
from .time_util import sleep
from socialcommons.file_manager import get_logfolder
from socialcommons.file_manager import get_workspace
from socialcommons.browser import set_selenium_local_session
from socialcommons.exceptions import SocialPyError
from .settings import Settings
import traceback
from .database_engine import get_database
import configparser
from .time_util import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import MoveTargetOutOfBoundsException


def login_browser(mailru, mailru_password, logfolder, browser, logger):
    try:
        browser.get("https://mail.ru")
        sleep(10)

        input_mailru = browser.find_element_by_xpath("//input[@id='mailbox:login']")
        (
            ActionChains(browser)
            .move_to_element(input_mailru)
            .click()
            .send_keys(mailru)
            .perform()
        )
        logger.info("Entered Email: {}".format(mailru))
        sleep(1)

        submit_mailru = browser.find_element_by_xpath("//input[@type='submit']")
        (ActionChains(browser).move_to_element(submit_mailru).click().perform())
        logger.info("Submitted Email")
        sleep(5)

        input_pass = browser.find_element_by_xpath("//input[@id='mailbox:password']")
        (
            ActionChains(browser)
            .move_to_element(input_pass)
            .click()
            .send_keys(mailru_password)
            .perform()
        )
        logger.info("Entered Pass: {}".format(mailru_password))
        sleep(1)

        submit_pass = browser.find_element_by_xpath("//input[@type='submit']")
        (ActionChains(browser).move_to_element(submit_pass).click().perform())
        logger.info("Submitted Pass")

        sleep(5)

    except Exception as e:
        logger.error(e)
        if browser:
            browser.quit()
        return False

    return True
