from sqlalchemy import create_engine 
from contextlib import contextmanager 
from sqlalchemy.orm  import Session as SessionType, sessionmaker 
from typing import Generator 
import os  # 环境变量 
# 连接到 MySQL 数据库
username = 'xiuxian'
password = 'NA72cz3hf6mESZwk'
host = '111.229.33.164'  # 'localhost'
port = '3306'
database = 'xiuxian'

# 创建连接引擎
dbHost = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'

engine = create_engine(
    dbHost,
    echo=True,  		# 是否打印SQL
    pool_size=10,  		# 连接池的大小，指定同时在连接池中保持的数据库连接数，默认:5
    max_overflow=20,  	# 超出连接池大小的连接数，超过这个数量的连接将被丢弃,默认: 5
    pool_pre_ping=True, # 连接池健康检查 
    pool_recycle=3600,  # 连接回收时间(秒)
    connect_args={
        'connect_timeout': 5  # 连接超时设置 
    },
)
# 会话工厂 
Session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=SessionType  # 指定session类 
)
@contextmanager 
def get_session() -> Generator[SessionType, None, None]:
    """带类型注解的会话生成器"""
    session = Session()
    try:
        yield session 
        session.commit()  
    except Exception as e:
        session.rollback()  
        raise e  # 保留原始异常堆栈 
    finally:
        session.close() 

