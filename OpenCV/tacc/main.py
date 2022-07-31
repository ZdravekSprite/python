#Train a Cascade Classifier
#https://www.youtube.com/watch?v=XrCAvs9AePM
import cv2
import numpy as np
import os
from time import time
from vision import Vision

print(cv2.__version__)
#os.chdir(os.path.dirname(os.path.abspath(__file__)))

cap = cv2.VideoCapture('lrv/test.LRV')

# load the trained model
cascade_signs = cv2.CascadeClassifier('cascade/cascade.xml')
# load an empty Vision class
vision_signs = Vision(None)

loop_time = time()

while cap.isOpened():
    ret, frame = cap.read()

    if (time() - loop_time) == 0:
        break

    print(f'\rFPS {1 / (time() - loop_time)}', end = "\r")
    loop_time = time()

    if ret:
        # do object detection
        rectangles = cascade_signs.detectMultiScale(frame)

        # draw the detection results onto the original image
        detection_image = vision_signs.draw_rectangles(frame, rectangles)

        cv2.imshow('Train a Cascade Classifier', detection_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
print('Exit.')