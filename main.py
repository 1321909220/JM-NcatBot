from ncatbot.core import BotClient, GroupMessage, PrivateMessage
from ncatbot.utils.config import config
from ncatbot.utils.logger import get_log
from business.keyWords import *
from business.xiuxian import *
from business.jm import (
    strict_match,
    is_at,
    getText,
    get_instructions  
                         )
from typing import Union
import jmcomic
import random
import os
import re
from business.message import *

from business.service.xiaoguo import get_user_is_urll

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

_log = get_log()

config.set_bot_uin("1321909220")  # 设置 bot qq 号 (必填)
config.set_root("")  # 设置 bot 超级管理员账号 (建议填写)
config.set_ws_uri("ws://localhost:3001")  # 设置 napcat websocket server 地址
config.set_token("")  # 设置 token (napcat 服务器的 token)

bot = BotClient()

config = "config.yml"
loadConfig = jmcomic.JmOption.from_file(config)
#如果需要下载，则取消以下注释
manhua = []

# # 消息处理逻辑 
@bot.group_event() 
@bot.private_event() 
async def on_at_message(msg: Union[GroupMessage, PrivateMessage]):
    _log.info(msg)
    # 清空 manhua
    manhua.clear()
    botId = "3219269174"  # 机器人id
    admin = ["1321909220","1"] #管理员
    userId = msg.user_id #用户id
    suerName = msg.sender.nickname #用户昵称
    message = msg.message #消息本体
    text = getText(message) #消息文本
    command,args= get_instructions(text)#command:命令和args:内容
    at = is_at(botId,message)#是否艾特我
    if at and strict_match(words_jm,command):
        print("艾特了我并且输入了",command,args)
        await msg.reply(rtf=receivedTask())
        manhua.append(args)
        # 下载该本子
        loadConfig.download_album(manhua)
        # 构造为pdf
        file_path = f"pdf/{args}.pdf"
        # 创建消息内容
        await msg.reply(rtf=msg_file(file_path))
        await msg.reply(rtf=endTask(userId))
    elif at and strict_match(words_randoms,command):
        print("艾特了我并且输入了",command,args)
        await msg.reply(rtf=randomsReceivedTask())
        album_id = random.randint(10,100000)
        manhua.append(album_id)
        # 下载该本子
        loadConfig.download_album(manhua)
        # 构造为pdf
        file_path = f"pdf/{album_id}.pdf"
        # 创建消息内容
        await msg.reply(rtf=msg_file(file_path))
        await msg.reply(rtf=endTask(userId))
    elif at and strict_match(words_randoms_caching,command):
        print("艾特了我并且输入了",command,args)
        await msg.reply(rtf=randomsReceivedTask())
        folder_path = "./pdf"
        all_files = [f for f in os.listdir(folder_path)  if os.path.isfile(os.path.join(folder_path,  f))]
        # 步骤2：随机获取单个文件名 
        album_id = random.choice(all_files)  
        id =album_id[:-4] if album_id.endswith('.pff')  else album_id 
        manhua.append(id)
        # 下载该本子
        loadConfig.download_album(manhua)
        # 构造为pdf
        file_path = f"pdf/{album_id}.pdf"
        # 创建消息内容
        await msg.reply(rtf=msg_file(file_path))
        await msg.reply(rtf=endTask(userId))
    elif at and strict_match(words_delt,command):
        print("艾特了我并且输入了",command,args)
        await msg.reply(rtf=msg_text("任务收到!正在消毒"))
        file_path = f"pdf/{args}.pdf"  # 替换为实际文件路径
        if os.path.exists(file_path):   # 安全验证[1]()
            try:
                os.remove(file_path) 
                msg_chain = MessageChain([
                        File(f"成功删除：{args}")
                ])
                await msg.reply(rtf=msg_chain) 
            except PermissionError:
                msg_chain = MessageChain([
                        File("权限不足，请联系管理员")
                    ])
                await msg.reply(rtf=msg_chain) 
            except Exception as e:
                msg_chain = MessageChain([
                        File("删除失败，请联系管理员")
                    ])
                await msg.reply(rtf=msg_chain) 
            else:
                msg_chain = MessageChain([
                        File("我这里没有缓存这个货物,请放心(´▽`ʃ♡ƪ)")
                    ])
                await msg.reply(rtf=msg_chain) 
        else:
            msg_chain = MessageChain([
                        File("你当前没有删除文件的权力(⌐■_■)")
                    ])
            await msg.reply(rtf=msg_chain)   
    elif at and strict_match(words_xiuxian,command):
        print("修仙")
        get_user_is_urll(userId,command)
        await msg.reply(rtf=msg_text(xiuxian(suerName)))
    elif at and strict_match(words_xiuxian,command):
        print("修仙")
        await msg.reply(rtf=msg_text(xiuxian(suerName)))
    elif at:  
        await msg.reply(rtf=atI())

if __name__ == "__main__":
    bot.run(reload=False)

