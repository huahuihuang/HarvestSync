#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   main.py
@Contact :   huahui_huang@qq.com
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/08/16     huahui_huang    1.0       None
"""
import logging
from typing import Optional

import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Depends, HTTPException
from fastapi.params import Query
from sqlalchemy.orm import Session

from app.crud import crud
from app.database.database import engine, Base, get_db, SessionLocal
from app.logs.logging_config import setup_logging
from app.models.health_check import HealthCheck
from app.models.model import LiveStreamExtractor
from app.schemas import schemas

setup_logging()  # 初始化日志配置

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    debug=False,
    title='HarvestSync-StreamMonitor',
    description='HarvestSync-StreamMonitor API文档',
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/redocs'
)

# 初始化 APScheduler
scheduler = BackgroundScheduler()
scheduler.start()


@app.post("/video/", response_model=schemas.VideoStream)
def create_video(video: schemas.VideoStreamCreate, db: Session = Depends(get_db)):
    logger.info(f"Attempting to create video with title: {video.title}")
    created_video = crud.create_video_stream(db=db, video=video)
    logger.info(f"Video with title {video.title} created successfully")

    # 热更新：创建视频流后立即开始监控它
    start_monitoring(created_video.id, db=db)

    return created_video


@app.get("/video/{video_id}", response_model=schemas.VideoStream)
def read_video(video_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching video with ID: {video_id}")
    db_video = crud.get_video_stream(db=db, video_id=video_id)
    if db_video is None:
        logger.error(f"Video with ID {video_id} not found")
        raise HTTPException(status_code=404, detail="Video not found")
    return db_video


@app.post("/monitor/{video_id}")
def monitor_task(video_id: int, interval: Optional[int] = Query(10), db: Session = Depends(get_db)):
    return start_monitoring(video_id, interval, db)


@app.delete("/monitor/{video_id}")
def stop_monitoring(video_id: int, db: Session = Depends(get_db)):
    logger.info(f"Stopping monitoring for video with ID: {video_id}")
    video = crud.get_video_stream(db, video_id=video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    job = scheduler.get_job(job_id=str(video_id))
    if job:
        job.remove()
        return {"status": f"Monitoring stopped for video: {video.title}"}
    else:
        raise HTTPException(status_code=404, detail=f"No monitoring found for video: {video.title}")


@app.get("/is_monitoring/{video_id}")
def is_monitoring(video_id: int, db: Session = Depends(get_db)):
    logger.info(f"Checking monitoring status for video with ID: {video_id}")
    video = crud.get_video_stream(db, video_id=video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    job = scheduler.get_job(job_id=str(video_id))
    return {"status": f"Monitoring {video.title}" if job else f"Not monitoring {video.title}"}


@app.on_event("startup")
async def startup_event():
    logger.info("Application startup event triggered. Preparing to initialize monitoring tasks...")

    with SessionLocal() as db:  # 假设SessionLocal是你的数据库会话
        videos = crud.get_video_streams(db, skip=0, limit=10001)  # 假设这个函数从数据库中获取所有视频
        logger.info(f"Retrieved {len(videos)} videos from the database for monitoring.")

        for video in videos:
            video_id = video.id

            # 添加健康检查任务
            health_checker = HealthCheck(video.stream_url, video_id)
            health_check_job_id = f"health_check_{video_id}"
            if not scheduler.get_job(job_id=health_check_job_id):
                scheduler.add_job(health_checker.check, 'interval', hours=24, id=health_check_job_id)
                logger.info(f"Started health check task for video ID: {video_id}, stream URL: {video.stream_url}")

            # 添加监控任务
            if not scheduler.get_job(job_id=str(video_id)):
                extractor = LiveStreamExtractor(video.stream_url)
                scheduler.add_job(extractor.extract_single_frame, 'interval', seconds=2, id=str(video_id))
                logger.info(
                    f"Started monitoring task for video ID: {video_id}, title: {video.title}, stream URL: {video.stream_url}")
            else:
                logger.warning(
                    f"Monitoring task already exists for video ID: {video_id}, title: {video.title}. Skipping...")

    logger.info("All monitoring and health check tasks initialized on startup.")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown event triggered. Preparing to stop all tasks...")

    jobs = scheduler.get_jobs()
    for job in jobs:
        job_id = job.id
        job.remove()
        if "health_check_" in job_id:
            logger.info(f"Stopped health check task with job ID: {job_id}")
        else:
            logger.info(f"Stopped monitoring task with job ID: {job_id}")

    scheduler.shutdown()
    logger.info("All tasks stopped on shutdown.")


def start_monitoring(video_id: int, interval: Optional[int] = 10, db: Session = Depends(get_db)):
    logger.info(f"Starting monitoring for video with ID: {video_id} with an interval of {interval} seconds")

    # Fetch video details from database
    video = crud.get_video_stream(db, video_id=video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    # Check if monitoring job already exists
    if not scheduler.get_job(job_id=str(video_id)):
        extractor = LiveStreamExtractor(video.stream_url)
        scheduler.add_job(extractor.extract_single_frame, 'interval', seconds=interval, id=str(video_id))
        logger.info(f"Monitoring started for video: {video.title} with an interval of {interval} seconds")
    else:
        logger.warning(f"Already monitoring video: {video.title}")


if __name__ == "__main__":
    logger.info("Starting FastAPI application")
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
