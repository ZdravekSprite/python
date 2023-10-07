import cv2
import numpy as np
import os
import argparse

from ultralytics import YOLO
import supervision as sv
from typing import List, Optional, Union

import cv2
import numpy as np

from supervision.detection.core import Detections
from supervision.draw.color import Color, ColorPalette

np.random.seed(20)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument("--webcam-resolution", default=[1280, 720], nargs=2, type=int)
    args = parser.parse_args()
    return args


def saveBox(box, name, frame):
    imagesPath = "../datasets/test/"
    dirpath, dirnames, filenames = next(os.walk(imagesPath), (None, [], []))
    cv2.imwrite(
        imagesPath + name + "_" + str(frame) + "_" + str(len(filenames)) + ".png", box
    )


def main():
    cap = cv2.VideoCapture("datasets/test.mp4")

    modelPath = "training/traffic_signs/weights/best.pt"

    framecount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    resolution = (width, height)

    info = {
        "framecount": framecount,
        "fps": cap.get(cv2.CAP_PROP_FPS),
        "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "codec": int(cap.get(cv2.CAP_PROP_FOURCC)),
    }
    print(info)

    model = YOLO(modelPath)

    frameNo = 0

    color = ColorPalette.default()
    thickness = 1
    text_scale = 0.5
    text_thickness = 1
    text_padding = 10
    text_color = Color.black()
    font = cv2.FONT_HERSHEY_SIMPLEX

    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            frameNo += 1
            result = model.track(frame, agnostic_nms=True)[0]
            detections = sv.Detections.from_ultralytics(result)

            if len(detections.confidence) != 0:
                labels = [
                    f"{model.model.names[class_id]} {confidence:0.2f}"
                    for _, _, confidence, class_id, _ in detections
                ]
                """
                frame = box_annotator.annotate(
                    scene=frame, 
                    detections=detections, 
                    labels=labels
                )
                """
                for i in range(len(detections)):
                    skip_label = detections.confidence[i] < 0.5
                    if skip_label:
                        continue

                    x1, y1, x2, y2 = detections.xyxy[i].astype(int)
                    class_id = (
                        detections.class_id[i]
                        if detections.class_id is not None
                        else None
                    )
                    idx = class_id if class_id is not None else i
                    color = (
                        color.by_idx(idx) if isinstance(color, ColorPalette) else color
                    )
                    cv2.rectangle(
                        img=frame,
                        pt1=(x1, y1),
                        pt2=(x2, y2),
                        color=color.as_bgr(),
                        thickness=thickness,
                    )

                    text = (
                        f"{model.model.names[class_id]} {detections.confidence[i]:0.2f}"
                    )

                    text_width, text_height = cv2.getTextSize(
                        text=text,
                        fontFace=font,
                        fontScale=text_scale,
                        thickness=text_thickness,
                    )[0]

                    text_x = x1 + text_padding
                    text_y = y1 - text_padding

                    text_background_x1 = x1
                    text_background_y1 = y1 - 2 * text_padding - text_height

                    text_background_x2 = x1 + 2 * text_padding + text_width
                    text_background_y2 = y1

                    cv2.rectangle(
                        img=frame,
                        pt1=(text_background_x1, text_background_y1),
                        pt2=(text_background_x2, text_background_y2),
                        color=color.as_bgr(),
                        thickness=cv2.FILLED,
                    )
                    cv2.putText(
                        img=frame,
                        text=text,
                        org=(text_x, text_y),
                        fontFace=font,
                        fontScale=text_scale,
                        color=text_color.as_rgb(),
                        thickness=text_thickness,
                        lineType=cv2.LINE_AA,
                    )

            cv2.imshow("yolov8", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if cv2.waitKey(30) == 27:
                break


if __name__ == "__main__":
    main()
