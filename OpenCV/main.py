import cv2

def rescale_frame(frame_input, percent=50):
    width = int(frame_input.shape[1] * percent / 100)
    height = int(frame_input.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame_input, dim, interpolation=cv2.INTER_AREA)

cap = cv2.VideoCapture('./OpenCV/test.mp4')

while not cap.isOpened():
    cap = cv2.VideoCapture("./OpenCV/test.mp4")
    cv2.waitKey(1000)
    print(f"Wait for the header")

pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
while True:
    flag, frame = cap.read()
    if flag:
        rescaled_frame = rescale_frame(frame)
        # The frame is ready and already captured
        cv2.imshow('video', rescaled_frame)
        pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        print(f"{str(pos_frame)} frames")
    else:
        # The next frame is not ready, so we try to read it again
        cap.set(cv2.CAP_PROP_POS_FRAMES, pos_frame-1)
        print(f"frame is not ready")
        # It is better to wait for a while for the next frame to be ready
        cv2.waitKey(1000)

    if cv2.waitKey(10) == 27:
        break
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        # If the number of captured frames is equal to the total number of frames,
        # we stop
        break