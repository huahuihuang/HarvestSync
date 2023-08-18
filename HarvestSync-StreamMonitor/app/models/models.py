#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   models.py    
@Contact :   huahui_huang@qq.com
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/08/16     huahui_huang    1.0       None
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Enum

from ..database.database import Base


class VideoStream(Base):
    __tablename__ = "video_stream_urls"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    stream_url = Column(String(1024), nullable=False)
    added_date = Column(DateTime, default=func.now())
    quality = Column(String(50))
    format = Column(String(50))
    source = Column(String(255))
    status = Column(Enum('active', 'inactive'), default='active')
    bandwidth = Column(String(50))
