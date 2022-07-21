# python detect.py --source ../Road_Sign_Dataset/images/test/ --weights runs/train/exp9/weights/best.pt --conf 0.25 --name yolo_road_det
# python detect.py --weights best.pt --source test.mp4 --view-img --name test02 --device cpu --save-conf
# python detect.py --source test.mp4 --weights runs/train/exp9/weights/best.pt --conf 0.25 --name yolo_road_det

# python detect.py --weights best.pt --source test.mp4 --view-img --name test02 --device cpu --save-conf
#            data='yolov5/data/test_data.yaml',
#            line_thickness=1,

#'--weights', nargs='+', type=str, default='yolov7.pt', help='model.pt path(s)'
#'--source', type=str, default='inference/images', help='source')  # file/folder, 0 for webcam
#'--img-size', type=int, default=640, help='inference size (pixels)')
#'--conf-thres', type=float, default=0.25, help='object confidence threshold')
#'--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')
#'--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
#'--view-img', action='store_true', help='display results')
#'--save-txt', action='store_true', help='save results to *.txt')
#'--save-conf', action='store_true', help='save confidences in --save-txt labels')
#'--nosave', action='store_true', help='do not save images/videos')
#'--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
#'--agnostic-nms', action='store_true', help='class-agnostic NMS')
#'--augment', action='store_true', help='augmented inference')
#'--update', action='store_true', help='update all models')
#'--project', default='runs/detect', help='save results to project/name')
#'--name', default='exp', help='save results to project/name')
#'--exist-ok', action='store_true', help='existing project/name ok, do not increment')
#'--no-trace', action='store_true', help='don`t trace model')

# python detect.py --source test.mp4 --view-img --device cpu --conf 0.25

# python detect.py --weights runs/train/road_det/weights/best.pt --source test.mp4 --view-img --name road_det --device cpu --save-conf
