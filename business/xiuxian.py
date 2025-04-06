import random 

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
