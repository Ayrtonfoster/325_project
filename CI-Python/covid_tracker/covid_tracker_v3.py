import numpy as np
import cv2
import math


#input_feed = cv2.VideoCapture(0)
camOn = True

# file references
yolo_config = "network_files/yolov4-tiny.cfg"
yolo_names = "network_files/coco.names"
yolo_weights = "network_files/yolov4-tiny.weights"

min_thresh = 0.3
min_confidence = 0.7

ROOM_WIDTH = 3.3 # in meters
ROOM_HEIGHT = 3.3 # in meters
MAX_PEOPLE = int(ROOM_HEIGHT/2) * int(ROOM_WIDTH/2)

# setup yolo and openCV network
# Load labels from .names fil
CATEGORIES = open(yolo_names).read().strip().split("\n")
# Generate a color for each classification
CATEGORIES_COLORS = np.random.randint(0,255,size=(len(CATEGORIES), 3), dtype="uint8")

# load YOLO object detector
YOLO_NET = cv2.dnn.readNetFromDarknet(yolo_config, yolo_weights)
# get reference to output layer of YOLO net
LAYER_NAMES = YOLO_NET.getLayerNames()
LAYER_NAMES = [LAYER_NAMES[i[0] - 1] for i in YOLO_NET.getUnconnectedOutLayers()]

ret, frame = input_feed.read()
(H, W) = frame.shape[:2]

black_screen = np.zeros((H,W))
black_screen = cv2.putText(black_screen, 'Disconnected', (int(H/2)-120 , int(W/2)-100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)


class VideoCamera(object):

    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def DoBoxesIntersect(x, y, w , h, x2, y2, w2, h2):
        return (abs((x + w/2) - (x2 + w2/2)) * 2 < (w + w2)) and (abs((y + h/2) - (y2 + h2/2)) * 2 < (h + h2))


    def frame_class_drawer(output_yolo, frame):
        boxes = []
        confidences = []
        classIDs = []
        num_people = 0

        #for output in output_yolo:
        output = output_yolo[0]
        for instance in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = instance[5:]
            classID = np.argmax(scores)
            #print(classID)
            confidence = scores[classID]
            #print(confidences)
            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > min_confidence:
                # scale the bounding box coordinates back relative to the
                # size of the image, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                box = instance[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                # use the center (x, y)-coordinates to derive the top and
                # and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                # update our list of bounding box coordinates, confidences,
                # and class IDs
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

        idxs = cv2.dnn.NMSBoxes(boxes, confidences, min_confidence, min_thresh)

        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                if(CATEGORIES[classIDs[i]]) == "person":
                    num_people = num_people + 1
                    # extract the bounding box coordinates
                    (x, y) = (boxes[i][0], boxes[i][1])
                    (w, h) = (boxes[i][2], boxes[i][3])

                    color = (0, 255, 0)

                    for j in idxs.flatten():
                        if(j != i):
                            (x2, y2) = (boxes[j][0], boxes[j][1])
                            (w2, h2) = (boxes[j][2], boxes[j][3])
                            overlap = DoBoxesIntersect(x, y, w , h, x2, y2, w2, h2)
                            # draw a bounding box rectangle and label on the image
                            if overlap:
                                color = (0,0,255)
                                break

                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    text = "person: " + str(num_people)
                    cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, color, 2)
        # Pulled from: https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/
        #ret, jpeg = cv2.imencode('.jpg', frame)
        
        
        return frame, num_people

        

    def get_frame():
            # success, image = self.video.read()
            # image=cv2.resize(image,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)
            # gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            # face_rects=face_cascade.detectMultiScale(gray,1.3,5)
            # for (x,y,w,h) in face_rects:
            # 	cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
            # 	break

        #while True:

        #while camOn:
        # Grab frame from camera feed
        ret, frame = input_feed.read()

        # Pre-process the image using openCV Blob
        pre_process = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)

        # Send pre-processed image through the network
        YOLO_NET.setInput(pre_process)
        output_yolo = YOLO_NET.forward(LAYER_NAMES)  # get results from network

        # send results for processing
        frame, people_count = frame_class_drawer(output_yolo, frame)
        if(people_count > MAX_PEOPLE):
            cv2.putText(frame, "Over Max Cap", (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)

        else:
            cv2.putText(frame, str(people_count), (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv2.LINE_AA)

        # Display the resulting frame
        #cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            camOn = not camOn
            cv2.imshow('Video', black_screen)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            camOn = not camOn

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
