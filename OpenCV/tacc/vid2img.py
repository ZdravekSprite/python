import cv2
vidcap = cv2.VideoCapture('test.mp4')
count = 0

while vidcap.isOpened():
    ret, frame = vidcap.read()

    if ret:
        if (count % 15) == 2:
            cv2.imwrite(f"temp/frame{count:05d}.jpg", frame)     # save frame as JPEG file      
        cv2.imshow('Video to frames', frame)
        count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

vidcap.release()