# -*- encoding=utf8 -*-
__author__ = "Nickydusk"

from airtest.core.api import start_app,stop_app,text,keyevent,sleep,auto_setup
from utility import exists, touch
from template import *
import json
from CONSTS import *


class GameController():
    r""" 游戏控制器类，实现所有所需的 原子、组合 控制方法。 """
    
    def __init__(self, config_json_path) -> None:
        r"""
        Args:
            config_json_path: 存放用户配置文件的目录

        """

        # 从配置文件加载
        with open(config_json_path,"r") as f:
            js = json.load(f)
        self.username = js['username']
        self.passwd = js['passwd']

        # 进行模组初始化
        self.fs = FormSelector(default="SL")
        self.TEM = init_template()
        self.UI = self.TEM['ui']
        
        # 加载游戏状态，并复位到游戏主页
        self.reset_state()
        self.back_to_home()

        print("GC 初始化成功！应当位于主界面")

    def reset_state(self): # TODO:更多情况
        r""" 检测当前所处状态并设置self.state  注意！！非常耗时！！ """
        if exists(self.UI['主页']['活动通知_今日不再显示']):
            self.state = "活动通知"
        elif exists(self.UI['主页']['每日奖励_领取']):
            self.state = "每日奖励"
        elif exists(self.UI['主页']['杂项'],threshold=0.85):
            self.state = "主页"
        elif exists(self.UI['出征']['演习_未选中'])!=False or exists(self.UI['出征']['演习_选中'])!=False:
            self.state = "出征"
        elif exists(self.UI['登录']["进入游戏"]):
            self.state = "登录"
        else:
            self.state = "未知"

    def login(self,first_time=False):
        r''' 登录游戏，如果发现账号未登录则先登录，账号密码放在config.json中 '''
        # 启动游戏
        start_app(r"com.huanmeng.zhanjian2")
        auto_setup(__file__,devices=['android://']) # FIXME:发现开启APP后再次setup，可以把横屏转换成竖屏，进而解决所有问题。后续需要解决如何横屏的问题
        self.state = "登录"
        if first_time or False==touch(self.UI['登录']["进入游戏"],timeout=20):
            while True:
                print('未发现“进入游戏”按钮，尝试可能情况中...')
                loc = exists(self.UI['登录']["进入游戏"])
                if loc:
                    touch(loc)
                    break
                # case 1: 需要下载
                loc = exists(self.UI['登录']['确认'])
                if loc:
                    print('检测到：下载资源！')
                    touch(loc)
                    continue
                # case 2: 需要确认模拟器权限
                loc = exists(self.UI['雷电模拟器']['允许'])
                if loc:
                    print('检测到：模拟器权限允许！')
                    touch(loc)
                    continue
                # case 3: 需要确认游戏条款
                loc = exists(self.UI['登录']['接受'])
                if loc:
                    print('检测到：接受条款！')
                    touch(loc)
                    continue
                # case 4: 需要登录
                loc = exists(self.UI['雷电模拟器']['允许'])
                if loc:
                    print('检测到：账号登陆！')
                    touch(loc)
                    text(self.username)
                    text(self.passwd)
                    keyevent("enter")
                    continue
                # case 5: 未能成功启动游戏
                start_app(r"com.huanmeng.zhanjian2")
                auto_setup(__file__,devices=['android://'])

        sleep(5)    # FIXME: 这5秒钟是必须等的吗？有没有更好的解决方法
        self.reset_state()
        if self.state in ['主页','活动通知','每日奖励']:
            self.back_to_home()
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
        else: # TODO: 点击游戏内的撤退
            pass

    def back_to_home(self): # TODO:更多情况
        r""" 回到游戏主界面 """
        
        print("%s -> 主页"%self.state)
        
        if self.state == "主页":
            return
        elif self.state in ['任务','船坞','出征']:
            touch(self.UI['出征']['返回'])
        elif self.state == "登录":
            touch(self.UI['登录']["进入游戏"])
        elif self.state == "活动通知":
            touch(self.UI['主页']['活动通知_今日不再显示'])
            touch(self.UI['主页']['活动通知_返回'])
            touch(self.UI['主页']['每日奖励_领取'])
            touch(self.UI['主页']['每日奖励_确认'])
        elif self.state == "每日奖励":
            touch(self.UI['主页']['每日奖励_领取'])
            touch(self.UI['主页']['每日奖励_确认'])
        else:
            self.SL()


    def select_form(self): # TODO:更多分支
        form = self.fs.select()
        if form=='SL':
            self.SL()
        


    def check_and_expedition(self):
        r""" 检测是否有结束的远征，有的话收取并重新派遣 """
        
        self.reset_state()
        # if self.state != "出征":
        self.back_to_home()

        loc = exists(self.UI['主页']['出征_红点'],threshold=0.9)
        if loc:
            print("发现远征！")
            touch(loc)
            self.state = "出征"
            while touch(self.UI['出征']['远征']['领取奖励'],timeout=2):
                touch(loc)      # 空白位置随便点一下，确认奖励
                touch(self.UI['出征']['远征']['确认'])
            touch(self.UI['出征']['返回'])
        else:
            print("远征-无")
        
        # 没出错就返回 0 ，有没有任务都 0
        return 0

    def check_missions(self):
        r""" 检查任务，有就领取 """
        
        self.reset_state()
        # if self.state != "任务":
        self.back_to_home()
        
        loc = exists(self.UI['主页']['任务_红点'],threshold=0.95)
        if loc:
            print("发现任务！")
            touch(loc)
            self.state = "任务"
            while touch(self.UI['任务']['领取奖励'],timeout=2):
                touch(self.UI['任务']['确认'])
            touch(self.UI['任务']['返回'])
        else:
            print("任务-无")
        
        return 0

    def check_mail(self):
        r""" 检查邮箱，主要是月卡奖励 """
        self.reset_state()
        # if self.state != "主页":
        self.back_to_home()
        
        loc = exists(self.UI['主页']['新邮件'],threshold=0.9)
        if loc:
            print("发现新邮件!")
            touch(loc)
            touch(self.UI['主页']['邮件_全部收取'])
            touch(self.UI['主页']['邮件_返回'])
        else:
            print("邮件-无")
        
        return 0



    def conqure(self, map, fleet, repair):
        r'''TODO：一次完整常规出征流程，包含 [选图(check)，换阵(check)，按需快修，按照策略进行数场战斗]

        Args:
                map: 需要出征的地图，两整数表示。如[6,1]代表 6-1万能练级图。
                fleet: 选取的舰队，1-6
                repair: 维修模式(用快修)，从['No','Big','Medium','Any']中选择一个

        '''
        pass


    

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

