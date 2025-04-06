from model.xiuxian_user import *
from model.xiuxian_user_equipment import delete_user_equipments_by_user

from model.xiuxian_user_item import *

from model.xiuxian_item import *
from model.xiuxian_ling_gen import get_ling_gen_all,XiuxianLingGen

ling_gen:List[XiuxianLingGen] = get_ling_gen_all()
# for lg in ling_gen:
#     print(lg)
# user = get_user(user_qq="1321909220")
# print(user.user_exp)

# 添加用户 
# new_user = add_user({
#     'user_id': '123456',
#     'user_qq': '123456',
#     'user_name': '张三',
#     'user_exp': 0 
# })

# 给用户添加装备
# user_equipment= add_user_equipment({
#     'user_id':"123456",
#     'item_id':"1"
# })

# print(user_equipment)
# 查询用户装备列表
# user_equipment:List[XiuxianUserEquipment]= get_user_equipment(user_id='123456')
# for usereq in user_equipment:
#     if usereq.item_id==1:
#         update_equipment_by_id(
#             id=usereq.id,
#             equipment_data={'durability': -1}
#       )
#     print(usereq.id,usereq.user_id,usereq.item_id)


# delete_user_equipments_by_user(user_id=123456,item_id=2)

# 更新用户装备 
# update_equipment = update_equipment_by_id(
#     id=1,
#     equipment_data={'durability': 10}
# )
# 更新用户 
# updated_user = update_user(
#     user_id=1907848081419886594,
#     update_data={'user_exp': 10000}
# )

# # 查询用户 
# user = get_user_by_id(1907848081419886594) 
# print(user.user_name,  user.user_exp) 
 
# 删除用户 
# if delete_users(1907848081419886595): 
#     print("删除成功") 

# print( add_user_item({
#     "user_id":123456,
#     "item_id":1
# }))

# print(get_item_by_id(1))