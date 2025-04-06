from ncatbot.core.element import (
    MessageChain,  # 消息链，用于组合多个消息元素
    Text,          # 文本消息
    Reply,         # 回复消息
    At,            # @某人
    AtAll,         # @全体成员
    Dice,          # 骰子
    Face,          # QQ表情
    Image,         # 图片
    Json,          # JSON消息
    Music,         # 音乐分享 (网易云, QQ 音乐等)
    CustomMusic,   # 自定义音乐分享
    Record,        # 语音
    Rps,           # 猜拳
    Video,         # 视频
    File,          # 文件
)
# 快捷消息创建
def msg_text(text):
    return MessageChain([
            Text(text)
        ])
    
# 快捷消息创建末尾加表情
def msg_text_face(text,face):
     return MessageChain([
            Text(text),
            Face(face)
        ])
# 艾特并且回复
def msg_at_text(at,text):
    return MessageChain([
            At(at),
            Text(text),
        ])

# 艾特并且回复加表情
def msg_at_text_face(at,text,face):
    return MessageChain([
            At(at),
            Text(text),
            Face(face)
        ])
# 发送文件 
def msg_file(path):
    return MessageChain([
            File(path)
        ])
#标准任务收到提醒
def  receivedTask():
    return msg_text("任务收到!正在努力取件中>_<")
#随机任务收到提醒
def  randomsReceivedTask():
    return msg_text_face("正在输入随机取件码,会是什么呢",178)
#任务结束提醒
def endTask(userId):
    return msg_at_text_face(userId,"你好！你的快递已经送达",178)
#只是at
def atI():
    return msg_text_face("你好！\n艾特我+/jm+本子id \n如:@qq /jm 112863 \n我就可以为你转换为pdf文件了",178)

