# -*- encoding=utf8 -*-
__author__ = "Nickydusk"

from airtest.core.api import start_app,stop_app,text,keyevent,auto_setup
from utility import exists, touch
from template import *
from CONSTS import *


class GameController():
    r""" 游戏控制器类，实现所有所需的 原子、组合 控制方法。 """
    
    def __init__(self) -> None:
        r"""
        Args:
            config_json_path: 存放用户配置文件的目录

        """
        auto_setup(__file__,devices=['android://?cap_method=JAVACAP&&ori_method=MINICAPORI&&touch_method=MINITOUCH"'])


        # 进行模组初始化
        self.fs = FormSelector(default="SL")
        
        # 加载游戏状态，并复位到游戏主页
        self.reset_state()
        self.back_to_home()

        print("GC 初始化成功！应当位于主界面")

    def reset_state(self): # TODO:更多情况
        r""" 检测当前所处状态并设置self.state  注意！！非常耗时！！ """
        
        if exists(UI['主页']['杂项'],threshold=0.85):
            self.state = "主页"
        elif exists(UI['返回'],threshold=0.95):
            self.state = "可返回"
        elif exists(UI['登录']["进入游戏"]):
            self.state = "登录"
        elif exists(UI['主页']['活动通知_今日不再显示']):
            self.state = "活动通知"
        else:
            self.state = "未知"

    def login(self,first_time=False):
        r''' 登录游戏，如果发现账号未登录则先登录，账号密码放在config.json中 '''
        # 启动游戏
        start_app(r"com.huanmeng.zhanjian2")

        self.state = "登录"
        if first_time or touch(UI['登录']["进入游戏"], timeout=20) == False:
            while True:
                print('未发现“进入游戏”按钮，尝试可能情况中...')
                if loc := exists(UI['登录']["进入游戏"]):
                    touch(loc)
                    break
                if loc := exists(UI['登录']['确认']):
                    print('检测到：下载资源！')
                    touch(loc)
                    continue
                if loc := exists(UI['雷电模拟器']['允许']):
                    print('检测到：模拟器权限允许！')
                    touch(loc)
                    continue
                if loc := exists(UI['登录']['接受']):
                    print('检测到：接受条款！')
                    touch(loc)
                    continue
                if loc := exists(UI['登录']['用户名']):
                    print('检测到：账号登陆！')
                    touch(loc)
                    text(CFG['username'])
                    text(CFG['passwd'])
                    keyevent("enter")
                    continue
                # case 5: 未能成功启动游戏
                start_app(r"com.huanmeng.zhanjian2")


        if exists(UI['主页']['杂项'],threshold=0.85,timeout=10):
            if touch(UI['主页']['每日奖励_领取'],timeout=0.5):
                touch(UI['主页']['每日奖励_确认'],timeout=0.5)
            self.state = "主页"
            print('进入游戏成功！')
        else:
            print("[ERROR] 登陆失败！")
            self.SL()

    def SL(self,big=True):
        r""" 进行SL,大的杀掉游戏进程,小的点击撤退 """
        if big:
            stop_app(r"com.huanmeng.zhanjian2")
            self.state = "设备主页"
            self.login()

    def back_to_home(self):    # TODO:更多情况
        r""" 回到游戏主界面 """
        
        print(f"{self.state} -> 主页")

        if self.state == "主页":
            if touch(UI['主页']['每日奖励_领取'],timeout=0.5):
                touch(UI['主页']['每日奖励_确认'],timeout=0.5)
        elif self.state == "可返回":
            touch(UI['返回'])
            self.state = "主页"
        elif self.state == "登录":
            touch(UI['登录']["进入游戏"])
            self.state = "主页"
        elif self.state == "活动通知":
            touch(UI['主页']['活动通知_今日不再显示'])
            touch(UI['返回'])
            touch(UI['主页']['每日奖励_领取'])
            touch(UI['主页']['每日奖励_确认'])
            self.state = "主页"
        else:
            self.SL()


    def select_form(self): # TODO:更多分支
        form = self.fs.select()
        if form=='SL':
            self.SL()
        

    # def conqure(self, map, fleet, repair):
    #     r'''TODO：一次完整常规出征流程，包含 [选图(check)，换阵(check)，按需快修，按照策略进行数场战斗]

    #     Args:
    #             map: 需要出征的地图，两整数表示。如[6,1]代表 6-1万能练级图。
    #             fleet: 选取的舰队，1-6
    #             repair: 维修模式(用快修)，从['No','Big','Medium','Any']中选择一个

    #     '''
    #     pass


class FormSelector():
    r""" 阵容选择器，需要实现 """
    def __init__(self, default, strategy=None) -> None:
        r"""
        Args:
            default: 规则不存在或匹配失败时采用的阵形，必须指定
            strategy: {"A":{"enemy":form,...}}，第一级字典表示图中的节点（字母），第二维是个字典，按照敌人的类型匹配阵形
            
        """
        self.default = default
        self.strategy = strategy
        self.node = "A"    # 出门点

    def set_strategy(self, strategy):
        self.strategy = strategy

    def detact_enemy(self):
        r"""检测敌人类型，用字符串表示(直接判定当前界面)
        """
        pass

    def select(self):
        enemy_type = self.detact_enemy()
        if self.node in self.strategy.keys() and enemy_type in self.strategy[self.node].keys():
            return self.strategy[self.node]
        else:
            return self.default

