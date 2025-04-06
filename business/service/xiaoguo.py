from model.xiuxian_effect import *
from model.xiuxian_user import *
from model.xiuxian_events import *
import random 
from random_all import *

#获取用户(带创建)
def get_user_is_urll(qq,name):
    user = get_user(user_id=qq)
    if user ==None:
        # 随机名字
        if name == None:
            name = generate_random_name 
        # 随机灵根
        ling_geng = get_random_ling_geng
        # 随机体质
        body =  get_random_body
        # 随机种族
        race = get_random_race
        # 随机地区
        region = get_random_region
        add_user({
        'user_id': qq,
        'user_qq': qq,
        'user_name': name,
        })

        user = get_user(user_id=qq)
    return user
 
def effect (user:XiuxianUser,effect:List[XiuxianEffect]):
    # 用户效果计算
    # 用户=> 循环效果=>判断效果分类=>效果叠加
    # !!!!
    return 


talent = [1,2,3,4,5]
slife = [100,90,85,95]

# 主角属性
class Person:
    def __init__(self,na,tal,Life):
        self.name = na
        self.talent = tal
        self.lingqi = 0.0
        self.lingshi = 0.0
        self.life = Life
    def xiulian(self):
            self.lingqi += 0.08*(1+random.choice(talent)/100)*self.talent

# 判断境界和寿命减少方式
def iff(s):
    if s.lingqi>=0 and s.lingqi<20:
        return "\n境界:练气"
    elif s.lingqi>=20 and s.lingqi<40:
        s.life += 0.9*s.talent/5
        return "\n境界:筑基"
    elif s.lingqi>=40 and s.lingqi<60:
        s.life += 0.6*s.talent/5
        return "\n境界:结丹"
    elif s.lingqi>=60 and s.lingqi<80:
        s.life += 0.3*s.talent/5
        return "\n境界:元婴"
    elif s.lingqi>=80 and s.lingqi<100:
        s.life += 0.1*s.talent/5
        return "\n境界:化神"
    elif s.lingqi>=100 and s.lingqi<150:
        s.life += 0.05*s.talent/5
        return "\n境界:炼虚"
    elif s.lingqi>=150 and s.lingqi<200:
        s.life += 0.01*s.talent/5
        return "\n境界:合体"
    elif s.lingqi>=200 and s.lingqi<250:
        return "\n境界:大乘"
    elif s.lingqi>=250:
        return "\n境界:渡劫"
    return

# 发生的事件 
def sth_happened(s, a, b, c): 
    if random.choice(a)  == 0: 
        return random.choice(b)  
    else: 
        aa = random.choice(c)  
        for index, event in enumerate(c): 
            if event == aa: 
                if index == 0: 
                    s.talent  += 1 
                elif index == 1: 
                    s.lingqi  += 10 
                elif index == 2: 
                    s.lingshi  += 1 
                elif index == 3: 
                    s.life  += 10 
                elif index == 4: 
                    s.life  -= 8 
                elif index == 5: 
                    s.life  -= 5 
                elif index == 6: 
                    s.lingqi  += 0.5 
                elif index == 7: 
                    s.lingqi  += random.choice([-1,  1, 10, 20]) 
                elif index == 8: 
                    s.lingqi  += 5 
                elif index == 9: 
                    s.lingshi  += 5 
                    s.lingqi  += 20 
                    return("你在神秘遗迹中发现了大量灵石和灵气，修为大幅提升！") 
                elif index == 10: 
                    s.talent  -= 1 
                    s.lingqi  -= 15 
                    return("你误食了毒草，天赋受损，修为倒退！") 
                elif index == 11: 
                    s.life  += 20 
                    s.lingqi  += 15 
                    return("你遇到了一位神秘老者，他传授你一套养生功法，寿命和修为都有所增加！") 
                elif index == 12: 
                    s.lingshi  -= 3 
                    return("你在集市上与人发生冲突，被抢走了 3 块灵石！") 
                elif index == 13: 
                    s.lingqi  += 30 
                    return("你在山洞中闭关修炼，突破了瓶颈，修为大增！") 
                elif index == 14: 
                    s.life  -= 15 
                    return("你遭遇了一场恶战，身受重伤，寿命减少！") 
                break 
        return aa 
 
# 事件库 
get = [0, 1] 
actually_get0 = [ 
    '这一年无事发生...', 
    '你感觉自己修为又上涨了一分', 
    '你萌生了下山的想法', 
    '师父收了个师妹，你想认识一下', 
    '你觉得很无聊，于是开始学习python',
    '你觉得很无聊，于是开始学习java', 
    '你做了个梦，梦见自己飞升了', 
    '快乐逐渐减少...' 
] 
actually_get1 = [ 
    '你获得了一本绝世功法', 
    '师父见你修炼过慢，给了你一枚灵气丹', 
    '走在路上，捡到了一枚下品灵石，你很高兴', 
    '师父感觉你会老死，给了你一枚寿元丹', 
    '你向师姐表白失败，道心受挫，寿命减少了', 
    '你向师妹表露心迹，师妹以你太丑拒绝了你', 
    '你走在路上捡到了一枚壮阳丹', 
    '你走在路上捡到了一枚神秘的丹药', 
    '听说山下妖魔作祟，师父让你下山除妖，你的修为进一步提升', 
    '你在神秘遗迹中发现了大量灵石和灵气，修为大幅提升！', 
    '你误食了毒草，天赋受损，修为倒退！', 
    '你遇到了一位神秘老者，他传授你一套养生功法，寿命和修为都有所增加！', 
    '你在集市上与人发生冲突，被抢走了 3 块灵石！', 
    '你在山洞中闭关修炼，突破了瓶颈，修为大增！', 
    '你遭遇了一场恶战，身受重伤，寿命减少！' 
] 
 
def xiuxian(name):
    # INIT	
    s = Person(name,random.choice(talent),random.choice(slife))
    text = ''  # 初始化 text 变量 
    # 主程序循环
    nian=10
    for i in range(300):
        text+=f"\n{nian}岁"
        text+='\n-----------'    
        s.xiulian()
        text+=f"\n姓名:{s.name}"
        text+=iff(s)
        text+=f"\n寿命:{round(s.life,2)}"
        s.life -= 1
        nian += 1
        text+=f"\n灵气值:{round(s.lingqi,2)}"
        text+=("\n"+sth_happened(s,get,actually_get0,actually_get1))
        text+='\n-----------'
        if s.lingqi>=300:
            text+=('\n修行之路，与天争寿，功成圆满，飞升而去...')
            return text
        if s.life<=0:
            text+=('\n修行之路，与天争寿，奈何时也命也，你寿终而亡...')
            return text
        text+="\n新的一年..."
        text+='\n-----------'
