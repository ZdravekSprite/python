from Detector import *
import os

def main():
    videoPath = "OpenCV/test.m4v"

    configPath = 'yolov5/models/road_sign_cfg.yaml'
    modelPath = 'yolov5/runs/train/yolo_road_det3/weights/best.pt'
    classesPath = 'OpenCV/test/road_sign.txt'
    modelType = "yolo"

    configPath = 'yolov7/cfg/training/custom-152.yaml'
    modelPath = 'yolov7/runs/train/custom-152/weights/best.pt'
    classesPath = 'yolov7/data/className.list'
    modelType = "yolo"

    configPath = os.path.join("OpenCV/dnn_model", "yolov4-tiny.cfg")
    modelPath = os.path.join("OpenCV/dnn_model", "yolov4-tiny.weights")
    classesPath = os.path.join("OpenCV/dnn_model", "classes.txt")
    modelType = "yolo"

    configPath = os.path.join("OpenCV/model_data", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    modelPath = os.path.join("OpenCV/model_data", "frozen_inference_graph.pb")
    classesPath = os.path.join("OpenCV/model_data", "coco.names")
    modelType = "mobilenet"

    detector = Detector(videoPath, configPath, modelPath, classesPath, modelType)
    detector.onVideo()

if __name__ == '__main__':
    main()