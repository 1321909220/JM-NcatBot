"""事件"""
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
#  事件表
class XiuxianEvents(Base):
    __table__ = Table(
        'xiuxian_events', 
        Base.metadata,   
        autoload_with=engine,
        autoload_replace=False,
        extend_existing=True  # 新增：允许表定义扩展 
    )
    # 新增：方便调试的repr 
    def __repr__(self):
        return f"<XiuxianEvents(id={self.events_id},  name={self.events_name})>" 

from typing import Optional, Union 
from sqlalchemy import select 

# 获取事件详情
def get_events_by_id(
    events_id: Optional[int] = None,
) -> Optional[XiuxianEvents]:
    try:
        with get_session() as session:
            # 构建查询条件 
            stmt = select(XiuxianEvents)
            if events_id is not None:
                stmt = stmt.where(XiuxianEvents.events_id  == events_id) 
            # 获取第一条结果 
            return session.scalars(stmt.limit(1)).first()             
    except SQLAlchemyError as e:
        logger.error(f" 查询事件失败: 条件(events_id={events_id} 错误: {e}")
        return None
    
    # 获取所事件
def get_events_all():
    try:
        with get_session() as session:
            stmt = select(XiuxianEvents)
            return session.scalars(stmt).all() 
            
    except SQLAlchemyError as e:
        logger.error(f"查询事件失败 错误: {e}")
        return None
