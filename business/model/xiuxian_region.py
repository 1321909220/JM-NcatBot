"""地区"""
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
#  地区表
class XiuxianRegion(Base):
    __table__ = Table(
        'xiuxian_region', 
        Base.metadata,   
        autoload_with=engine,
        autoload_replace=False,
        extend_existing=True  # 新增：允许表定义扩展 
    )
    
    # 新增：方便调试的repr 
    def __repr__(self):
        return f"<XiuxianRegion(id={self.region_id},  name={self.region_name})>" 

from typing import Optional, Union 
from sqlalchemy import select 

# 获取地区详情
def get_region_by_id(
    region_id: Optional[int] = None,
) -> Optional[XiuxianRegion]:
    try:
        with get_session() as session:
            # 构建查询条件 
            stmt = select(XiuxianRegion)
            if region_id is not None:
                stmt = stmt.where(XiuxianRegion.region_id  == region_id) 
            # 获取第一条结果 
            return session.scalars(stmt.limit(1)).first() 
            
    except SQLAlchemyError as e:
        logger.error(f" 查询地区失败: 条件(region_id={region_id} 错误: {e}")
        return None
   # 获取所有地区
def get_region_all():
    try:
        with get_session() as session:
            stmt = select(XiuxianRegion)
            return session.scalars(stmt).all() 
            
    except SQLAlchemyError as e:
        logger.error(f"查询地区失败 错误: {e}")
        return None