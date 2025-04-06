"""种族"""
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
#  种族表
class XiuxianRace(Base):
    __table__ = Table(
        'xiuxian_race', 
        Base.metadata,   
        autoload_with=engine,
        autoload_replace=False,
        extend_existing=True  # 新增：允许表定义扩展 
    )
    
    # 新增：方便调试的repr 
    def __repr__(self):
        return f"<XiuxianLingGen(id={self.race_id},  name={self.race_name})>" 

from typing import Optional, Union 
from sqlalchemy import select 

# 获取种族详情
def get_race_by_id(
    race_id: Optional[int] = None,
) -> Optional[XiuxianRace]:
    try:
        with get_session() as session:
            # 构建查询条件 
            stmt = select(XiuxianRace)
            if race_id is not None:
                stmt = stmt.where(XiuxianRace.race_id  == race_id) 
            # 获取第一条结果 
            return session.scalars(stmt.limit(1)).first() 
            
    except SQLAlchemyError as e:
        logger.error(f"查询种族失败: 条件(race_id={race_id} 错误: {e}")
        return None
   
    # 获取所有种族
def get_race_all():
    try:
        with get_session() as session:
            stmt = select(XiuxianRace)
            return session.scalars(stmt).all() 
            
    except SQLAlchemyError as e:
        logger.error(f"查询道具失败 错误: {e}")
        return None