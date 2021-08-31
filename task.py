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


''' 维护容错类 '''
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



''' 运营检查类 '''
class AutoMissionExpedition(Task):
    r""" 同时检查 任务/远征。需要提前设置好远征队，会始终重复出发 """
    
    def __init__(self,GC: GameController, priority, wake_time) -> None:
        super().__init__('收任务／远征',GC, priority, wake_time)
        self.did_something = False
    
    def do(self):
        self.GC.reset_state()
        self.GC.back_to_home()

        loc = exists(UI['主页']['红点'])
        if loc:
            touch(loc)
            self.did_something=True
            while touch(UI['任务']['领取奖励'],timeout=1,threshold=0.9):
                print("发现任务！")
                touch(UI['任务']['确认'])
            while touch(UI['出征']['远征']['收获奖励'],timeout=1,threshold=0.9):
                print("发现远征！")
                touch(UI['空'])      # 空白位置随便点一下，确认奖励
                touch(UI['出征']['远征']['确认'])
            
            touch(UI['返回'])
            self.status = "正常结束"
        else:
            print("任务／远征-无")
            self.status = "等待执行"
        
    def destructor(self):
        if self.status == "正常结束":
            self.wake_time = dt.datetime.now()
            self.status = "等待执行"
        else:
            self.wake_time = dt.datetime.now() + dt.timedelta(minutes=10)
        
        return 0

class CheckMail(Task):
    r""" 检查邮箱，主要是月卡奖励 """

    def __init__(self, GC: GameController, priority, wake_time) -> None:
        super().__init__('检查邮件',GC, priority, wake_time)
    
    def do(self):
        self.GC.reset_state()
        self.GC.back_to_home()
        
        loc = exists(UI['主页']['新邮件'],threshold=0.85)    # FIXME：定阈值没用了，得改图片
        if loc:
            print("发现新邮件!")
            touch(loc)
            touch(UI['主页']['邮件_全部收取'])
            touch(UI['返回'])
            self.status = "正常结束"
        else:
            print("邮件-无")
            self.status = "等待执行"

    def destructor(self):
        if self.status == "正常结束":
            self.status = "等待执行"
            tm = dt.datetime.now() + dt.timedelta(days=1)
            self.wake_time = dt.datetime(tm.year,tm.month,tm.day,0,5)     # 明天凌晨三点
        else:
            self.wake_time = dt.datetime.now() + dt.timedelta(hours=1)
        
        return 0

class CheckDev(Task):
    r""" 检查有无开发建造，有的话收一下 """
    def __init__(self, GC: GameController, priority, wake_time) -> None:
        super().__init__("收建造／开发", GC, priority, wake_time)
        
    def do(self):
        self.GC.reset_state()
        self.GC.back_to_home()
        
        loc = exists(UI['主页']['建造开发完成'])
        if loc:
            print("发现新建造开发!")
            touch(loc)
            touch(UI['杂项']['建造']['建造_开发']['完成'])
            touch(UI['空'])
            touch(UI['新_确认'],timeout=1)
            touch(UI['返回'])
            self.status = "正常结束"
        else:
            print("建造/开发-无")
            self.status = "等待执行"

        

    def destructor(self):
        if self.status == "正常结束":
            self.status = "等待执行"
            self.wake_time = dt.datetime.now()
        else:
            self.wake_time = dt.datetime.now() + dt.timedelta(minutes=60)
        
        return 0

''' 主动出击类 '''



