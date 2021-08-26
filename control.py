# -*- encoding=utf8 -*-
__author__ = "dh"

from airtest.core.api import *
import time
import json
import os

jryx = Template(r"pictures/ui/进入游戏.png", record_pos=(0.385, 0.204), resolution=(1280, 720))

def check_and_login(first_time=False):
    r''' 登录游戏，如果发现账号未登录则先登录，账号密码放在config.json中
    '''
    # 启动游戏
    start_app(r"com.huanmeng.zhanjian2")
    sleep(5)
    times=-1
    print(times)
    while not exists(jryx):
        times+=1
        print(times)
        # case 1: 需要下载
        if exists(Template(r"pictures/ui/确认.png", record_pos=(-0.12, 0.037), resolution=(1280, 720))):
            print('检测到：下载资源！')
            touch((-0.12, 0.037))
            sleep(5)
        # case 2: 需要确认模拟器权限
        elif first_time and exists(Template(r"pictures/ui/雷电模拟器/允许.png", record_pos=(0.151, 0.001), resolution=(1280, 720))):
            print('检测到：模拟器权限允许！')
            touch((0.151, 0.001))
        # case 3: 需要确认游戏条款
        elif first_time and exists(Template(r"pictures/ui/接受.png", record_pos=(-0.102, 0.17), resolution=(1280, 720))):
            print('检测到：确认条款！')
            touch((-0.102, 0.17))
            sleep(1)
        # case 4: 需要登录
        elif first_time and exists(Template(r"pictures/ui/账号登陆.png", record_pos=(-0.002, -0.151), resolution=(1280, 720))):
            print('检测到：账号登陆！')
            touch((-0.196, -0.079))

            with open('config.json','r') as f:
                config = json.load(f)
            
            text(config['username'])
            text(config['passwd'])
            keyevent("enter")
        print(times)
        
    touch((0.385, 0.204))
    
    print('进入游戏成功！')


def SL(big=True): # TODO:进行SL,大的杀掉游戏进程,小的断网重连
    if big:
        stop_app(r"com.huanmeng.zhanjian2")
        check_and_login()
    else:
        pass


def select_formation(form_id): # TODO:从6种阵形种选一个
    pass


def single_battle(): # TODO:单场战斗
    pass





