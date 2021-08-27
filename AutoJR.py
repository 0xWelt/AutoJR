# -*- encoding=utf8 -*-
__author__ = "Nickydusk"

from airtest.core.api import auto_setup,sleep
from template import *
from control import *
from policy import *
from strategy import *

import logging
logger = logging.getLogger('airtest')
logger.setLevel(logging.ERROR)

import time


auto_setup(__file__,devices=['android://'])

GC = GameController("config.json")

# 主循环，简易控制
while True:
    GC.check_and_expedition()
    GC.check_missions()
    
    sleep(10)

