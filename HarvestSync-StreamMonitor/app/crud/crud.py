#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   crud.py    
@Contact :   huahui_huang@qq.com
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/08/16     huahui_huang    1.0       None
"""

from sqlalchemy.orm import Session

from ..models import models
from ..schemas import schemas


def create_video_stream(db: Session, video: schemas.VideoStreamCreate):
    db_video = models.VideoStream(**video.model_dump())
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


def get_video_stream(db: Session, video_id: int):
    return db.query(models.VideoStream).filter(models.VideoStream.id == video_id).first()


def get_video_streams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.VideoStream).offset(skip).limit(limit).all()


def update_video_stream(db: Session, video_id: int, video: schemas.VideoStreamCreate):
    db_video = db.query(models.VideoStream).filter(models.VideoStream.id == video_id).first()
    for key, value in video.model_dump().items():
        setattr(db_video, key, value)
    db.commit()
    return db_video


def delete_video_stream(db: Session, video_id: int):
    db_video = db.query(models.VideoStream).filter(models.VideoStream.id == video_id).first()
    db.delete(db_video)
    db.commit()
    return db_video
