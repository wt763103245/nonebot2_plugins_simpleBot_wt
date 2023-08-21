'''
Date: 2023-08-11 22:43:15
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2023-08-12 19:51:31
FilePath: \OneDrive\tools\qqBot\plugins\testbot_wt\chatglm.py
Author: 萌新王
Qq: 763103245
Email: 763103245@qq.com
'''
import requests
from nonebot.exception import FinishedException


class bot():
    def __init__(self):

        # 历史记录
        self.history = [
            # [
            #     """你是一只会说话的猫猫，可以自由回答问题，像人类一样思考和表达。现在你与我对话时每一句话后面都要加上喵，并加上用表情。回复不要超过30个字符，不要换行""",
            #     """好的主人喵~🥰""",
            # ],
        ]
        # 最大长度
        # Maximum length 参数
        # 通常用于限制输入序列的最大长度，因为 ChatGLM-6B 是2048长度推理的，
        # 一般这个保持默认就行，太大可能会导致性能下降
        self.max_length = 2048
        # 精度
        # Top P 参数是指在生成文本等任务中，选择可能性最高的前P个词的概率累加和。
        # 这个参数被称为Top P，也称为Nucleus Sampling。
        # 例如，如果将Top P参数设置为0.7，那么模型会选择可能性排名超过70%的词进行采样。
        # 这样可以保证生成的文本准确性较高，但可能会缺乏多样性。相反，
        # 如果将Top P参数设置为0.3，则会选择可能性超过30%的词进行采样，
        # 这可能会导致生成文本的准确性下降，但能够更好地增加多样性。
        self.top_p = 0.7
        # Temperature参数通常用于调整softmax函数的输出，
        # 用于增加或减少模型对不同类别的置信度。
        # 具体来说，softmax函数将模型对每个类别的预测转换为概率分布。
        # Temperature参数可以看作是一个缩放因子，
        # 它可以增加或减少softmax函数输出中每个类别的置信度。
        # 比如将 Temperature 设置为 0.05 和 0.95 的主要区别在于，
        # T=0.05 会使得模型更加自信，更加倾向于选择概率最大的类别作为输出，
        # 而 T=0.95 会使得模型更加不确定，更加倾向于输出多个类别的概率值较大。
        self.temperature = 0.05

    def run(self, text):  # type: (str) -> str
        """回复消息
        :param text: 回应信息
        :return: 回复消息
        """
        print("ChatGlm")
        # 图片跳出
        if "CQ:image" in text:
            print("图片跳出")
            return ""
        # 请求地址
        url = 'http://127.0.0.1:8000/'
        headers = {'Content-Type': 'application/json'}
        # 请求内容数据
        data = {
            'prompt': text,
            'history': self.history,
            'max_length': self.max_length,
            'top_p': self.top_p,
            'temperature': self.temperature,
        }
        # 移除未回复
        self.fail()
        response = requests.post(url, json=data, headers=headers)
        data = response.json()
        print("ChatGLM2-6B:", data)
        # 成功回复
        if data and 'status' in data and data['status'] == 200:
            self.history = data["history"]
            # 遗忘记忆
            self.forget()
            return data["response"]
        else:
            raise FinishedException

    def forget(self, saveLen=160, minLen=1):
        """遗忘
        :param saveLen: 默认只记160条
        :param minLen: 默认保留前3条
        """
        _list = self.history
        _listLen = len(_list)
        if _listLen > saveLen:
            for i in (minLen, minLen+_listLen-saveLen):
                del self.history[minLen]

    def fail(self):
        """没有说话，则从这次记忆中消失
        """
        _list = self.history
        for i in range(len(_list)-1, -1, -1):
            # 没说话
            if not _list[i][1]:
                del self.history[i]
