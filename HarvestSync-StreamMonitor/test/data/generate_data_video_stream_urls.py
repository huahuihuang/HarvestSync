#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   generate_data_video_stream_urls.py    
@Contact :   huahui_huang@qq.com
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/08/18     huahui_huang    1.0       None
"""

import random

import pandas as pd


# 生成模拟数据
def generate_data():
    qualities = ['1080p', '720p', '480p']
    formats = ['H.264', 'H.265']
    sources = ['source1', 'source2', 'source3']
    statuses = ['active', 'inactive']
    bandwidths = ['5Mbps', '10Mbps', '15Mbps']

    data = []
    for i in range(10000):
        id = i + 1
        title = 'video-' + str(id)
        description = 'description for video-' + str(id)
        stream_url = 'http://example.com/video-' + str(id) + '.mp4'
        added_date = pd.Timestamp.now()
        quality = random.choice(qualities)
        format = random.choice(formats)
        source = random.choice(sources)
        status = random.choice(statuses)
        bandwidth = random.choice(bandwidths)
        latitude = round(random.uniform(3.51, 53.55), 8)  # 限定在中国的纬度范围
        longitude = round(random.uniform(73.33, 135.05), 8)  # 限定在中国的经度范围

        data.append(
            [id, title, description, stream_url, added_date, quality, format, source, status, bandwidth, latitude,
             longitude])

    return data


# 保存为Excel文件
def save_to_excel(data):
    columns = ['id', 'title', 'description', 'stream_url', 'added_date', 'quality', 'format', 'source', 'status',
               'bandwidth', 'latitude', 'longitude']
    df = pd.DataFrame(data, columns=columns)
    df.to_excel('video_stream_data.xlsx', index=False)


if __name__ == "__main__":
    data = generate_data()
    save_to_excel(data)
