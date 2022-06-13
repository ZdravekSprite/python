import cv2

cap = cv2.VideoCapture('OpenCV/test.mp4');
#get frame_number for saving, and save the frame
def getFrame(sec): 
    cap.set(cv2.CAP_PROP_POS_MSEC,sec*1000) 
    #cap.set(cv2.CAP_PROP_POS_FRAMES,frame_no);
    hasFrames,image = cap.read() 
    if hasFrames: 
        cv2.imwrite("OpenCV/test/"+str(sec)+".png", image)     # save frame as JPG file 
    return hasFrames 

sec = 0 
frameRate = 1 #it will capture image in each 1 second 
success = getFrame(sec) 
while success: 
    sec = sec + frameRate 
    sec = round(sec, 2) 
    success = getFrame(sec)