'''
Author: 萌新王
Date: 2023-08-09 15:20:38
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2023-08-12 13:58:24
FilePath: \OneDrive\tools\qqBot\plugins\testbot_wt\__init__.py
Email: 763103245@qq.com
'''
# 测试回复机器人
import requests
import time
import random
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Event, Message
from .bot import AutoChatBots
from nonebot import on_message, on_command, get_driver
from .config import Config
from nonebot.exception import FinishedException

# 延迟时间
randTime = [1.0, 1.0]

global_config = get_driver().config
config = Config.parse_obj(global_config)

#
# # # 事件响应器会对 /天气 开头的消息进行响应。
# # weather = on_command("天气")

# from nonebot.rule import to_me
# # 在被私聊或者at时，响应"天气"，"weather", "查天气"，优先级10阻断其他响应
# # weather = on_command("天气", rule=to_me(), aliases={"weather", "查天气"}, priority=10, block=True)
# weather = on_command("天气", aliases={"weather", "查天气"}, priority=10, block=True)
# # 响应天气类消息时
# @weather.handle()
# async def handle_function():
#     # pass  # do something here
#     # await weather.send("天气是...")
#     await weather.finish("天气是...")


talk = on_message(priority=50)

# 运行时相关变更参数
args = {
    # 开始时间
    "startTime": 0.0,
}
# _overTime = time.time()


async def bc(text):
    """回复消息回调
    :param text: 回复文本
    """
    print("准备开始回复")
    # 当前时间
    currentTime = time.time()
    # 接收到信息时
    startTime = args["startTime"]
    # 经过时间
    elapsedTime = currentTime - startTime
    # # 储存当前时间
    # args["startTime"] = currentTime
    # 固定延迟时间
    randTime1 = randTime[1]
    # 回复信息长度
    strLen = len(text)
    # 延迟时间倍率
    timeMultiplying = 1.0
    # 回复信息长度过长，超过10个字符串
    if strLen > 10:
        # 计算长度，每10个长度增加一倍
        timeMultiplying = strLen/10
        # 超过4倍，设置为4倍
        if timeMultiplying > 4:
            timeMultiplying = 4
    # 延迟时间。随机时间（0-1）+长度倍率*1.0-已经经过的时间
    delay = (random.random()*randTime[0]) + \
        (randTime1*timeMultiplying) - elapsedTime
    print(delay)
    # 如果还需要延迟
    if delay > 0:
        time.sleep(delay)
    print("开始回复")
    await talk.finish(Message(text))
# testAi
testAi = AutoChatBots(bc)

# 切换test回复机器人
switchAi = on_command("切换", aliases={"switch"}, priority=10, block=True)
seeAi = on_command("查看", aliases={}, priority=10, block=True)
xAi = on_command("屑", aliases={}, priority=10, block=True)


@xAi.handle()
async def kk():
    print("屑")
    text = Message(requests.get(
        url='https://api.lovelive.tools/api/SweetNothings').text)   # type: str
    time.sleep(random.random()*randTime[0] + randTime[1])
    if text and type(text) is str and not text.startswith("<"):
        await talk.finish(Message(text))
    raise FinishedException


@seeAi.handle()
async def _():
    print(testAi.see())
    await kk()
    pass


@switchAi.handle()
async def handle_function():
    text = testAi.switch()
    print("当前聊天机器人被切换：", text)
    time.sleep(random.random()*randTime[0] + randTime[1])
    await kk()
    # await switchAi.finish(text)

# @talk.type_updater
# async def _() -> str:
#     return "notice"


@talk.handle()
async def _(event: Event):
    args["startTime"] = time.time()
    text = str(event.message)
    await testAi.run(text)
    # await talk.finish(text)
    # await talk.skip()
    pass
