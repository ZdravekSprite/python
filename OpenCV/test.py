import cv2
import numpy as np
import time
import os

cap = cv2.VideoCapture('OpenCV/test.mp4')
configPath = os.path.join("OpenCV/dnn_model", "yolov4-tiny.cfg")
modelPath = os.path.join("OpenCV/dnn_model", "yolov4-tiny.weights")
classesPath = os.path.join("OpenCV/dnn_model", "classes.txt")

info = {
    "framecount": cap.get(cv2.CAP_PROP_FRAME_COUNT),
    "fps": cap.get(cv2.CAP_PROP_FPS),
    "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
    "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    "codec": int(cap.get(cv2.CAP_PROP_FOURCC))
}
print(info)

net = cv2.dnn_DetectionModel(modelPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0/255.0)
with open(classesPath, 'r') as f:
    classesList = f.read().splitlines()
    colorList = np.random.uniform(
        low=0, high=255, size=(len(classesList), 3))

while cap.isOpened():
    ret, frame = cap.read()
    image = np.array(frame)

    startTime = 0

    if ret:
        currentTime = time.time()
        fps = 1/(currentTime - startTime)
        startTime = currentTime

        classLabelIDs, confidences, bboxs = net.detect(
            image, confThreshold=0.5)

        cv2.imshow('play', image)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
