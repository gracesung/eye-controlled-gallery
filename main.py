import os
import sys
import numpy as np
import cv2
import dlib 
from math import hypot


def calc_EAR(eye_pts, landmarks):
    # get lengths of horizontal and verticals to determine eye aspect ratio (EAR)
    h_len = hypot(landmarks.part(eye_pts[0]).x - landmarks.part(eye_pts[3]).x, landmarks.part(eye_pts[0]).y - landmarks.part(eye_pts[3]).y)
    v_len1 = hypot(landmarks.part(eye_pts[1]).x - landmarks.part(eye_pts[5]).x, landmarks.part(eye_pts[1]).y - landmarks.part(eye_pts[5]).y)
    v_len2 = hypot(landmarks.part(eye_pts[2]).x - landmarks.part(eye_pts[4]).x, landmarks.part(eye_pts[2]).y - landmarks.part(eye_pts[4]).y)
    
    ratio = (v_len1 + v_len2) / (2 * h_len) # this is the EAR formula
    
    return ratio

VERBOSE = False

# check for verbose mode
if (len(sys.argv)) == 2:
    if (sys.argv[1] == "--verbose" or sys.argv[1] == "-v"):
        print("Verbose mode enabled")
        VERBOSE = True
    else:
        print("Invalid argument. Use 'verbose' or '-v' to enable verbose mode.")
        sys.exit(1)
if (len(sys.argv)) > 2:
    print("Too many arguments. Use 'verbose' or '-v' to enable verbose mode.")
    sys.exit(1)

# set up image gallery
image_paths = []
cur_image_idx = 0
# set up image paths
for imgs in os.listdir('./images/'):
    # ensure file is image
    if (imgs.endswith(".png") or imgs.endswith(".jpg") or imgs.endswith(".jpeg")):
        image_paths.append(os.path.join('./images/', imgs))
    if VERBOSE:
        print(image_paths)
SIZE = (1200, 700) # initial size of gallery window

cv2.namedWindow("gallery", cv2.WINDOW_NORMAL)
cv2.resizeWindow("gallery", SIZE[0], SIZE[1])
# initial gallery image
display = cv2.imread(image_paths[0])

cap = cv2.VideoCapture(0) 
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('./assets/shape_predictor_68_face_landmarks.dat') # dat file taken from dlib

# these are the points for the left and right eye (can reference png file in assets)
USER_RIGHT_EYE = [36, 37, 38, 39, 40, 41]
USER_LEFT_EYE = [42, 43, 44, 45, 46, 47]

EAR_THRESHOLD = 0.2 # if EAR is below this, we can assume eye is closed
FRAME_THRESHOLD = 6 # number of consecutive frames for closed eyes to register 
blink_frame_count = 0 # track number of frames since blink started

while True: 
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)

        # map landmarks (for verbose mode)
        for n in range(0, 68):
            x = landmarks.part(n).x 
            y = landmarks.part(n).y
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        left_ear = calc_EAR(USER_LEFT_EYE, landmarks)
        right_ear = calc_EAR(USER_RIGHT_EYE, landmarks)
        avg = (left_ear + right_ear) / 2
        if avg < EAR_THRESHOLD:
            # eyes are closed
            blink_frame_count += 1
            cv2.putText(frame, "eyes closed", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            if blink_frame_count >= FRAME_THRESHOLD:
                # eyes opened from a blink long enough to register
                cv2.putText(frame, "blink open", (60, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                # switch image
                if cur_image_idx < len(image_paths) - 1:
                    cur_image_idx += 1
                else:
                    cur_image_idx = 0
                display = cv2.imread(image_paths[cur_image_idx]) 
            # reset blink frame count  
            blink_frame_count = 0

        if VERBOSE:
            print("blink frame count: " + str(blink_frame_count) + "    avg: " + str(avg))   
    
    cv2.imshow("gallery", display) # rotating image gallery

    if VERBOSE:
        cv2.imshow('camera', frame) # camera feed

    # exit on 'q' key press
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()