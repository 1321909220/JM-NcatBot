"""用户"""
from typing import Optional, Dict, Any, List, Union 
from sqlalchemy import Table, select, update, delete 
from sqlalchemy.orm  import declarative_base 
from sqlalchemy.exc  import SQLAlchemyError 
from mysql_config import get_session, engine 
import logging 
# 配置日志 
logging.basicConfig() 
logger = logging.getLogger(__name__) 
logger.setLevel(logging.INFO) 
 
Base = declarative_base()
#  用户表
class XiuxianUser(Base):
    __table__ = Table(
        'xiuxian_user', 
        Base.metadata,   
        autoload_with=engine,
        autoload_replace=False,
        extend_existing=True  # 新增：允许表定义扩展 
    )
    
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
 
# 添加用户 (支持批量)
def add_user(user_data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Union[XiuxianUser, List[XiuxianUser]]:
    try:
        with get_session() as session:
            if isinstance(user_data, dict):
                user = XiuxianUser(**user_data)
                session.add(user) 
            else:
                users = [XiuxianUser(**data) for data in user_data]
                session.add_all(users) 
            
            session.commit() 
            
            if isinstance(user_data, dict):
                session.refresh(user) 
                return user 
            else:
                # 批量添加时不逐个refresh，性能考虑 
                return users 
    except SQLAlchemyError as e:
        logger.error(f" 添加用户失败: {e}")
        raise  # 根据业务需求决定是否重新抛出 
 
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
