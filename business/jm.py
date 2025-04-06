import re

def strict_match(search_list, target):
    """字符串是否在列表内严格精确匹配函数"""
    return target in set(search_list)

def is_at(bot_id, message):  
    """检测是否被艾特"""  
    target_id = str(bot_id)
    for msg in message:  
        if (  
            msg.get("type")  == "at"  
            and isinstance(msg.get("data"),  dict)  
            and str(msg["data"].get("qq", "")) == target_id  
        ):  
            return True  
    return False  

def getText(message):
    """获取消息文本"""
    for msg in message:
        if msg.get("type")  == "text":  # 匹配类型 
            return msg.get("data",  {}).get("text", "")# 安全获取值  
   
def get_instructions(text):
    """获取消息指令和内容"""
    text = text.strip()  if text else ""  # 空值转为空字符串
    match = re.match(r"^\/(\S+)(?:\s+(.*))?$",  text.strip()) 
    if match:
        command = f"/{match.group(1)}"   # 完整命令（含斜杠）
        args =f"{match.group(2)}" # 参数（无则为空）
        return (command,args)
    return("","")

def extract_command(text):  
    """从文本中提取斜杠命令（如`/音乐`）"""  
    command, _ = get_instructions(text)  
    return command  
 
def extract_args(text):  
    """从文本中提取命令参数（如`10086`）"""  
    _, args = get_instructions(text)  
    return args  


