# -*- encoding=utf8 -*-
__author__ = "Nickydusk"

from airtest.core.api import auto_setup,sleep
from template import *
from control import *
from strategy import *

import logging
logger = logging.getLogger('airtest')
logger.setLevel(logging.ERROR)

import time


auto_setup(__file__,devices=['android://'])

GC = GameController("config.json")

# 主循环，简易控制
while True:
    print(time.ctime())
    GC.check_and_expedition()
    GC.check_missions()
    GC.check_mail()
    
    sleep(575)


