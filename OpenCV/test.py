import cv2
import numpy as np
import time
import os

np.random.seed(20)

cap = cv2.VideoCapture('OpenCV/test.mp4')
configPath = os.path.join("OpenCV/dnn_model", "yolov4-tiny.cfg")
modelPath = os.path.join("OpenCV/dnn_model", "yolov4-tiny.weights")
classesPath = os.path.join("OpenCV/dnn_model", "classes.txt")
framecount = cap.get(cv2.CAP_PROP_FRAME_COUNT)

info = {
    "framecount": framecount,
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

frameNo = 0

while cap.isOpened():
    ret, image = cap.read()
    #image = np.array(frame)


    if ret:
        frameNo += 1
        classLabelIDs, confidences, bboxs = net.detect(
            image, confThreshold=0.5)

        bboxs = list(bboxs)
        confidences = list(np.array(confidences).reshape(1, -1)[0])
        confidences = list(map(float, confidences))

        bboxIdx = cv2.dnn.NMSBoxes(
            bboxs, confidences, score_threshold=0.5, nms_threshold=0.2)

        if len(bboxIdx) != 0:
            for i in range(0, len(bboxIdx)):
                bbox = bboxs[np.squeeze(bboxIdx[i])]
                classConfidence = confidences[np.squeeze(bboxIdx[i])]

                classLabelID = np.squeeze(
                    classLabelIDs[np.squeeze(bboxIdx[i])])
                classLabel = classesList[classLabelID]
                classColor = [int(c) for c in colorList[classLabelID]]
                displayText = "{}:{:.2f}".format(
                    classLabel, classConfidence)
                x, y, w, h = bbox
                cv2.rectangle(image, (x, y), (x+w, y+h),
                              color=classColor, thickness=1)
                cv2.putText(image, displayText, (x, y-10),
                            cv2.FONT_HERSHEY_PLAIN, 1, classColor, 2)

        cv2.putText(image, "frame: " + str(int(frameNo)), (20, 70),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
        cv2.imshow('play', image)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if frameNo >= framecount/2:
            break
        (ret, image) = cap.read()
cap.release()
cv2.destroyAllWindows()
