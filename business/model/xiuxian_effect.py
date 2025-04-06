"""效果"""
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
#  效果表
class XiuxianEffect(Base):
    __table__ = Table(
        'xiuxian_effect', 
        Base.metadata,   
        autoload_with=engine,
        autoload_replace=False,
        extend_existing=True  # 新增：允许表定义扩展 
    )
    
    # 新增：方便调试的repr 
    def __repr__(self):
        return f"<XiuxianEffect(id={self.effect_id},  name={self.effect_name})>" 

from typing import Optional, Union 
from sqlalchemy import select 

# 获取效果详情
def get_effect_by_id(
    effect_id: Optional[int] = None,
) -> Optional[XiuxianEffect]:
    try:
        with get_session() as session:
            # 构建查询条件 
            stmt = select(XiuxianEffect)
            if effect_id is not None:
                stmt = stmt.where(XiuxianEffect.effect_id  == effect_id) 
            # 获取第一条结果 
            return session.scalars(stmt.limit(1)).first() 
            
    except SQLAlchemyError as e:
        logger.error(f" 查询道具失败: 条件(user_id={effect_id} 错误: {e}")
        return None

   # 获取所效果
def get_effect_all():
    try:
        with get_session() as session:
            stmt = select(XiuxianEffect)
            return session.scalars(stmt).all() 
            
    except SQLAlchemyError as e:
        logger.error(f"查询效果失败 错误: {e}")
        return None
