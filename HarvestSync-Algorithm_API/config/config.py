#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   config.py    
@Contact :   huahui_huang@qq.com
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/09/17     huahui_huang    1.0       None
"""
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    debug: bool = False
    processes: int = 1
    port: int = 9003
    weights: str = "weights"
    ip: str = "0.0.0.0"

    class Config:
        env_file = ".env"
