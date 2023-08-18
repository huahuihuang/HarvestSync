#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   test_viedo.py    
@Contact :   huahui_huang@qq.com
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/08/08     huahui_huang    1.0       None
"""

import os
import threading
import time

import cv2


class LiveStreamExtractor:
    def __init__(self, stream_url, interval=1, save_dir='./frames'):
        self.stream_url = stream_url
        self.interval = interval
        self.capture = None
        self.thread = None
        self.stop_flag = False
        self.save_dir = save_dir

        # 如果保存目录不存在，创建它
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def _save_frame(self, frame, timestamp):
        filename = f"{self.stream_url.replace('/', '_').replace(':', '_')}_{timestamp}.jpg"
        filepath = os.path.join(self.save_dir, filename)
        cv2.imwrite(filepath, frame)

    def _extract_frames(self):
        self.capture = cv2.VideoCapture(self.stream_url)

        if not self.capture.isOpened():
            print("无法打开视频流")
            return

        while not self.stop_flag:
            ret, frame = self.capture.read()
            if not ret:
                break

            timestamp = int(time.time())  # 获取当前时间戳
            self._save_frame(frame, timestamp)  # 保存帧

            time.sleep(self.interval)

        self.capture.release()

    def start_extraction(self):
        self.stop_flag = False
        self.thread = threading.Thread(target=self._extract_frames)
        self.thread.start()

    def stop_extraction(self):
        self.stop_flag = True
        if self.thread:
            self.thread.join()


if __name__ == '__main__':
    # 使用方法
    stream = LiveStreamExtractor('rtmp://liteavapp.qcloud.com/live/liteavdemoplayerstreamid', 30)  # 提取帧的间隔为2秒
    stream.start_extraction()

    # 当你想停止提取时
    # stream.stop_extraction()
