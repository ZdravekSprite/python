import cv2
import numpy as np
import time
import os

cap = cv2.VideoCapture('OpenCV/test.mp4')
configPath = os.path.join("OpenCV/dnn_model", "yolov4-tiny.cfg")
modelPath = os.path.join("OpenCV/dnn_model", "yolov4-tiny.weights")

info = {
    "framecount": cap.get(cv2.CAP_PROP_FRAME_COUNT),
    "fps": cap.get(cv2.CAP_PROP_FPS),
    "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
    "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    "codec": int(cap.get(cv2.CAP_PROP_FOURCC))
}
print(info)

net = cv2.dnn_DetectionModel(modelPath, configPath)

while cap.isOpened():
    ret, frame = cap.read()
    image = np.array(frame)

    startTime = 0

    if ret:
        currentTime = time.time()
        fps = 1/(currentTime - startTime)
        startTime = currentTime

        cv2.imshow('play', image)


        key = cv2.waitKey(30) & 0xFF
        if key == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
