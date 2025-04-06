"""随机与数据汇总"""
from typing import Optional, Dict, Any, List, Union
import random 
from model.xiuxian_ling_gen import (get_ling_gen_all,XiuxianLingGen) 
from model.xiuxian_item import(get_item_all,XiuxianItem)
from model.xiuxian_race import(get_race_all,XiuxianRace)
from model.xiuxian_region import(get_region_all,XiuxianRegion)
from model.xiuxian_body import(get_body_all,XiuxianBody)
from model.xiuxian_realm import(get_realm_all,XiuxianRealm)
from model.xiuxian_effect import(get_effect_all,XiuxianEffect)
from model.xiuxian_events import(get_events_all,XiuxianEvents)
import schedule 
from datetime import time 

surnames = [ 
    "凌", "洛", "墨", "萧", "楚", "苏", "白", "夜", "凤", "龙", 
    "轩辕", "慕容", "欧阳", "上官", "端木", "东方", "南宫", "北冥", 
    "司徒", "司马", "独孤", "赫连", "百里", "公孙", "令狐", "钟离" 
] 
# 适合组成单字名和双字名的元素 
single_given_names = [ 
    "风", "云", "雷", "电", "雨", "雪", "霜", "雾", "虹", "霞", 
    "山", "水", "林", "木", "石", "泉", "溪", "湖", "海", "沙", 
    "灵", "幻", "玄", "幽", "冥", "仙", "神", "魔", "妖", "鬼", 
    "诀", "咒", "符", "印", "法", "术", "丹", "器", "阵", "劫", 
    "清", "净", "虚", "无", "空", "明", "悟", "觉", "善", "仁", 
    "义", "礼", "智", "信", "忠", "孝", "勇", "毅", "诚", "谦", 
    "羽", "尘", "影", "月", "星", "辰", "耀", "辉", "光", "芒", 
    "逸", "轩", "宇", "泽", "渊", "澜", "涛", "峰", "岭", "巅" 
] 
# 专门用于组成双字名的搭配字 
double_given_names_complements = [ 
    "天", "地", "玄", "黄", "宇", "宙", "洪", "荒", "苍", "穹", 
    "灵", "幻", "仙", "圣", "神", "魔", "妖", "鬼", "冥", "幽", 
    "清", "净", "虚", "无", "空", "明", "悟", "觉", "善", "仁" 
] 
#生成随机名字
def generate_random_name(): 
    surname = random.choice(surnames)  
    # 有 30% 的概率生成双字名 
    if random.random()  < 0.3: 
        first_char = random.choice(single_given_names)  
        second_char = random.choice(double_given_names_complements)  
        given_name = first_char + second_char 
    else: 
        given_name = random.choice(single_given_names)  
    full_name = surname + given_name 
    return full_name

# 全局读写锁  
data_lock = threading.RLock() 
#预加载
ling_gen_list:List[XiuxianLingGen] = get_ling_gen_all()#灵根list
item_list:List[XiuxianItem] = get_item_all()#道具list
region_list:List[XiuxianRegion] = get_region_all()#地区list
body_list:List[XiuxianBody] = get_body_all()#体质list
race_list:List[XiuxianRace] = get_race_all()#种族list
realm_list:List[XiuxianRealm] = get_realm_all()#境界list
effect_list:List[XiuxianEffect] = get_effect_all()#效果list
events_list:List[XiuxianEvents] = get_events_all()#事件list

def refresh_data():  
    global ling_gen_list,item_list,region_list,body_list,race_list,realm_list,effect_list,events_list
    with data_lock:
        ling_gen_list= get_ling_gen_all()
        item_list = get_item_all()
        region_list= get_region_all()
        body_list= get_body_all()
        race_list= get_race_all()
        realm_list= get_realm_all()
        effect_list= get_effect_all()
        events_list= get_events_all()
  
# 启动独立线程运行定时任务（避免阻塞主线程）  
import threading  
def schedule_loop():  
    while True:  
        schedule.run_pending()   
        time.sleep(60)   # 每分钟检查一次

threading.Thread(target=schedule_loop, daemon=True).start()
# 定时任务:每天4点更新内容
schedule.every().day.at("04:00").do(refresh_data) 


#获取随机灵根
def get_random_ling_geng():
    with data_lock:
        return random.choice(ling_gen_list)
#获取随机某品质灵根
def get_random_ling_geng_rarity(rarity):
    rarity_list = [gen_list for gen_list in ling_gen_list if gen_list.rarity  == rarity]
    if not rarity_list:
        get_random_ling_geng()
    with data_lock:
        return random.choice(rarity_list)

#获取随机体质
def get_random_body():
    with data_lock:
        return random.choice(body_list)
#获取随机某品质体质
def get_random_ling_geng_rarity(rarity):
    rarity_list = [body for body in body_list if body.rarity  == rarity]
    if not rarity_list:
        get_random_body()
    with data_lock:
        return random.choice(rarity_list)

#获取随机种族
def get_random_race():
    with data_lock:
        return random.choice(race_list)
#获取随机某品质种族
def get_random_ling_geng_rarity(rarity):
    rarity_list = [race for race in race_list if race.rarity  == rarity]
    if not rarity_list:
        get_random_race()
    with data_lock:
        return random.choice(rarity_list)

#获取随机地区
def get_random_region():
    with data_lock:
        return random.choice(region_list)
#获取随机某品质地区
def get_random_ling_geng_rarity(rarity):
    rarity_list = [regiont for regiont in region_list if regiont.rarity  == rarity]
    if not rarity_list:
        get_random_region()
    with data_lock:
        return random.choice(rarity_list)

#获取随机道具
def get_random_item():
    with data_lock:
        return random.choice(item_list)
#获取随机某品质道具
def get_random_ling_geng_rarity(rarity):
    rarity_list = [item for item in item_list if item.rarity  == rarity]
    if not rarity_list:
        get_random_item()
    with data_lock:
        return random.choice(rarity_list)

#获取随机事件
def get_random_item():
    with data_lock:
        return random.choice(events_list)
#获取随机某品质事件
def get_random_ling_geng_rarity(rarity):
    rarity_list = [events for events in events_list if events.rarity  == rarity]
    if not rarity_list:
        get_random_item()
    with data_lock:
        return random.choice(rarity_list)

#获取随机效果
def get_random_item():
    with data_lock:
        return random.choice(effect_list)
#获取随机某品质效果
def get_random_ling_geng_rarity(rarity):
    rarity_list = [effect for effect in effect_list if effect.rarity  == rarity]
    if not rarity_list:
        get_random_item()
    with data_lock:    
        return random.choice(rarity_list)

