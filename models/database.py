from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import *

"""数据库配置相关"""

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://"+username+":"+password+"@"+mysqlhost+":"+mysqlport+"/"+mysqldb

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, encoding="utf8", echo=True
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
