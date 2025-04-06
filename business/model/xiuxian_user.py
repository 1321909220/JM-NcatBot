"""用户"""
from typing import Optional, Dict, Any, List, Union 
from sqlalchemy import Table, select, update, delete 
from sqlalchemy.orm  import declarative_base 
from sqlalchemy.exc  import SQLAlchemyError 
from mysql_config import get_session, engine 
import logging 
from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, Numeric, Table 
# 配置日志 
logging.basicConfig() 
logger = logging.getLogger(__name__) 
logger.setLevel(logging.INFO) 
 
Base = declarative_base()
#  用户表
@dataclass
class XiuxianUser(Base):
    __table__ = Table(
        'xiuxian_user', 
        Base.metadata,
        autoload_with=engine,
        autoload_replace=False,
        extend_existing=True  # 新增：允许表定义扩展 
    )  
    user_hp: int = 100                    # 生命值（HP）  
    user_energy: int = 100                # 法力值（MP）  
    user_life: int = 80                   # 寿命值（剩余寿元）  
    user_mental: int = 100                # 念力值（神识强度）  
    user_speed: int = 100                 # 速度值（行动优先级）
    user_justice: int = 0                 # 正义值（正邪倾向）
    user_exp: int = 0                     # 修为值（境界经验）  
    user_breakthrough: int = 1            # 突破几率（百分比）
    user_attack: int = 10                 # 基础攻击力  
    user_critical_attack: int = 5         # 暴击率（单位：‰，实际值需/1000）  
    user_critical_magnification: int = 2  # 暴击倍率（200%）  
    user_penetration_attack: int = 5      # 穿透率（无视防御概率，单位：‰）  
    user_penetration_magnification: int =1# 穿透伤害比例（100%）  
    user_defense: int = 1                 # 防御值（减伤系数） 
    user_san: int = 100                   # 道心值（SAN值，防止入魔）  
    
    # 新增：方便调试的repr 
    def __repr__(self):
        return f"<XiuxianUser(id={self.user_id},  name={self.user_name})>" 

from typing import Optional, Union 
from sqlalchemy import select 

# 获取用户
def get_user(
    *,
    user_id: Optional[int] = None,
    user_qq: Optional[str] = None 
) -> Optional[XiuxianUser]:
    if not any([user_id, user_qq]):
        raise ValueError("至少需要提供一个查询条件（user_id或user_qq）")
    try:
        with get_session() as session:
            # 构建查询条件 
            stmt = select(XiuxianUser)
            
            if user_id is not None:
                stmt = stmt.where(XiuxianUser.user_id  == user_id)
                
            if user_qq is not None:
                stmt = stmt.where(XiuxianUser.user_qq  == user_qq)
                
            # 获取第一条结果 
            return session.scalars(stmt.limit(1)).first() 
            
    except SQLAlchemyError as e:
        logger.error(f" 查询用户失败: 条件(user_id={user_id}, user_qq={user_qq}), 错误: {e}")
        return None
 
# 批量获取用户 
def get_users_by_ids(user_ids: List[int]) -> List[XiuxianUser]:
    try:
        with get_session() as session:
            stmt = select(XiuxianUser).where(XiuxianUser.user_id.in_(user_ids)) 
            return list(session.scalars(stmt)) 
    except SQLAlchemyError as e:
        logger.error(f" 批量获取用户失败: {e}")
        return []
 
def add_user(user_data: Union[XiuxianUser, List[XiuxianUser]]):
    with get_session() as session:
        # 修改类型判断逻辑 
        if isinstance(user_data, XiuxianUser):  # 直接处理对象 
            session.add(user_data) 
        elif isinstance(user_data, list):
            session.add_all(user_data) 
        else:
            raise TypeError("仅支持XiuxianUser对象或对象列表")
 
        session.commit() 
        session.refresh(user_data)  if isinstance(user_data, XiuxianUser) else None 
        return user_data 
 
# 更新用户 (支持直接SQL更新)
def update_user(
    user_id: int, 
    update_data: Dict[str, Any],
    use_merge: bool = False 
) -> Optional[XiuxianUser]:
    try:
        with get_session() as session:
            if use_merge:
                # 使用merge方式 (适合复杂对象)
                user = XiuxianUser(user_id=user_id, **update_data)
                merged_user = session.merge(user) 
                session.commit() 
                return merged_user 
            else:
                # 直接UPDATE语句 (更高效)
                stmt = (
                    update(XiuxianUser)
                    .where(XiuxianUser.user_id  == user_id)
                    .values(**update_data)
                    .execution_options(synchronize_session="fetch")
                )
                result = session.execute(stmt) 
                session.commit() 
                
                if result.rowcount  > 0:
                    return session.get(XiuxianUser,  user_id)
                return None 
    except SQLAlchemyError as e:
        logger.error(f" 更新用户失败: {e}")
        return None 
 
# 删除用户 (支持批量)
def delete_users(user_ids: Union[int, List[int]]) -> int:
    try:
        with get_session() as session:
            if isinstance(user_ids, int):
                user_ids = [user_ids]
                
            stmt = delete(XiuxianUser).where(XiuxianUser.user_id.in_(user_ids)) 
            result = session.execute(stmt) 
            session.commit() 
            return result.rowcount  
    except SQLAlchemyError as e:
        logger.error(f" 删除用户失败: {e}")
        return 0 
