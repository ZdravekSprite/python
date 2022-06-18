import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

#python train.py --data road_sign_data.yaml --epochs 5 --workers 0 --name yolo_road_det
from yolov5 import train

train.run(data='road_sign_data.yaml', epochs=5, workers=0, name='yolo_road_det')