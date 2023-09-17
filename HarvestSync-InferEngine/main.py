#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   main.py    
@Contact :   huahui_huang@qq.com
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/08/18     huahui_huang    1.0       None
"""
import time

import cv2
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from kafka import KafkaConsumer

matplotlib.use('TkAgg')


class KafkaFrameConsumer:
    def __init__(self, topic, kafka_bootstrap_servers='localhost:9092'):
        self.topic = topic
        self.consumer = KafkaConsumer(self.topic, bootstrap_servers=kafka_bootstrap_servers)

    def consume_and_display_frames(self):
        frame_count = 0
        start_time = time.time()
        last_print_time = start_time

        # Set up the display with matplotlib
        plt.ion()
        fig, ax = plt.subplots()
        img_display = ax.imshow(
            np.zeros((480, 640, 3), dtype=np.uint8))  # Assuming a default frame size, adjust if necessary

        for message in self.consumer:
            frame_bytes = message.value
            frame = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), -1)

            # Update the displayed frame with matplotlib
            img_display.set_data(frame)
            plt.draw()
            plt.pause(0.01)  # Display each frame for 10 milliseconds

            frame_count += 1
            current_time = time.time()
            elapsed_time = current_time - start_time

            # Print the speed every second
            if current_time - last_print_time >= 1.0:
                speed = frame_count / elapsed_time
                print(f"Consumed {frame_count} frames in {elapsed_time:.2f} seconds. Speed: {speed:.2f} frames/sec")
                last_print_time = current_time

        plt.ioff()
        plt.show()


# Example usage:
consumer = KafkaFrameConsumer(topic="live_stream_frames")
consumer.consume_and_display_frames()
