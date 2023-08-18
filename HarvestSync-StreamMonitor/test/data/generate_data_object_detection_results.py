#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   generate_data_object_detection_results.py    
@Contact :   huahui_huang@qq.com
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/08/18     huahui_huang    1.0       None
"""
import random

import pandas as pd

# Define the categories
categories = ['Anomala corpulenta', 'Athetis lepigone', 'Bollworm', 'Meadow borer', 'holotrichia parallela',
              'Armyworm', 'Agriotes fuscicollis Miwa', 'Spodoptera exigua', 'Gryllotalpa orientalis', 'Little Gecko',
              'Scotogramma trifolii Rottemberg', 'Spodoptera cabbage', 'Rice planthopper', 'Spodoptera litura',
              'Yellow tiger', 'Stem borer', 'Plutella xylostella', 'Rice Leaf Roller', 'Melahotus',
              'Striped rice borer', 'Land tiger', 'Nematode trench', 'eight-character tiger', 'holotrichia oblita']

# Generate random data
data = {
    'detection_id': list(range(1, 10001)),
    'media_id': [random.randint(1, 5000) for _ in range(10000)],
    'object_class': [random.choice(categories) for _ in range(10000)],
    'confidence': [round(random.uniform(0.0001, 1.0000), 4) for _ in range(10000)],
    'bbox_x': [random.randint(0, 1920) for _ in range(10000)],
    'bbox_y': [random.randint(0, 1080) for _ in range(10000)],
    'bbox_width': [random.randint(1, 1920) for _ in range(10000)],
    'bbox_height': [random.randint(1, 1080) for _ in range(10000)]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Export to Excel
df.to_excel("object_detection_results.xlsx", index=False, engine='openpyxl')

print("Data exported to object_detection_results.xlsx")

# if __name__ == '__main__':
#     print_hi('Python')
