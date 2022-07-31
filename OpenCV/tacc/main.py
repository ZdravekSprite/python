#Train a Cascade Classifier
import cv2
import numpy as np
import os
from time import time

print(cv2.__version__)
#os.chdir(os.path.dirname(os.path.abspath(__file__)))

cap = cv2.VideoCapture('OpenCV/test.mp4')

loop_time = time()

while cap.isOpened():
    ret, frame = cap.read()

    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    if ret:
        cv2.imshow('Train a Cascade Classifier', frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

cap.release()