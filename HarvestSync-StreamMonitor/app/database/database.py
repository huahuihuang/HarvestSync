#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   database.py    
@Contact :   huahui_huang@qq.com
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/07/16     huahui_huang    1.0       None
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库连接配置
SQLALCHEMY_DATABASE_URI = (
    "mysql+pymysql://root:161618qqh,.@localhost/harvestsync"
    #                用户:密码@服务器/数据库?参数
)

# 创建数据库引擎
engine = create_engine(SQLALCHEMY_DATABASE_URI)
# 创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 声明基类
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
