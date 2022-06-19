# python detect.py --source ../Road_Sign_Dataset/images/test/ --weights runs/train/exp9/weights/best.pt --conf 0.25 --name yolo_road_det
# python detect.py --weights best.pt --source test.mp4 --view-img --name test02 --device cpu --save-conf
# python detect.py --source test.mp4 --weights runs/train/exp9/weights/best.pt --conf 0.25 --name yolo_road_det

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from yolov5 import detect

# python detect.py --weights best.pt --source test.mp4 --view-img --name test02 --device cpu --save-conf
detect.run(weights='yolov5/runs/train/yolo_road_det3/weights/best.pt',
           source='yolov5/test.mp4',
           data='yolov5/data/road_sign_data.yaml',
           view_img=True,
           exist_ok=True,
           line_thickness=1,
           name='yolo_road_det2')

"""
import os
from PIL import Image
import random
import numpy as np
import matplotlib.pyplot as plt

path = "C:\\git\\python\\yolov5"
detections_dir = os.path.sep.join([path, "runs\\detect\\yolo_road_det"])
#print(detections_dir)
detection_images = [os.path.join(detections_dir, x) for x in os.listdir(detections_dir)]
#print(detection_images)
random_detection_image = Image.open(random.choice(detection_images))
#print(random_detection_image)
plt.imshow(np.array(random_detection_image))
plt.show()
"""
