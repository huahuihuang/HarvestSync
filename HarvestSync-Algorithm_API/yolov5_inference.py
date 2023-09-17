#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   yolov5_inference.py    
@Contact :   huahui_huang@qq.com
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/09/16     huahui_huang    1.0       None
"""

import numpy as np
import torch

from models.common import DetectMultiBackend
from utils.augmentations import letterbox
from utils.general import non_max_suppression, check_img_size


class YoloV5Detector:
    def __init__(self, in_conf, device):
        """
        Initialize the YOLOv5 detector.
        """
        self.device = device
        self.model = DetectMultiBackend(in_conf["weights"], device=self.device, dnn=in_conf["dnn"],
                                        data=in_conf["data"], fp16=in_conf["half"])
        self.stride, self.names, self.pt = self.model.stride, self.model.names, self.model.pt
        self.imgsz = check_img_size(in_conf["imgsz"], s=self.stride)

    def preprocess_image(self, image):
        """
        Preprocess the input image.
        """
        im = letterbox(image, self.imgsz, stride=self.stride, auto=self.pt)[0]
        im = im.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        im = np.ascontiguousarray(im)
        im = torch.from_numpy(im).to(self.device)
        im = im.half() if self.model.fp16 else im.float()
        im /= 255.0
        if im.ndimension() == 3:
            im = im[None]
        return im

    def postprocess_predictions(self, pred):
        """
        Postprocess model predictions.
        """
        formatted_results = []
        for *xyxy, conf, cls in pred[0]:
            result = {
                "bbox": [float(coord) for coord in xyxy],
                "confidence": float(conf),
                "class": int(cls),
                "label": self.names[int(cls)]
            }
            formatted_results.append(result)

        return formatted_results

    def detect(self, image, detect_conf):
        """
        Detect objects in an image.
        """
        if not isinstance(image, np.ndarray) or not isinstance(detect_conf, dict):
            raise ValueError("Invalid input format for image or detect_conf")

        im = self.preprocess_image(image)
        with torch.no_grad():
            pred = self.model(im, detect_conf["augment"])
            pred = non_max_suppression(pred, detect_conf["conf_thres"], detect_conf["iou_thres"],
                                       detect_conf["classes"], detect_conf["agnostic_nms"],
                                       max_det=detect_conf["max_det"])

        return self.postprocess_predictions(pred)
