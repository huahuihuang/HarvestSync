#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   logging_config.py    
@Contact :   huahui_huang@qq.com
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/09/17     huahui_huang    1.0       None
"""

from loguru import logger


def setup_logging():
    logger.add("logs/app.log", rotation="1 day", retention="10 days", level="INFO")
    return logger
