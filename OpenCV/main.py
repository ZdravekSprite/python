from Detector import *
import os

def main():
    videoPath = "OpenCV/test.mp4"

    configPath1 = os.path.join("OpenCV/model_data", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    modelPath1 = os.path.join("OpenCV/model_data", "frozen_inference_graph.pb")
    classesPath1 = os.path.join("OpenCV/model_data", "coco.names")
    modelType1 = "mobilenet"
    configPath2 = os.path.join("OpenCV/dnn_model", "yolov4-tiny.cfg")
    modelPath2 = os.path.join("OpenCV/dnn_model", "yolov4-tiny.weights")
    classesPath2 = os.path.join("OpenCV/dnn_model", "classes.txt")
    modelType2 = "yolo"

    detector = Detector(videoPath, configPath2, modelPath2, classesPath2, modelType2)
    detector.onVideo()

if __name__ == '__main__':
    main()