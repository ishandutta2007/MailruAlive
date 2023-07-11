from math import ceil
import signal
from platform import system
from platform import python_version
from subprocess import call
import sqlite3
from contextlib import contextmanager
from argparse import ArgumentParser
import os
import re

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from .time_util import sleep
from .time_util import sleep_actual

# from .database_engine import get_database
from .settings import Settings

from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException

_nonbmp = re.compile(r"[\U00010000-\U0010FFFF]")

import random
import hashlib
import string


def gen_random_string(length=8, chars=string.ascii_letters + string.digits):
    return "".join([random.choice(chars) for i in range(length)])


def check_kill_process(pstring, logger):
    for line in os.popen("ps ax | grep " + pstring + " | grep -v grep"):
        try:
            fields = line.split()
            pid = fields[0]
            os.kill(int(pid), signal.SIGKILL)
            logger.info("{} killed".format(pstring))
        except Exception as e:
            logger.error(e)
