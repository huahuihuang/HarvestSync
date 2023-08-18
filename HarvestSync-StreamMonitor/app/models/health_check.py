#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   health_check.py    
@Contact :   huahui_huang@qq.com
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/08/18     huahui_huang    1.0       None
"""
import logging
import smtplib
from email.message import EmailMessage

import requests


class HealthCheck:
    def __init__(self, stream_url, video_id):
        self.stream_url = stream_url
        self.video_id = video_id
        # Setup logger
        self.logger = logging.getLogger(__name__)

    def check(self):
        try:
            response = requests.get(self.stream_url, timeout=10)  # 设置一个超时时间，例如10秒
            if response.status_code != 200:
                self.logger.error(f"Video stream with ID {self.video_id} is not healthy!")
                self.notify()  # 发送通知
        except requests.RequestException as e:
            self.logger.error(f"Error checking video stream with ID {self.video_id}: {e}")
            self.notify()  # 发送通知

    def notify(self):
        # 当前只实现了电子邮件通知，但你可以在这里添加其他通知方式
        self.send_alert_email()

    def send_alert_email(self):
        # 这是一个简单的发送电子邮件的示例，你可能需要根据你的SMTP服务进行调整
        msg = EmailMessage()
        msg.set_content(f"Video stream with ID {self.video_id} is not healthy!")
        msg["Subject"] = "Video Stream Health Alert"
        msg["From"] = "alert@example.com"
        msg["To"] = "admin@example.com"

        # 使用SMTP服务发送邮件
        try:
            with smtplib.SMTP("smtp.example.com", 587) as server:
                server.starttls()
                server.login("alert@example.com", "password")
                server.send_message(msg)
                self.logger.info(f"Sent health alert email for video ID {self.video_id}")
        except Exception as e:
            self.logger.error(f"Error sending health alert email for video ID {self.video_id}: {e}")

    # 为将来的拓展预留的方法
    def send_sms_alert(self):
        # 你可以在这里实现发送短信的功能
        pass

    def send_slack_alert(self):
        # 你可以在这里实现发送Slack消息的功能
        pass
