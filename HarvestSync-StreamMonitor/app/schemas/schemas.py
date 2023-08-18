#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   schemas.py    
@Contact :   huahui_huang@qq.com
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/08/16     huahui_huang    1.0       None
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class VideoStreamBase(BaseModel):
    title: str
    description: Optional[str] = None
    stream_url: str
    quality: Optional[str] = None
    format: Optional[str] = None
    source: Optional[str] = None
    status: Optional[str] = "active"
    bandwidth: Optional[str] = None


class VideoStreamCreate(VideoStreamBase):
    pass


class VideoStream(VideoStreamBase):
    id: int
    added_date: datetime

    class Config:
        orm_mode = True
