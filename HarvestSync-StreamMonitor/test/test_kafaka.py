#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   test_kafaka.py    
@Contact :   huahui_huang@qq.com
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/08/18     huahui_huang    1.0       None
"""
import json

from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['127.0.0.1:9092']
)

for _id in range(1, 5):
    content = {"title": "生命不息，运动不止!", "index": _id}
    future = producer.send(
        topic="test_topic",
        value=json.dumps(content, ensure_ascii=False).encode("utf-8"),
    )
    result = future.get(timeout=10)
    print("kafka生产消息:", result)
