import cv2
from time import time

vidcap = cv2.VideoCapture('test.mp4')
count = 0

loop_time = time()

while vidcap.isOpened():
    ret, frame = vidcap.read()

    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    if ret:
        if (count % 20) == 3:
            cv2.imwrite(f"temp/frame{count:05d}.jpg", frame)     # save frame as JPEG file      
        cv2.imshow('Video to frames', frame)
        count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

vidcap.release()