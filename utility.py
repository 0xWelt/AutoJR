# -*- encoding=utf8 -*-
__author__ = "Nickydusk"

""" 由于airtest部分API过于僵硬，需要手动从更底层实现一些新的封装 """

import time
from airtest.core.api import logwrap, loop_find, TargetNotFoundError,Template
from airtest.core.cv import try_log_screen
from airtest.core.helper import G
from CONSTS import *


@logwrap
def exists(v, timeout=1, threshold=0.7, interval=0):
    r""" 加入: 自定义超时、相似阈值 """

    try:
        pos = loop_find(v, timeout, threshold, interval)
    except TargetNotFoundError:
        return False
    else:
        return pos

@logwrap
def touch(v, times=1, timeout=5, threshold=0.7, interval=0, delay=0.75, **kwargs):
    r""" 加入: 找不到返回False、自定义超时 """

    if isinstance(v, Template):
        try:
            pos = loop_find(v, timeout, threshold, interval)
        except TargetNotFoundError:
            return False            # 加入了报错功能
    else:
        try_log_screen()
        pos = v
    for _ in range(times):
        G.DEVICE.touch(pos, **kwargs)
        time.sleep(0.05)

    time.sleep(delay)     # 控制点击之后休息多久
    return pos

