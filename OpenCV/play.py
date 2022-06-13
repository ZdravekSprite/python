import cv2
import numpy as np

cap = cv2.VideoCapture('OpenCV/test.mp4')
#width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


while cap.isOpened():
    ret, frame = cap.read()
    image_np = np.array(frame)

    if ret:
        #cv2.imshow('object detection', cv2.resize(image_np, (960, 540)))
        cv2.imshow('play', image_np)

        if cv2.waitKey(240) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
