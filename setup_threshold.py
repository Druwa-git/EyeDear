"""
This Python Program Set Up Your Pupil direction Threshold.
Pupil Threshold save in text file.
"""

import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
setCount = 0
setThreshold = 0

direction = ["left", "right", "upward", "under"]
direction_key = ["A", "S", "D", "F"]
direction_index = 0

thresholdFile = open("threshold.txt", 'w')

while webcam.isOpened():
    _, frame = webcam.read()
    gaze.refresh(frame)
    frame = gaze.annotated_frame()

    text = "Please turn your eyes to the " + direction[direction_index]
    text_push = "Push Button " + direction_key[direction_index] + " To SetUp Your Threshold!!"

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
    cv2.putText(frame, text_push, (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.imshow("SetUp", frame)

    #left
    if cv2.waitKey(1) == ord('a') and direction_index == 0:
        print(setThreshold)
        if setCount == 10:
            direction_index += 1
            setCount = 0
            thresholdFile.write(str(setThreshold / 100) + "\n")
            setThreshold = 0
        if gaze.pupils_located:
            setThreshold += gaze.horizontal_ratio()
            setCount += 1
    #right
    elif cv2.waitKey(1) == ord('s') and direction_index == 1:
        if setCount == 10:
            direction_index += 1
            setCount = 0
            thresholdFile.write(setThreshold / 100)
            thresholdFile.write("\n")
            setThreshold = 0
        if gaze.pupils_located:
            setThreshold += gaze.horizontal_ratio()
            setCount += 1
    #upward
    elif cv2.waitKey(1) == ord('d') and direction_index == 2:
        if setCount == 10:
            direction_index += 1
            setCount = 0
            thresholdFile.write(setThreshold / 100)
            thresholdFile.write("\n")
            setThreshold = 0
        if gaze.pupils_located:
            setThreshold += gaze.vertical_ratio()
            setCount += 1
    #under
    elif cv2.waitKey(1) == ord('f') and direction_index == 3:
        if setCount == 10:
            direction_index += 1
            setCount = 0
            thresholdFile.write(setThreshold / 100)
            thresholdFile.write("\n")
            setThreshold = 0
        if gaze.pupils_located:
            setThreshold += gaze.vertical_ratio()
            setCount += 1


    if direction_index > 3 :
        break

    if cv2.waitKey(1) == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()
thresholdFile.close()