import cv2
import numpy as np
import os

cap = cv2.VideoCapture('OpenCV/test.mp4')
modelPath = 'yolov5/runs/train/yolo_road_det/weights/best.onnx'
classesPath = os.path.join("OpenCV/test", "road_sign_data.txt")

# Constants.
INPUT_WIDTH = 640
INPUT_HEIGHT = 640
SCORE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.45
CONFIDENCE_THRESHOLD = 0.45 #0.45

# Text parameters.
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.7
THICKNESS = 1

# Colors.
BLACK  = (0,0,0)
BLUE   = (255,178,50)
YELLOW = (0,255,255)

def draw_label(im, label, x, y):
    """Draw text onto image at location."""
    # Get text size.
    text_size = cv2.getTextSize(label, FONT_FACE, FONT_SCALE, THICKNESS)
    dim, baseline = text_size[0], text_size[1]
    # Use text size to create a BLACK rectangle.
    cv2.rectangle(im, (x,y), (x + dim[0], y + dim[1] + baseline), (0,0,0), cv2.FILLED);
    # Display text inside the rectangle.
    cv2.putText(im, label, (x, y + dim[1]), FONT_FACE, FONT_SCALE, YELLOW, THICKNESS, cv2.LINE_AA)

def pre_process(input_image, net):
    # Create a 4D blob from a frame.
    blob = cv2.dnn.blobFromImage(input_image, 1/255,  (INPUT_WIDTH, INPUT_HEIGHT), [0,0,0], 1, crop=False)
 
    # Sets the input to the network.
    net.setInput(blob)
 
    # Run the forward pass to get output of the output layers.
    outputs = net.forward(net.getUnconnectedOutLayersNames())
    return outputs

def post_process(input_image, outputs):
      # Lists to hold respective values while unwrapping.
      class_ids = []
      confidences = []
      boxes = []
      # Rows.
      rows = outputs[0].shape[1]
      image_height, image_width = input_image.shape[:2]
      # Resizing factor.
      x_factor = image_width / INPUT_WIDTH
      y_factor =  image_height / INPUT_HEIGHT
      # Iterate through detections.
      for r in range(rows):
            row = outputs[0][0][r]
            confidence = row[4]
            # Discard bad detections and continue.
            if confidence >= CONFIDENCE_THRESHOLD:
                  classes_scores = row[5:]
                  # Get the index of max class score.
                  class_id = np.argmax(classes_scores)
                  #  Continue if the class score is above threshold.
                  if (classes_scores[class_id] > SCORE_THRESHOLD):
                        confidences.append(confidence)
                        class_ids.append(class_id)
                        cx, cy, w, h = row[0], row[1], row[2], row[3]
                        left = int((cx - w/2) * x_factor)
                        top = int((cy - h/2) * y_factor)
                        width = int(w * x_factor)
                        height = int(h * y_factor)
                        box = np.array([left, top, width, height])
                        boxes.append(box)
 # Perform non maximum suppression to eliminate redundant, overlapping boxes with lower confidences.
      indices = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
      for i in indices:
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]             
            # Draw bounding box.             
            cv2.rectangle(input_image, (left, top), (left + width, top + height), BLUE, 3*THICKNESS)
            # Class label.                      
            label = "{}:{:.2f}".format(classes[class_ids[i]], confidences[i])             
            # Draw label.             
            draw_label(input_image, label, left, top)
      return input_image

# Load class names.
classes = None
with open(classesPath, 'rt') as f: classes = f.read().rstrip('\n').split('\n')

net = cv2.dnn.readNet(modelPath)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

#print(net.getLayerNames())

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        # Process image.
        detections = pre_process(frame, net)
        img = post_process(frame.copy(), detections)
        t, _ = net.getPerfProfile()
        label = 'Inference time: %.2f ms' % (t * 1000.0 /  cv2.getTickFrequency())
        #print(label)
        height, width = frame.shape[:2]
        if width > 2000:
            height = int(height*2000/width)
            width = 2000
        dim =(width, height)
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        cv2.putText(resized, label, (20, 40), FONT_FACE, FONT_SCALE,  (0, 0, 255), THICKNESS, cv2.LINE_AA)
        cv2.imshow('Output', resized)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        ret, frame = cap.read()
cap.release()
cv2.destroyAllWindows()
