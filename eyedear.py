"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

while webcam.isOpened():
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""
    
    if gaze.is_blinking():
        text = "Blinking"
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

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    face_loc = gaze.face_coords()
    if face_loc == None:
        continue

    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    try:
        cv2.putText(frame, "right_top: " , (face_loc.right(), face_loc.top()), cv2.FONT_HERSHEY_DUPLEX, 0.3, (147, 58, 31), 1)
        cv2.putText(frame, "right_bottom: " , (face_loc.right(), face_loc.bottom()), cv2.FONT_HERSHEY_DUPLEX, 0.3, (147, 58, 31), 1)
        cv2.putText(frame, "left_bottom: " , (face_loc.left(), face_loc.bottom()), cv2.FONT_HERSHEY_DUPLEX, 0.3, (147, 58, 31), 1)
        cv2.putText(frame, "left_top: " , (face_loc.left(), face_loc.top()), cv2.FONT_HERSHEY_DUPLEX, 0.3, (147, 58, 31), 1)
    except:
        pass

    



    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == ord('q'):
        break
   
webcam.release()
cv2.destroyAllWindows()