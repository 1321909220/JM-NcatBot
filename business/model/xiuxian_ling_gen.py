"""灵根"""
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
#  灵根表
class XiuxianLingGen(Base):
    __table__ = Table(
        'xiuxian_ling_gen', 
        Base.metadata,   
        autoload_with=engine,
        autoload_replace=False,
        extend_existing=True  # 新增：允许表定义扩展 
    )
    
    # 新增：方便调试的repr 
    def __repr__(self):
        return f"<XiuxianLingGen(id={self.ling_gen_id},  name={self.ling_gen_name})>" 

from typing import Optional, Union 
from sqlalchemy import select 

# 获取灵根详情
def get_ling_gen_by_id(
    ling_gen_id: Optional[int] = None,
) -> Optional[XiuxianLingGen]:
    try:
        with get_session() as session:
            # 构建查询条件 
            stmt = select(XiuxianLingGen)
            if ling_gen_id is not None:
                stmt = stmt.where(XiuxianLingGen.ling_gen_id  == ling_gen_id) 
            # 获取第一条结果 
            return session.scalars(stmt.limit(1)).first() 
            
    except SQLAlchemyError as e:
        logger.error(f" 查询灵根失败: 条件(ling_gen_id={ling_gen_id} 错误: {e}")
        return None

    #获取所有灵根 
def get_ling_gen_all():
    try:
        with get_session() as session:
            stmt = select(XiuxianLingGen)
            return session.scalars(stmt).all() 
            
    except SQLAlchemyError as e:
        logger.error(f"查询灵根失败 错误: {e}")
        return None
