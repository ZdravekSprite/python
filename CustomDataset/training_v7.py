#!python train.py --batch 16 --cfg cfg/training/yolov7.yaml --epochs 55 --data {dataset.location}/data.yaml --weights 'yolov7.pt' --device 0 

#!python train.py --batch 16 --cfg cfg/training/yolov7-tiny-4.yaml --epochs 10 --data data/road_sign_data.yaml --weights 'yolov7.pt' --device 'cpu'

#python train.py --batch 8 --cfg cfg/training/yolov7-tiny-4.yaml --epochs 10 --data data/road_sign_data.yaml --name road_det --weights yolov7.pt

#python train.py --resume False --data road_sign_data.yaml --imgsz --cfg --epochs 5 --workers 0 --save-period 1 --name yolo_road_det