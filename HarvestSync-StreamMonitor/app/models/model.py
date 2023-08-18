#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   models.py
@Contact :   huahui_huang@qq.com
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/07/16     huahui_huang    1.0       None
"""
import logging
import os
import time

import cv2


class LiveStreamExtractor:
    def __init__(self, stream_url, save_dir='./frames'):
        self.stream_url = stream_url
        self.capture = None
        self.save_dir = save_dir

        # Setup logger
        self.logger = logging.getLogger(__name__)

        # Create save directory if it doesn't exist
        self._create_save_dir()

    def _create_save_dir(self):
        """Helper method to create the save directory if it doesn't exist."""
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            self.logger.info(f"Created directory: {self.save_dir}")

    def _save_frame(self, frame, timestamp):
        filename = f"{self.stream_url.replace('/', '_').replace(':', '_')}_{timestamp}.jpg"
        filepath = os.path.join(self.save_dir, filename)
        cv2.imwrite(filepath, frame)
        self.logger.info(f"Saved frame to: {filepath}")

    def extract_single_frame(self):
        """Extract and save a single frame from the live stream."""
        self.capture = cv2.VideoCapture(self.stream_url)
        if not self.capture.isOpened():
            self.logger.error("Unable to open video stream.")
            return

        ret, frame = self.capture.read()
        if ret:
            timestamp = int(time.time())
            self._save_frame(frame, timestamp)
        else:
            self.logger.warning(f"Failed to read frame from: {self.stream_url}")

        self.capture.release()
        self.logger.info("Video capture released.")
