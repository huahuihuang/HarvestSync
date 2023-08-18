#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   logging_config.py    
@Contact :   huahui_huang@qq.com
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/08/17     huahui_huang    1.0       None
"""

import logging
from logging.handlers import TimedRotatingFileHandler

import coloredlogs


def setup_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # 控制台高亮显示
    coloredlogs.install(level='DEBUG', logger=root_logger)

    # 定义日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 控制台日志处理
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # 使用RotatingFileHandler
    file_handler = TimedRotatingFileHandler('../HarvestSync-StreamMonitor/app/logs/HarvestSync.log', when='D',
                                            interval=1,
                                            backupCount=10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
