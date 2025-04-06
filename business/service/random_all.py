from typing import Optional, Dict, Any, List, Union 
import random 
from model.xiuxian_ling_gen  import (get_ling_gen_all, XiuxianLingGen) 
from model.xiuxian_item  import (get_item_all, XiuxianItem) 
from model.xiuxian_race  import (get_race_all, XiuxianRace) 
from model.xiuxian_region  import (get_region_all, XiuxianRegion) 
from model.xiuxian_body  import (get_body_all, XiuxianBody) 
from model.xiuxian_realm  import (get_realm_all, XiuxianRealm) 
from model.xiuxian_effect  import (get_effect_all, XiuxianEffect) 
from model.xiuxian_events  import (get_events_all, XiuxianEvents) 
import schedule 
import time 
import threading 
 
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
 
# 生成随机名字 
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
 
# 预加载并转换为字典 
data_dicts = { 
    'ling_gen': {ling_gen.ling_gen_id:  ling_gen for ling_gen in get_ling_gen_all()}, 
    'item': {item.item_id:  item for item in get_item_all()}, 
    'region': {region.region_id:  region for region in get_region_all()}, 
    'body': {body.body_id:  body for body in get_body_all()}, 
    'race': {race.race_id:  race for race in get_race_all()}, 
    'realm': {realm.realm_id:  realm for realm in get_realm_all()}, 
    'effect': {effect.effect_id:  effect for effect in get_effect_all()}, 
    'events': {event.event_id:  event for event in get_events_all()} 
} 
 
def refresh_data(): 
    global data_dicts 
    with data_lock: 
        data_dicts = { 
            'ling_gen': {ling_gen.ling_gen_id:  ling_gen for ling_gen in get_ling_gen_all()}, 
            'item': {item.item_id:  item for item in get_item_all()}, 
            'region': {region.region_id:  region for region in get_region_all()}, 
            'body': {body.body_id:  body for body in get_body_all()}, 
            'race': {race.race_id:  race for race in get_race_all()}, 
            'realm': {realm.realm_id:  realm for realm in get_realm_all()}, 
            'effect': {effect.effect_id:  effect for effect in get_effect_all()}, 
            'events': {event.event_id:  event for event in get_events_all()} 
        } 
    print("数据已更新") 
 
# 启动独立线程运行定时任务（避免阻塞主线程） 
def schedule_loop(): 
    while True: 
        schedule.run_pending()  
        time.sleep(60)   # 每分钟检查一次 
 
threading.Thread(target=schedule_loop, daemon=True).start() 
# 定时任务:每天4点更新内容 
schedule.every().day.at("04:00").do(refresh_data)  
 
# 获取随机数据 
def get_random_data(data_type: str): 
    with data_lock: 
        data_dict = data_dicts.get(data_type)  
        if data_dict: 
            return random.choice(list(data_dict.values()))  
    return None 
 
# 获取随机某品质数据 
def get_random_data_rarity(data_type: str, rarity): 
    with data_lock: 
        data_dict = data_dicts.get(data_type)  
        if data_dict: 
            rarity_list = [data for data in data_dict.values()  if hasattr(data, 'rarity') and data.rarity  == rarity] 
            if not rarity_list: 
                return get_random_data(data_type) 
            return random.choice(rarity_list)  
    return None 
 
# 根据 id 获取数据 
def get_data_by_id(data_type: str, id): 
    with data_lock: 
        data_dict = data_dicts.get(data_type)  
        if data_dict: 
            return data_dict.get(id)  
    return None 


# 获取随机灵根 
def get_random_ling_geng(): 
    return get_random_data('ling_gen') 
# 获取随机某品质灵根 
def get_random_ling_geng_rarity(rarity): 
    return get_random_data_rarity('ling_gen', rarity) 
# 获取灵根 
def get_ling_geng_by_id(id): 
    return get_data_by_id('ling_gen', id) 


 #获取随机道具
def get_random_item():
    return get_random_data('item')
#获取随机某品质道具
def get_random_item_rarity(rarity):
    return get_random_data_rarity('item', rarity)
# 获取道具
def get_item_by_id(id):
    return get_data_by_id('item', id)


#获取随机地区
def get_random_region():
    return get_random_data('region')
#获取随机某品质地区
def get_random_region_rarity(rarity):
    return get_random_data_rarity('region', rarity)
# 获取地区
def get_region_by_id(id):
    return get_data_by_id('region', id)


#获取随机体质
def get_random_body():
    return get_random_data('body')
#获取随机某品质体质
def get_random_body_rarity(rarity):
    return get_random_data_rarity('body', rarity)
# 获取体质
def get_body_by_id(id):
    return get_data_by_id('body', id)


#获取随机种族
def get_random_race():
    return get_random_data('race')
#获取随机某品质种族
def get_random_race_rarity(rarity):
    return get_random_data_rarity('race', rarity)
# 获取种族
def get_race_by_id(id):
    return get_data_by_id('race', id)


#获取随机境界
def get_random_realm():
    return get_random_data('realm')
#获取随机某品质境界
def get_random_realm_rarity(rarity):
    return get_random_data_rarity('realm', rarity)
# 获取境界
def get_realm_by_id(id):
    return get_data_by_id('realm', id)


#获取随机效果
def get_random_effect():
    return get_random_data('effect')
#获取随机某品质效果
def get_random_effect_rarity(rarity):
    return get_random_data_rarity('effect', rarity)
# 获取效果
def get_effect_by_id(id):
    return get_data_by_id('effect', id)


#获取随机事件
def get_random_events():
    return get_random_data('events')
#获取随机某品质事件
def get_random_events_rarity(rarity):
    return get_random_data_rarity('events', rarity)
# 获取事件
def get_event_by_id(id):
    return get_data_by_id('events', id)
