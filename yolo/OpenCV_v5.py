import cv2
import numpy as np
import torch
import os
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
script_path = Path(SCRIPT_DIR)
yolov5_path = "/".join(str(script_path.parent / "yolov5").split("\\"))
model_path = yolov5_path + '/yolov5.pt'

# Model
model = torch.hub.load(yolov5_path, 'custom', path=model_path, source='local')

cap = cv2.VideoCapture('OpenCV/test.mp4')
#width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


while cap.isOpened():
    ret, frame = cap.read()
    image_np = np.array(frame)

    if ret:
        # Inference
        results = model(image_np)

        # Results
        #.print() .show(), .save(), .crop(), .pandas(), etc.
        #print(results)

        #cv2.imshow('object detection', cv2.resize(image_np, (960, 540)))
        cv2.imshow('Inference', image_np)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
