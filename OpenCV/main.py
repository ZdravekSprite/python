from Detector import *
import os

def main():
    videoPath = "OpenCV/test.mp4"

    configPath = os.path.join("OpenCV/model_data", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    modelPath = os.path.join("OpenCV/model_data", "frozen_inference_graph.pb")
    classesPath = os.path.join("OpenCV/model_data", "coco.names")
    modelType = "mobilenet"

    configPath = os.path.join("OpenCV/dnn_model", "yolov4-tiny.cfg")
    modelPath = os.path.join("OpenCV/dnn_model", "yolov4-tiny.weights")
    classesPath = os.path.join("OpenCV/dnn_model", "classes.txt")
    modelType = "yolo"

    configPath = 'yolov5/models/road_sign_cfg.yaml'
    modelPath = 'yolov5/runs/train/yolo_road_det3/weights/best.pt'
    classesPath = 'OpenCV/test/road_sign.txt'
    modelType = "yolo"

    detector = Detector(videoPath, configPath, modelPath, classesPath, modelType)
    detector.onVideo()

if __name__ == '__main__':
    main()