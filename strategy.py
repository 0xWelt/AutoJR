# -*- encoding=utf8 -*-
__author__ = "Nickydusk"
from control import GameController
import time

''' 体现人类智慧的策略，分为出击策略、运维策略，策略抽象成类 '''



class Task():
    r""" 任务抽象，定时唤醒执行指定功能 """
    
    def __init__(self, GC:GameController, priority, wake_time, job) -> None:
        self.GC = GC                # 游戏控制器
        self.priority = priority    # 优先级，数字越小越优先，同一时刻检测到多个符合唤醒条件的任务，执行最优先的
        self.wake_time = wake_time  # 唤醒时间，但钱时间>=唤醒时间则为唤醒状态
        self.job = job              # 执行的动作
        self.status = "等待执行"
        
    
    def do(self):
        self.job(self.GC)

        
class Strategy():
    r''' 策略对象，维护以“定时任务”为基础的控制流程 '''
    def __init__(self, config_json_path) -> None:
        self.GC = GameController(config_json_path)
        self.task_list = []
    
    def main_loop(self):
        pass

    def add_task(self,priority, wake_time, job):
        self.task_list.append(Task(self.GC,priority, wake_time, job))
        
    
    

    