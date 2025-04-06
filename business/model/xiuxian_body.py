"""体质"""
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
#  体质表
class XiuxianBody(Base):
    __table__ = Table(
        'xiuxian_body', 
        Base.metadata,   
        autoload_with=engine,
        autoload_replace=False,
        extend_existing=True  # 新增：允许表定义扩展 
    )
    
    # 新增：方便调试的repr 
    def __repr__(self):
        return f"<XiuxianBody(id={self.body_id},  name={self.body_name})>" 

from typing import Optional, Union 
from sqlalchemy import select 

# 获取体质详情
def get_body_by_id(
    body_id: Optional[int] = None,
) -> Optional[XiuxianBody]:
    try:
        with get_session() as session:
            # 构建查询条件 
            stmt = select(XiuxianBody)
            if body_id is not None:
                stmt = stmt.where(XiuxianBody.body_id  == body_id) 
            # 获取第一条结果 
            return session.scalars(stmt.limit(1)).first() 
            
    except SQLAlchemyError as e:
        logger.error(f" 查询体质失败: 条件(body_id={body_id} 错误: {e}")
        return None

   # 获取所有体质
def get_body_all():
    try:
        with get_session() as session:
            stmt = select(XiuxianBody)
            return session.scalars(stmt).all() 
            
    except SQLAlchemyError as e:
        logger.error(f"查询体质失败 错误: {e}")
        return None