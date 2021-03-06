import cv2

import numpy as np
import time

np.random.seed(20)


class Detector:
    def __init__(self, videoPath, configPath, modelPath, classesPath, modelType='mobilenet'):
        self.videoPath = videoPath
        self.configPath = configPath
        self.modelPath = modelPath
        self.classesPath = classesPath
        self.modelType = modelType

        ##############################

        self.net = cv2.dnn_DetectionModel(self.modelPath, self.configPath)
        self.net.setInputSize(320, 320)
        if self.modelType == 'mobilenet':
            self.net.setInputScale(1.0/127.5)
            self.net.setInputMean((127.5, 127.5, 127.5))
            self.net.setInputSwapRB(True)
        if self.modelType == 'yolo':
            self.net.setInputScale(1.0/255.0)

        self.readClasses()

    def readClasses(self):
        with open(self.classesPath, 'r') as f:
            self.classesList = f.read().splitlines()

        if self.modelType == 'mobilenet':
            self.classesList.insert(0, '__Background__')

        self.colorList = np.random.uniform(
            low=0, high=255, size=(len(self.classesList), 3))

        # print(self.classesList)

    def onVideo(self):
        cap = cv2.VideoCapture(self.videoPath)

        if (cap.isOpened() == False):
            print("Error opening file...")
            return

        info = {
            "framecount": cap.get(cv2.CAP_PROP_FRAME_COUNT),
            "fps": cap.get(cv2.CAP_PROP_FPS),
            "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "codec": int(cap.get(cv2.CAP_PROP_FOURCC))
        }
        print(info)

        success, frame = cap.read()
        image = np.array(frame)

        startTime = 0

        while success:
            currentTime = time.time()
            fps = 1/(currentTime - startTime)
            startTime = currentTime

            classLabelIDs, confidences, bboxs = self.net.detect(
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
                    classLabel = self.classesList[classLabelID]
                    classColor = [int(c) for c in self.colorList[classLabelID]]

                    displayText = "{}:{:.2f}".format(
                        classLabel, classConfidence)

                    x, y, w, h = bbox

                    cv2.rectangle(image, (x, y), (x+w, y+h),
                                  color=classColor, thickness=1)
                    cv2.putText(image, displayText, (x, y-10),
                                cv2.FONT_HERSHEY_PLAIN, 1, classColor, 2)

            cv2.putText(image, "FPS: " + str(int(fps)), (20, 70),
                        cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
            cv2.imshow(self.modelType, image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            (success, image) = cap.read()
        cv2.destroyAllWindows()
