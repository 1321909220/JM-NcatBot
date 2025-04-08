"""用户装备"""
from typing import Optional, Dict, Any, List, Union 
from sqlalchemy import Table, select, update, delete 
from sqlalchemy.orm  import declarative_base 
from sqlalchemy.exc  import SQLAlchemyError 
from mysql_config import get_session, engine 
import logging 
from typing import Optional, Union 
from sqlalchemy import select 

 
# 配置日志 
logging.basicConfig() 
logger = logging.getLogger(__name__) 
logger.setLevel(logging.INFO) 
 
Base = declarative_base()
#  用户装备 
class XiuxianUserEquipment(Base):
    __table__ = Table(
        'xiuxian_user_equipment', 
        Base.metadata,   
        autoload_with=engine,
        autoload_replace=False,
        extend_existing=True  # 新增：允许表定义扩展 
    )
    
    # 方便调试的repr 
    def __repr__(self):
        return f"<XiuxianUserEquipment(id={self.user_id},  name={self.item_id})>" 

# 获取用户装备列表
def get_user_equipment(user_id: Optional[int] = None
) -> Optional[XiuxianUserEquipment]:
    try:
        with get_session() as session:
            # 构建查询条件 
            stmt = select(XiuxianUserEquipment)
            
            if user_id is not None:
                stmt = stmt.where(XiuxianUserEquipment.user_id  == user_id)
            return session.scalars(stmt).all() 
            
    except SQLAlchemyError as e:
        logger.error(f" 查询用户失败: 条件(user_id={user_id}, 错误: {e}")
        return None
    
# 给某个用户添加某个装备 (支持批量)
def add_user_equipment(userEquipment_data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Union[XiuxianUserEquipment, List[XiuxianUserEquipment]]:
    try:
        with get_session() as session:
            if isinstance(userEquipment_data, dict):
                userEquipment = XiuxianUserEquipment(**userEquipment_data)
                session.add(userEquipment) 
            else:
                userEquipments = [XiuxianUserEquipment(**data) for data in userEquipment_data]
                session.add_all(userEquipments) 
            
            session.commit() 
            
            if isinstance(userEquipment_data, dict):
                session.refresh(userEquipment) 
                return userEquipment 
            else:
                # 批量添加时不逐个refresh，性能考虑 
                return userEquipments 
    except SQLAlchemyError as e:
        logger.error(f" 添加失败: {e}")
        raise  # 根据业务需求决定是否重新抛出 
 
# 更新用户某件装备道具id
def update_equipment_by_user_on_item(
    user_id: int,
    item_id: int, 
    equipment_data: Dict[str, Any],
    use_merge: bool = False 
) -> Optional[XiuxianUserEquipment]:
    try:
        with get_session() as session:
            if use_merge:
                # 使用merge方式 (适合复杂对象)
                user = XiuxianUserEquipment(user_id=user_id,item_id=item_id,**equipment_data)
                equipment = session.merge(user) 
                session.commit() 
                return equipment 
            else:
                # 直接UPDATE语句 (更高效)
                stmt = (
                    update(XiuxianUserEquipment)
                    .where(XiuxianUserEquipment.user_id  == user_id)
                    .where(XiuxianUserEquipment.item_id==item_id)
                    .values(**equipment_data)
                    .execution_options(synchronize_session="fetch")
                )
                result = session.execute(stmt) 
                session.commit() 
            
                if result.rowcount  > 0:
                    return session.get(XiuxianUserEquipment,  user_id)
                return None 
    except SQLAlchemyError as e:
        logger.error(f" 更新失败: {e}")
        return None 
    
# 更新用户某件装备道具id
def update_equipment_by_id(
    id: int, 
    equipment_data: Dict[str, Any],
    use_merge: bool = False 
) -> Optional[XiuxianUserEquipment]:
    try:
        with get_session() as session:
            if use_merge:
                # 使用merge方式 (适合复杂对象)
                user = XiuxianUserEquipment(id=id,**equipment_data)
                equipment = session.merge(user) 
                session.commit() 
                return equipment 
            else:
                # 直接UPDATE语句 (更高效)
                stmt = (
                    update(XiuxianUserEquipment)
                    .where(XiuxianUserEquipment.id  == id)
                    .values(**equipment_data)
                    .execution_options(synchronize_session="fetch")
                )
                result = session.execute(stmt) 
                session.commit() 
            
                if result.rowcount  > 0:
                    return session.get(XiuxianUserEquipment,id)
                return None 
    except SQLAlchemyError as e:
        logger.error(f" 更新失败: {e}")
        return None 
 
# 删除用户装备记录
def delete_user_equipments(ids: Union[int, List[int]]) -> int:
    try:
        with get_session() as session:
            if isinstance(ids, int):
                ids = [ids]
                
            stmt = delete(XiuxianUserEquipment).where(XiuxianUserEquipment.id.in_(ids)) 
            result = session.execute(stmt) 
            session.commit() 
            return result.rowcount  
    except SQLAlchemyError as e:
        logger.error(f" 删除用户失败: {e}")
        return 0 
    
# 删除用户某个装备记录
def delete_user_equipments_by_user(user_id,item_id)->int:
    try:
        with get_session() as session:
            stmt = delete(XiuxianUserEquipment).where(XiuxianUserEquipment.user_id==user_id).where(XiuxianUserEquipment.item_id==item_id) 
            result = session.execute(stmt) 
            session.commit() 
            return result.rowcount  
    except SQLAlchemyError as e:
        logger.error(f" 删除用户失败: {e}")
        return 0 