# -*- encoding=utf8 -*-
__author__ = "Nickydusk"

from CONSTS import *
from control import GameController
import time
import datetime as dt
from task import *
from random import choice

''' 体现人类智慧的策略，分为出击策略、运维策略，策略抽象成类 '''


class Strategy():
    r''' 策略对象，维护以“定时任务”为基础的控制流程 '''
    def __init__(self) -> None:
        self.GC = GameController()
        self.task_list = []
        self.init_tasks()
    
    def add_task(self,task:Task, priority,wake_time):
        self.task_list.append(task(self.GC,priority,wake_time))

    def init_tasks(self):
        raise NotImplementedError
    
    def print_tasks(self):
        print()
        print("===== 现在时间:",dt.datetime.now(),"=====")
        for task in self.task_list:
            print(task.name,task.status,task.priority,task.wake_time)
        print()

    def main_loop(self):
        while True:
            self.print_tasks()

            todo_list = []
            hp = 100
            wait_time = None
            for task in self.task_list:
                # 选取当前最高优先级动作
                if task.wake_time <= dt.datetime.now():
                    if task.priority < hp:
                        todo_list = [task]
                        hp = task.priority
                    elif task.priority == hp:
                        todo_list.append(task)

            # 随机从最高优先级中挑一个做
            if todo_list:
                todo = choice(todo_list)
                todo.do()
                wait_time = todo.destructor()

            wait_time = 60 if wait_time is None else wait_time
            time.sleep(wait_time)


class tmpStrategy(Strategy):
    def __init__(self) -> None:
        super().__init__()

    def init_tasks(self):
        # 每天三点重启游戏，刷新每日任务
        tm = dt.datetime.now() + dt.timedelta(days=1)
        self.add_task(AutoRestartGame,0,dt.datetime(tm.year,tm.month,tm.day,3))

        # 每隔数小时重启模拟器，防止模拟器卡死
        self.add_task(AutoRestartSimulator,0,dt.datetime.now()+dt.timedelta(hours=6))

        # 被动型任务，检查是否完成并相关处理
        self.add_task(RepeatExpedition,0,dt.datetime.now())
        self.add_task(CheckMission,0,dt.datetime.now())
        self.add_task(CheckMail,0,dt.datetime.now())

        # 主动型任务


    
    

    