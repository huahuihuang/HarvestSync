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

import cv2
from kafka import KafkaProducer


class LiveStreamExtractor:
    def __init__(self, stream_url, base_save_dir='./frames', kafka_bootstrap_servers='localhost:9092',
                 topic='live_stream_frames'):
        self.stream_url = stream_url
        self.capture = None
        self.base_save_dir = base_save_dir
        self.stream_folder_name = self._generate_folder_name_from_url(stream_url)
        self.save_dir = os.path.join(self.base_save_dir, self.stream_folder_name)
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers)

        # Setup logger
        self.logger = logging.getLogger(__name__)

        # Create save directory if it doesn't exist
        self._create_save_dir()

    @staticmethod
    def _generate_folder_name_from_url(url):
        """Generate a folder name from the stream URL."""
        return url.replace('/', '_').replace(':', '_').replace('.', '_')

    def _create_save_dir(self):
        """Helper method to create the save directory if it doesn't exist."""
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            self.logger.info(f"Created directory: {self.save_dir}")

    def extract_single_frame(self):
        """Extract and send a single frame from the live stream to Kafka."""
        self.capture = cv2.VideoCapture(self.stream_url)
        if not self.capture.isOpened():
            self.logger.error("Unable to open video stream.")
            return

        ret, frame = self.capture.read()
        if ret:
            self._send_frame_to_kafka(frame)
        else:
            self.logger.warning(f"Failed to read frame from: {self.stream_url}")

        self.capture.release()
        self.logger.info("Video capture released.")

    def _send_frame_to_kafka(self, frame):
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        self.producer.send(self.topic, frame_bytes)

    def _save_frame(self, frame, timestamp):
        filename = f"{timestamp}.jpg"
        filepath = os.path.join(self.save_dir, filename)
        cv2.imwrite(filepath, frame)
        self.logger.info(f"Saved frame to: {filepath}")
