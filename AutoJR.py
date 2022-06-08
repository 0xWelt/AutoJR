# -*- encoding=utf8 -*-
__author__ = "Nickydusk"

import logging

from strategy import *

logger = logging.getLogger('airtest')
logger.setLevel(logging.ERROR)


st = tmpStrategy()
st.main_loop()
