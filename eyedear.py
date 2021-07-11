"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking
#from gaze_tracking import Eye
from datetime import datetime
from datetime import timedelta

#eye = Eye()
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

before_blink=False
blink_count=0
first_now=datetime.now()    #캠키자마자 찍히는 시간
first_now=first_now.second

start_study_time = datetime.now()
no_monitor_time = 0
study_time = timedelta(seconds=0)
are_you_study = False

while webcam.isOpened():
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
        if before_blink == True:
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
    #print(gaze.out_of_monitor())
    # if out_of_monitor False, no monitor time is not initialize
    # So if out_of_monitor False, your not watch monitor
    now_study_time = datetime.now()
    if are_you_study:
        study_time += (now_study_time - start_study_time)
    start_study_time = now_study_time

    print(f"study time : {study_time}")
    if not gaze.out_of_monitor():
        if no_monitor_time == 0:
            print("Your Study Right Now")
            no_monitor_time = datetime.now()
        elif (datetime.now() - no_monitor_time) > timedelta(seconds=10) and are_you_study:
            print("Your not Study!!!!")
            are_you_study = False
            study_time -= (datetime.now() - no_monitor_time)
    else:
        are_you_study = True
        no_monitor_time = 0


    before_blink=gaze.is_blinking()
    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    now = datetime.now()    #현재 시간
    now = now.second

    #눈깜박임 횟수 세서 팝업창띄우기(15회미만이고 1분이 지났으면)
    if blink_count <= 15 and now == first_now:
        print(blink_count, '건조해!')
        blink_count=0
    elif now == first_now:
        print(blink_count, '안 건조해!')
        blink_count=0

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("EyeDear", frame)

    if cv2.waitKey(1) == ord('q'):
        break
else:
    print("WebCam is not detected")
   
webcam.release()
cv2.destroyAllWindows()
