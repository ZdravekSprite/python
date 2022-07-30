import torch
import os
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
script_path = Path(SCRIPT_DIR)
yolov5_path = "/".join(str(script_path.parent / "yolov5").split("\\"))
model_path = yolov5_path + '/yolov5.pt'

# Model
#model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom
model = torch.hub.load(yolov5_path, 'custom', path=model_path, source='local')

# Images
img = 'https://ultralytics.com/images/zidane.jpg'  # or file, Path, PIL, OpenCV, numpy, list

# Inference
results = model(img)

# Results
#.print() .show(), .save(), .crop(), .pandas(), etc.
print(results.pandas())
