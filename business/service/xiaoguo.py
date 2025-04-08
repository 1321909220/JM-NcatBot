from model.xiuxian_effect import *
from model.xiuxian_user import *
from model.xiuxian_events import *
from model.xiuxian_user_equipment import *
from model.xiuxian_user_buff import *
import random 
from service.random_all import *
import copy
#获取用户(带创建)
def get_user_is_urll(
    *,
    qq: Optional[int] = None,
    name: Optional[str] = None):
    user = get_user(user_id=qq)
    if user ==None:
        # 随机名字
        if name == None:
            name = generate_random_name() 
        # 随机灵根
        ling_geng = get_random_ling_geng()
        # 随机体质
        body =  get_random_body()
        # 随机种族
        race = get_random_race()
        # 随机地区
        region = get_random_region()
        # 获取境界
        realm = get_realm_by_id(1)
        user:XiuxianUser = XiuxianUser(
            user_id=qq,
            user_qq=qq,
            user_name=name,
            user_race_id=race.race_id,
            user_realm_id=realm.realm_id,
            user_ling_gen_id=ling_geng.ling_gen_id,
            user_region_id=region.region_id,
            user_body_id=body.body_id,
        )
        new_user = get_xiuxian_user_basics(user)
        effectlist: List[int] = []
        effectlist+=[realm.effect_id,ling_geng.effect_id,body.effect_id,region.effect_id,race.effect_id]
        add_user(resultUserEffect(new_user,effectlist))
    return user

# 获取前置条件算法 
def get_preposition_algorithm(v): 
    """能够判断的计算有(4大于,5等于,6小于)""" 
    operators = { 
        4: lambda a, b: a > b, 
        5: lambda a, b: a == b, 
        6: lambda a, b: a < b 
    } 
    if v not in operators: 
        raise ValueError("无效的操作码") 
    return operators[v] 
 
 
# 获取结果效果算法 
def get_result_algorithm(v): 
    """能够直接计算的有(0加,1减,2乘,3除,5等于)""" 
    operators = { 
        0: lambda a, b: a + b, 
        1: lambda a, b: a - b, 
        2: lambda a, b: a * b, 
        3: lambda a, b: a / b, 
        5: lambda a, b: b 
    } 
    if v not in operators: 
        raise ValueError("无效的操作码") 
    return operators[v] 
 

attributes = ['user_hp', 'user_energy', 'user_life', 'user_mental','user_speed','user_justice','user_exp','user_exp_magnification','user_breakthrough','user_attack','user_critical_attack','user_critical_magnification','user_penetration_attack','user_penetration_magnification','user_defense','user_san'] 

# 前置效果判断 
def prepositionUserEffect(user: XiuxianUser, effectIds: List[int]) -> Union[XiuxianUser, bool]: 
    effectList = get_effect_by_ids(effectIds)
    for effect in effectList: 
        for attr in attributes: 
            algorithm_attr = f'{attr[5:]}_algorithm'  
            value = getattr(effect, algorithm_attr) 
            if value is not None: 
                operator = get_preposition_algorithm(value) 
                user_value = getattr(user, attr) 
                effect_value = getattr(effect, attr[5:])  
                if not operator(user_value, effect_value): 
                    return False 
    return True 

# 结果效果计算
def resultUserEffect(user: XiuxianUser, effectIds: List[int]) -> Union[XiuxianUser, bool]: 
    effectList = get_effect_by_ids(effectIds) 
    for effect in effectList: 
        for attr in attributes: 
            algorithm_attr = f'{attr[5:]}_algorithm'  
            value = getattr(effect, algorithm_attr) 
            if value is not None: 
                operator = get_result_algorithm(value) 
                user_value = getattr(user, attr) 
                effect_value = getattr(effect, attr[5:])  
                setattr(user, attr, operator(user_value, effect_value)) 
    return user  

# 获取用户先天属性
def userInnateEffect(user):
    effectlist: List[int] = []
    # 获取灵根
    ling_geng = get_ling_geng_by_id(user.user_ling_gen_id)
    # 获取体质
    body =  get_body_by_id(user.user_body_id)
    # 获取种族
    race = get_race_by_id(user.user_race_id)
    # 获取境界
    realm = get_realm_by_id(user.user_realm_id)
    effectlist+=[ling_geng.effect_id,body.effect_id,race.effect_id,realm.effect_id]
    return resultUserEffect(user,effectlist)

# 计算用户后天属性
def userTomorrowEffect(user):
    effectlist: List[int] = []
    # 获取地区
    region = get_region_by_id(user.user_region_id)
    effectlist+=region.effect_id
    # 获取用户装备
    equipmentList = get_user_equipment(user.user_id)
    for equipment in equipmentList:
        effectlist+=equipment.effect_id
    # 获取用户buff
    buffList = get_user_buff(user.user_id)
    for buff in buffList:
        effectlist+=buff.effect_id
    return resultUserEffect(user,effectlist)

#获取用户最终属性
def userEffect(user):
   userInnate = userInnateEffect(user)
   return userTomorrowEffect(userInnate)


