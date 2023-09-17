import base64
import unittest

import requests


class YOLOv5APITestCase(unittest.TestCase):
    API_URL = "http://localhost:9003/v1/pests/detections/Pest_yolov5s"  # 根据您的配置修改

    def encode_image(self, image_path):
        """将图像转换为base64编码"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def send_request(self, algorithm, encoded_image):
        """发送请求到API并返回响应"""
        data = {
            "algorithm": algorithm,
            "image_base64": encoded_image
        }
        return requests.post(self.API_URL, json=data)

    def test_yolov5_detection(self):
        encoded_image = self.encode_image("0000058.jpg")
        response = self.send_request("Pest_yolov5s", encoded_image)

        self.assertEqual(response.status_code, 200)

        # 检查返回的数据是否包含预期的字段
        json_response = response.json()
        print(json_response)  # 打印返回的结果

        self.assertIn("code", json_response)
        self.assertIn("msg", json_response)
        self.assertIn("result", json_response)
        self.assertIsInstance(json_response["result"], list)

    def test_invalid_algorithm(self):
        encoded_image = self.encode_image("0000058.jpg")
        response = self.send_request("InvalidAlgorithm", encoded_image)

        self.assertEqual(response.status_code, 400)

    # 可以继续添加其他的测试用例，例如测试无效的图像格式等


if __name__ == '__main__':
    unittest.main()
