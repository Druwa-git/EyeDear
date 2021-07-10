"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking
from gaze_tracking import Eye
from datetime import datetime

eye = Eye()
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

before_blink=False
blink_count=0
first_now=datetime.now()    #캠키자마자 찍히는 시간
first_now=first_now.second
while webcam.isOpened():
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
        if before_blink==True:
            continue
        else:
            blink_count += 1
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        if gaze.is_up():
            text = "Looking upward"
        elif gaze.is_down():
            text = "Looking under"
        else:
            text = "Looking center"
    before_blink=eye.pupil()
    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    now = datetime.now()    #현재 시간
    now = now.second
    #눈깜박임 횟수 세서 팝업창띄우기(15회미만이고 1분이 지났으면)
    if blink_count<=15 and now==first_now:
        popup

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == ord('q'):
        break
   
webcam.release()
cv2.destroyAllWindows()
