# import os
import time
import random
# import pyttsx3
import requests
from nonebot.exception import FinishedException
from . import chatglm

class AutoChatBots():
    def __init__(self, bc):
        self.supported_bots = {
            # 无法使用
            # '海知智能机器人': self.ruyi,
            # 需要用户id
            # '图灵机器人': self.turing,

            '天行机器人': self.tian,
            '思知机器人': self.ownthink,
            '青云客智能聊天机器人': self.qingyunke,
        }
        # # test 添加chatglm
        # _bot = chatglm.bot()
        # self.supported_bots['ChatGlm'] = _bot.run
        # self.bot_name = 'ChatGlm'

        # 默认随机获取一个机器人
        self.bot_name = random.choice(list(self.supported_bots.keys()))
        
        self.bc = bc
        # 是否开始，防止多次输入
        self.isStart = False
    async def run(self, topic):
        '''运行'''
        if not self.isStart:
            self.isStart = True
            bot_name = self.bot_name
            bot = self.supported_bots[bot_name]
            try:
                topic = bot(topic)
                print(f'[{bot_name}]: {topic}')
                if topic:
                    await self.bc(topic)
                self.isStart = False
            finally:
                self.isStart = False
                raise FinishedException
        raise FinishedException

    def ownthink(self, sentence, need_say=True):
        '''思知机器人API'''
        # 在https://www.ownthink.com/可以申请app_keys
        app_keys = [
            'xiaosi',
            '9ffcb5785ad9617bf4e64178ac64f7b1',
            '3f9ae1c73db460f4bbb2b491c9119eec',
            'c4b2d5f87542b70e2f65f9dec5288913',
        ]
        while True:
            url = 'https://api.ownthink.com/bot'
            app_key = random.choice(app_keys)
            params = {
                'appid': app_key,
                'userid': random.randrange(1, 9999),
                'spoken': sentence
            }
            response = requests.get(url, params=params)
            if response.json()['message'] != 'success':
                time.sleep(random.random() + 0.5)
                continue
            reply = response.json()['data']['info']['text']
            # if need_say: self.say(reply)
            return reply
    '''海知智能机器人API'''
    # def ruyi(self, sentence, need_say=True):
    #     # 在https://ruyi.ai/可以申请app_keys
    #     app_keys = [
    #         'bfdeb392-0e9e-452f-8eec-09a1de2e58d0',
    #         '0df50fac-4df0-466c-9798-99136f42bb8c',
    #         '9aa281dd-ec2e-407d-85c8-ad0a0abd0824',
    #         '631e72e1-6867-49b9-af92-36d4c4c154de',
    #     ]
    #     while True:
    #         url = 'http://api.ruyi.ai/v1/message'
    #         headers = {'Content-Type': 'application/json'}
    #         app_key = random.choice(app_keys)
    #         params = {'q': sentence, 'user_id': random.randrange(1, 9999), 'app_key': app_key}
    #         response = requests.get(url, headers=headers, params=params)
    #         if response.json()['msg'] != 'ok':
    #             time.sleep(random.random() + 0.5)
    #             continue
    #         reply = response.json()['result']['intents'][0]['result']['text']
    #         if need_say: self.say(reply)
    #         return reply

    def tian(self, sentence, need_say=True):
        '''天行机器人API'''
        # 在https://www.tianapi.com/apiview/47可以申请app_keys
        app_keys = [
            (random.randrange(1, 9999), '16e2471e7a72f1e9dca46b2a80486c7d'),
            (random.randrange(1, 9999), '5fb41161aff1256441d57dafeef854fc'),
            (random.randrange(1, 9999), '6c80a34954420f65176ec34f1261967e'),
            (random.randrange(1, 9999), '8461142e844b269785d25242986696c5'),
        ]
        while True:
            url = 'https://api.tianapi.com/txapi/robot/'
            userid, key = random.choice(app_keys)
            params = {
                'key': key,
                'question': sentence,
                'userid': userid,
                'limit': '10',
                'mode': '1',
                'datatype': '0',
            }
            response = requests.get(url, params=params)
            if response.json()['msg'] != 'success':
                time.sleep(random.random() + 0.5)
                continue
            reply = response.json()['newslist'][0]['reply']
            # if need_say: self.say(reply)
            return reply
    def qingyunke(self, sentence, need_say=True):
        '''青云客智能聊天机器人API'''
        while True:
            url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg=%s'
            response = requests.get(url % sentence)
            if response.json()['result'] != 0:
                time.sleep(random.random() + 0.5)
                continue
            reply = response.json()['content']
            # if need_say: self.say(reply)
            return reply
    
    # def turing(self, sentence, need_say=True):
    #     '''图灵机器人API'''
    #     # 在http://www.tuling123.com/可以申请appkeys
    #     appkeys = [
    #         'f0a5ab746c7d41c48a733cabff23fb6d',
    #         'c4fae3a2f8394b73bcffdecbbb4c6ac6',
    #         '0ca694db371745668c28c6cb0a755587',
    #         '7855ce1ebd654f31938505bb990616d4',
    #         '5945954988d24ed393f465aae9be71b9',
    #         '1a337b641da04c64aa7fd4849a5f713e',
    #         'eb720a8970964f3f855d863d24406576',
    #         '1107d5601866433dba9599fac1bc0083',
    #         '70a315f07d324b3ea02cf21d13796605',
    #         '45fa933f47bb45fb8e7746759ba9b24a',
    #         '2f1446eb0321804291b0a1e217c25bb5',
    #         '7f05e31d381143d9948109e75484d9d0',
    #         '35ff2856b55e4a7f9eeb86e3437e23fe',
    #         '820c4a6ca4694063ab6002be1d1c63d3',
    #     ]
    #     while True:
    #         url = 'http://www.tuling123.com/openapi/api?key=%s&info=%suserid=12345678'
    #         response = requests.get(url % (random.choice(appkeys), sentence))

    #         reply = response.json()['text']
    #         if u'亲爱的，当天请求次数已用完。' in reply:
    #             continue
    #         if need_say: self.say(reply)
    #         return reply
    # def filter(self, sentence):
    #     '''过滤非中文内容'''
    #     sentence_clean = ''
    #     for c in sentence:
    #         if '\u4e00' <= c <= '\u9fa5': sentence_clean += c
    #     return sentence_clean
    # def say(self, content):
    #     '''说话'''
    #     if random.random() > 0.5:
    #         os.system('mshta vbscript:createobject("sapi.spvoice").speak("%s")(window.close)' % content)
    #     else:
    #         pyttsx3.speak(content)
    # def chatGlm(self, content):
    #     return chatglm.run(text=content)
    # 切换
    def switch(self, key=None):
        aiList = self.supported_bots  # type: list
        if len(aiList) > 1:
            aiDict = dict(aiList)
            del aiDict[self.bot_name]
            if not key in aiDict:
                key = random.choice(list(aiDict.keys()))
            self.bot_name = key
            return key
        # 判空
        else:
            return aiList.keys()[0] if aiList else ""

    def see(self):
        """
        查看当前bot名称
        """
        return self.bot_name
