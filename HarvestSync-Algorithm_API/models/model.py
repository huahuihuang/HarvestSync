#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   model.py    
@Contact :   huahui_huang@qq.com
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/09/16     huahui_huang    1.0       None
"""
from typing import Optional

from pydantic import BaseModel


class ImageRequest(BaseModel):
    algorithm: Optional[str] = "Pest_yolov5s"
    image_base64: str


class ImageResponse(BaseModel):
    code: int
    msg: str
    result: list
