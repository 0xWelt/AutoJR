# -*- encoding=utf8 -*-
__author__ = "NickyDusk"

from airtest.core.api import *
from control import *
from policy import *
from strategy import *

import logging
logger = logging.getLogger('airtest')
logger.setLevel(logging.ERROR)

import time




auto_setup(__file__,devices=['android://'])

check_and_login(first_time=True)
SL(big=True)