import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

#python train.py --data road_sign_data.yaml --imgsz --cfg --epochs 5 --workers 0 --save-period 1 --name yolo_road_det
from yolov5 import train

train.run(data='road_sign_data.yaml',
          cfg='road_sign_cfg.yaml',
          resume=True,
          device='cpu',
          epochs=100,
          workers=0,
          save_period=5,
          name='yolo_road_det')