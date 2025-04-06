"""道具"""
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
#  道具表
class XiuxianItem(Base):
    __table__ = Table(
        'xiuxian_item', 
        Base.metadata,   
        autoload_with=engine,
        autoload_replace=False,
        extend_existing=True  # 新增：允许表定义扩展 
    )
    
    # 新增：方便调试的repr 
    def __repr__(self):
        return f"<XiuxianItem(id={self.item_id},  name={self.item_name})>" 

from typing import Optional, Union 
from sqlalchemy import select 

# 获取道具详情
def get_item_by_id(
    item_id: Optional[int] = None,
) -> Optional[XiuxianItem]:
    try:
        with get_session() as session:
            # 构建查询条件 
            stmt = select(XiuxianItem)
            if item_id is not None:
                stmt = stmt.where(XiuxianItem.item_id  == item_id) 
            # 获取第一条结果 
            return session.scalars(stmt.limit(1)).first() 
            
    except SQLAlchemyError as e:
        logger.error(f" 查询道具失败: 条件(user_id={item_id} 错误: {e}")
        return None
    
    # 获取所有道具
def get_item_all():
    try:
        with get_session() as session:
            stmt = select(XiuxianItem)
            return session.scalars(stmt).all() 
            
    except SQLAlchemyError as e:
        logger.error(f"查询道具失败 错误: {e}")
        return None
