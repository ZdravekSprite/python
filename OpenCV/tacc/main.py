#Train a Cascade Classifier
#https://www.youtube.com/watch?v=XrCAvs9AePM
import cv2
import numpy as np
import os
from time import time
from vision import Vision

print(cv2.__version__)
#os.chdir(os.path.dirname(os.path.abspath(__file__)))

cap = cv2.VideoCapture('test.mp4')

# load the trained model
cascade_limestone = cv2.CascadeClassifier('cascade/cascade.xml')
# load an empty Vision class
vision_limestone = Vision(None)

loop_time = time()

while cap.isOpened():
    ret, frame = cap.read()

    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    if ret:
        # do object detection
        rectangles = cascade_limestone.detectMultiScale(frame)

        # draw the detection results onto the original image
        detection_image = vision_limestone.draw_rectangles(frame, rectangles)

        cv2.imshow('Train a Cascade Classifier', detection_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

cap.release()
print('Exit.')