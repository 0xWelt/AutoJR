# -*- encoding=utf8 -*-
__author__ = "Nickydusk"

""" 将图片template直接提前编译好，后续直接调用 """

from airtest.core.api import Template

def init_template():
    TEM = {
        "ui":{
            "雷电模拟器":{
                "允许":Template(r"pictures/ui/雷电模拟器/允许.png", record_pos=(0.151, 0.001), resolution=(1280, 720))
            },
            "登录":{
                "进入游戏":Template(r"pictures/ui/登录/进入游戏.png", record_pos=(0.385, 0.206), resolution=(1280, 720)),
                "确认":Template(r"pictures/ui/登录/确认.png", record_pos=(-0.12, 0.037), resolution=(1280, 720)),
                "接受":Template(r"pictures/ui/登录/接受.png", record_pos=(-0.102, 0.17), resolution=(1280, 720)),
                "用户名":Template(r"pictures/ui/登录/用户名.png", record_pos=(-0.196, -0.079), resolution=(1280, 720)),
            },
            "主页":{
                "杂项":Template(r"pictures/ui/主页/杂项.png", record_pos=(-0.449, 0.222), resolution=(1280, 720)),
                "建造开发完成":Template(r"pictures/ui/主页/建造开发完成.png", record_pos=(-0.364, 0.24), resolution=(1280, 720)),
                "新邮件":Template(r"pictures/ui/主页/新邮件.png", record_pos=(-0.285, 0.243), resolution=(1280, 720)),
                "邮件_全部收取":Template(r"pictures/ui/主页/邮件_全部收取.png", record_pos=(0.401, 0.245), resolution=(1280, 720)),
                "邮件_返回":Template(r"pictures/ui/主页/邮件_返回.png", record_pos=(-0.467, -0.248), resolution=(1280, 720)),

                "出征":Template(r"pictures/ui/主页/出征.png", record_pos=(0.463, 0.247), resolution=(1280, 720)),
                "出征_红点":Template(r"pictures/ui/主页/出征_红点.png", record_pos=(0.462, 0.205), resolution=(1280, 720)),
                "船坞":Template(r"pictures/ui/主页/船坞.png", record_pos=(0.321, 0.249), resolution=(1280, 720)),
                "任务":Template(r"pictures/ui/主页/任务.png", record_pos=(0.206, 0.248), resolution=(1280, 720)),
                "任务_红点":Template(r"pictures/ui/主页/任务_红点.png", record_pos=(0.197, 0.21), resolution=(1280, 720)),
                
                "活动通知_今日不再显示":Template(r"pictures/ui/主页/活动通知_今日不再显示.png", record_pos=(-0.434, 0.233), resolution=(1280, 720)),
                "活动通知_返回":Template(r"pictures/ui/主页/活动通知_返回.png", record_pos=(-0.468, -0.248), resolution=(1280, 720)),
                "每日奖励_领取":Template(r"pictures/ui/主页/每日奖励_领取.png", record_pos=(0.0, 0.097), resolution=(1280, 720)),
                "每日奖励_确认":Template(r"pictures/ui/主页/每日奖励_确认.png", record_pos=(-0.001, 0.038), resolution=(1280, 720))
            },
            "杂项":{
                "建造":{
                    "建造_开发":{
                        # "开始":
                        # "完成":
                    },
                    "建造":{
                    },
                    "解装":{
                    },
                    "废弃":{
                    },
                    "开发":{
                    },
                }
            },
            "任务":{
                "领取奖励":Template(r"pictures/ui/任务/领取奖励.png", record_pos=(0.374, -0.079), resolution=(1280, 720)),
                "确认":Template(r"pictures/ui/任务/确认.png", record_pos=(0.004, 0.037), resolution=(1280, 720)),
                "返回":Template(r"pictures/ui/出征/返回.png", record_pos=(-0.463, -0.251), resolution=(1280, 720)), # 复用出征
            },
            "船坞":{
                "返回":Template(r"pictures/ui/出征/返回.png", record_pos=(-0.463, -0.251), resolution=(1280, 720)), # 复用出征
            },
            "出征":{
                "返回":Template(r"pictures/ui/出征/返回.png", record_pos=(-0.463, -0.251), resolution=(1280, 720)),
                "演习_未选中":Template(r"pictures/ui/出征/演习_未选中.png", record_pos=(-0.188, -0.257), resolution=(1280, 720)),
                "演习_选中":Template(r"pictures/ui/出征/演习_选中.png", record_pos=(-0.189, -0.256), resolution=(1280, 720)),
                "出征":{

                },
                "演习":{

                },
                "远征":{
                    "领取奖励":Template(r"pictures/ui/出征/远征/领取奖励.png", record_pos=(0.402, -0.017), resolution=(1280, 720)),
                    "确认":Template(r"pictures/ui/出征/远征/确认.png", record_pos=(-0.116, 0.074), resolution=(1280, 720)),
                },
                "战役":{

                },
                "决战":{

                },
            },
        },
        "舰娘":{

        }
    }
    return TEM