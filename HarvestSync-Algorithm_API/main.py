#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   main.py
@Contact :   huahui_huang@qq.com
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/09/16     huahui_huang    1.0       None
"""
import argparse
import base64
import binascii

import cv2
import numpy as np
import yaml
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config.config import Config
from logger.logging_config import setup_logging
from models.model import ImageRequest, ImageResponse
from yolov5_inference import YoloV5Detector

logger = setup_logging()
app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load configurations from the YAML file
with open("config/config.yaml", "r") as file:
    configs = yaml.safe_load(file)

detect_IN_conf = configs["detect_conf"]
YoloV5Detector_IN_conf = configs["YoloV5Detector_IN_conf"]

# Define a global variable for the model
detector: YoloV5Detector


@app.on_event("startup")
async def load_model():
    logger.info("Starting up the FastAPI application...")
    global detector
    detector = YoloV5Detector(in_conf=YoloV5Detector_IN_conf, device=args.device)


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the FastAPI application...")


@app.post("/v1/pests/detections/Pest_yolov5s", response_model=ImageResponse)
async def image_object_detect(request: ImageRequest):
    algorithm_str = request.algorithm
    image_base64 = request.image_base64

    logger.info(f"[*]=====================Received request with algorithm: {request.algorithm}====================")

    if not image_base64:
        logger.warning("No image uploaded")
        raise HTTPException(status_code=400, detail="Image not uploaded")

    if algorithm_str not in ["Pest_yolov5s"]:
        logger.error(f"Unsupported algorithm: {algorithm_str}")
        raise HTTPException(status_code=400, detail=f"Unsupported algorithm: {algorithm_str}")

    try:
        encoded_image_byte = base64.b64decode(image_base64)
        image_array = np.frombuffer(encoded_image_byte, np.uint8)
        im = cv2.imdecode(image_array, cv2.COLOR_RGB2BGR)
    except binascii.Error:
        logger.error("Base64 decoding failed")
        raise HTTPException(status_code=400, detail="Base64 decoding failed")
    except cv2.error:
        logger.error("Image decoding failed")
        raise HTTPException(status_code=400, detail="Image decoding failed")

    detect_data = detector.detect(image=im, detect_conf=detect_IN_conf)

    logger.info("Detection completed successfully")
    logger.info(f"=========================================================================================\n")

    return ImageResponse(code=200, msg="Success", result=detect_data)


if __name__ == "__main__":
    import uvicorn

    parser = argparse.ArgumentParser(description="FastAPI for YOLOv5 Detection")
    parser.add_argument('--device', default='cpu',
                        help='Device to run the model on (i.e. 0 or 0,1,2,3 or cpu"). Default is "cpu".')
    args = parser.parse_args()

    config = Config()
    uvicorn.run(app, host=config.ip, port=config.port)
