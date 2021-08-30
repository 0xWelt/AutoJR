# -*- encoding=utf8 -*-
__author__ = "Nickydusk"

from CONSTS import *
from template import *
from control import GameController
from utility import touch,exists
from time import sleep
import datetime as dt
import os


class Task():
    r""" 任务抽象，定时唤醒执行指定功能 """
    
    def __init__(self, name, GC:GameController, priority, wake_time) -> None:
        self.name = name
        self.status = "等待执行"
        self.GC = GC                # 游戏控制器
        self.priority = priority    # 优先级，数字越小越优先，同一时刻检测到多个符合唤醒条件的任务，执行最优先的
        self.wake_time = wake_time  # 唤醒时间，但钱时间>=唤醒时间则为唤醒状态
        
        
    def do(self):
        raise NotImplementedError
    
    def destructor() -> int:
        r""" 返回，执行完这个任务之后需要等待的时间 """
        raise NotImplementedError


class RepeatExpedition(Task):
    r""" 预先设定好远征内容与编队并出发，此task会定期检查并继续用原始队伍远征 """
    
    def __init__(self,GC: GameController, priority, wake_time) -> None:
        super().__init__('自动远征',GC, priority, wake_time)
    
    def do(self):
        self.GC.reset_state()
        self.GC.back_to_home()

        loc = exists(UI['主页']['出征_红点'],threshold=0.9)
        if loc:
            print("发现远征！")
            touch(loc)
            while touch(UI['出征']['远征']['领取奖励'],timeout=2):
                touch(loc)      # 空白位置随便点一下，确认奖励
                touch(UI['出征']['远征']['确认'])
            touch(UI['返回'])
        else:
            print("远征-无")
        
        self.status = "正常结束"

    def destructor(self):
        # 不销毁，重复执行，每 半小时 检查一次
        if self.status == "正常结束":
            self.status = "等待执行"
            self.wake_time = dt.datetime.now() + dt.timedelta(minutes=10)
        else:
            print("[ERROR] 远征-异常")
            quit()
        
        return 0

class CheckMission(Task):
    r""" 预先设定好远征内容与编队并出发，此task会定期检查并继续用原始队伍远征 """

    def __init__(self, GC: GameController, priority, wake_time) -> None:
        super().__init__('检查任务',GC, priority, wake_time)
    
    def do(self):
        r""" 检查任务，有就领取 """
        
        self.GC.reset_state()
        self.GC.back_to_home()
        
        loc = exists(UI['主页']['任务_红点'],threshold=0.95)
        if loc:
            print("发现任务！")
            touch(loc)
            self.state = "任务"
            while touch(UI['任务']['领取奖励'],timeout=2):
                touch(UI['任务']['确认'])
            touch(UI['返回'])
        else:
            print("任务-无")
        
        self.status = "正常结束"

    def destructor(self):
        # 不销毁，重复执行，每 半小时 检查一次
        if self.status == "正常结束":
            self.status = "等待执行"
            self.wake_time = dt.datetime.now() + dt.timedelta(minutes=60)
        else:
            print("[ERROR] 任务-异常")
            quit()
        
        return 0

class CheckMail(Task):
    def __init__(self, GC: GameController, priority, wake_time) -> None:
        super().__init__('检查邮件',GC, priority, wake_time)
    
    def do(self):
        r""" 检查邮箱，主要是月卡奖励 """

        self.GC.reset_state()
        self.GC.back_to_home()
        
        loc = exists(UI['主页']['新邮件'],threshold=0.9)
        if loc:
            print("发现新邮件!")
            touch(loc)
            touch(UI['主页']['邮件_全部收取'])
            touch(UI['返回'])
        else:
            print("邮件-无")

        self.status = "正常结束"

    def destructor(self):
        # 不销毁，重复执行，每 半小时 检查一次
        if self.status == "正常结束":
            self.status = "等待执行"
            self.wake_time = dt.datetime.now() + dt.timedelta(minutes=120)
        else:
            print("[ERROR] 任务-异常")
            quit()
        
        return 0

class AutoRestartGame(Task):
    def __init__(self, GC: GameController, priority, wake_time) -> None:
        super().__init__('重启游戏',GC, priority, wake_time)

    def do(self):
        self.GC.SL()
        self.status = "正常结束"
    
    def destructor(self):
        if self.status == "正常结束":
            self.status = "等待执行"
            tm = dt.datetime.now() + dt.timedelta(days=1)
            self.wake_time = dt.datetime(tm.year,tm.month,tm.day,3)     # 明天凌晨三点
        
        return 0

class AutoRestartSimulator(Task):
    def __init__(self, GC: GameController, priority, wake_time) -> None:
        super().__init__('重启雷电',GC, priority, wake_time)

    def do(self):
        os.system('taskkill /F /IM dnplayer.exe')
        os.system('D:\leidian\LDPlayer4\dnplayer.exe')
        sleep(20)
        self.status = "正常结束"
    
    def destructor(self):
        if self.status == "正常结束":
            self.status = "等待执行"
            self.wake_time = dt.datetime.now() + dt.timedelta(hours=6)

        return 0