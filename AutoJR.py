# -*- encoding=utf8 -*-
__author__ = "Nickydusk"

from strategy import *

import logging
logger = logging.getLogger('airtest')
logger.setLevel(logging.ERROR)


st = tmpStrategy()
st.main_loop()


