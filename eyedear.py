"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking
from datetime import datetime
from datetime import timedelta
from tkinter import *
from PIL import ImageTk, Image


# eye = Eye()
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

before_blink = False
blink_count = 0
count_blink_one_minute = datetime.now()
#first_now = datetime.now()  # 캠키자마자 찍히는 시간
#first_now = first_now.second

# count study time
start_study_time = datetime.now()  # check before study
no_monitor_time = 0  # if no monitor time is zero, the pupil is located.
study_time = timedelta(seconds=0)  # real study time
are_you_study = False  # check person study or not

# face coords
face_x = 0
face_y = 0
face_std_x = 0
face_std_y = 0

# stay pose
pose_time = datetime.now()


root = Tk()
root.title('Eye Dear')
root.geometry("+500+10")
label1 = Label(root, text="안구건조증", font= ('Helvetica 15 bold'))
label1.grid(row=0, column=0)

label2 = Label(root, text="자세교정", font= ('Helvetica 15 bold'))
label2.grid(row=1, column=0)

label3 = Label(root, text="공부시간", font= ('Helvetica 15 bold'))
label3.grid(row=2, column=0)
label_cam = Label(root)
label_cam.grid(row=3, column=0)

button = Button(root,text="quit", command=root.destroy, width=8, height=1)
button.grid(row=4, column=1)
def video_stream():
    global study_time, are_you_study, start_study_time, no_monitor_time
    global count_blink_one_minute, before_blink, blink_count
    global face_x, face_y, face_std_x, face_std_y, pose_time

    _, frame = webcam.read()
    if not _:
        print("WebCam is not detected")
    
    else:
        # We get a new frame from the webcam
        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        frame = gaze.annotated_frame()
        text = ""

        if gaze.is_blinking():
            text = "Blinking"
            if before_blink == False:
                blink_count += 1
                before_blink = True
        elif gaze.is_right():
            before_blink = False
            text = "Looking right"
        elif gaze.is_left():
            before_blink = False
            text = "Looking left"
        elif gaze.is_center():
            before_blink = False
            if gaze.is_up():
                text = "Looking upward"
            elif gaze.is_down():
                text = "Looking under"
            else:
                text = "Looking center"
        else:
            before_blink = False
        #print(gaze.out_of_monitor())
        # if out_of_monitor False, no monitor time is not initialize
        # So if out_of_monitor False, your not watch monitor
        now_study_time = datetime.now()
        if are_you_study:
            study_time += (now_study_time - start_study_time)
        start_study_time = now_study_time

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

        #label3 show study time
        study_time_second = study_time.total_seconds()
        study_hour = int(study_time_second / 3600)
        study_minute = int((study_time_second % 3600) / 60)
        study_second = int(study_time_second % 60)
        label3.configure(text = f"공부시간 : {study_hour}시간 {study_minute}분 {study_second}초")

        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

        # now = now_study_time.second # 현재 시간

        # 눈깜박임 횟수 세서 팝업창띄우기(15회미만이고 1분이 지났으면)
        if (now_study_time - count_blink_one_minute) > timedelta(seconds=60):
            count_blink_one_minute = datetime.now()
            if blink_count <= 15:
                label1.configure(text = f"1분동안 눈을 깜빡인 횟수 : {blink_count}, 건조해!")
                blink_count = 0
            else:
                label1.configure(text = f"1분동안 눈을 깜빡인 횟수 : {blink_count}, 안 건조해!")
                blink_count = 0

        face_loc = gaze.face_coords()
        if face_loc != None:
            face_x, face_y = face_loc.center().x, face_loc.center().y
            if face_std_x == 0 and face_std_y == 0:
                label2.configure(text="자세를 고치지 않아도 됩니다. 1분 뒤에 봬요~")
                pose_time = datetime.now()
                face_std_x = face_x
                face_std_y = face_y
            elif abs(face_std_x - face_x) > 100 or abs(face_std_y - face_y) > 50:
                label2.configure(text="자세를 고치지 않아도 됩니다. 1분 뒤에 봬요~")
                pose_time = datetime.now()
                face_std_x = face_x
                face_std_y = face_y
            elif (now_study_time - pose_time) > timedelta(minutes=1):
                label2.configure(text="슬슬 자세를 고치세요.")
            #print((now_study_time - pose_time))
            cv2.putText(frame, "C", (face_loc.center().x, face_loc.center().y), cv2.FONT_HERSHEY_DUPLEX, 0.3, (147, 58, 31), 1)

            # cv2.imshow("Eye Dear", frame)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        label_cam.imgtk = imgtk
        label_cam.configure(image=imgtk)
        label_cam.after(1, video_stream)

def setup():
    setCount = 0
    setThreshold = 0

    direction = ["left", "right", "upward", "under"]
    direction_key = ["A", "S", "D", "F"]
    direction_index = 0

    thresholdFile = open("gaze_tracking/threshold.txt", 'w')

    while webcam.isOpened():
        _, frame2 = webcam.read()
        gaze.refresh(frame2)
        frame2 = gaze.annotated_frame()

        text = "Please turn your eyes to the " + direction[direction_index]
        text_push = "Push Button " + direction_key[direction_index] + " To SetUp Your Threshold!!"

        cv2.putText(frame2, text, (20, 60), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 2)
        cv2.putText(frame2, text_push, (20, 130), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
        cv2.imshow("SetUp", frame2)

        #left
        if cv2.waitKey(1) == ord('a') and direction_index == 0:
            print(setThreshold, direction_index, setCount)
            if setCount > 10:
                direction_index += 1
                thresholdFile.write(str(setThreshold / setCount) + "\n")
                setCount = 0
                setThreshold = 0
            if gaze.pupils_located:
                setThreshold += gaze.horizontal_ratio()
                setCount += 1
        #right
        elif cv2.waitKey(1) == ord('s') and direction_index == 1:
            print(setThreshold, direction_index, setCount)
            if setCount > 10:
                direction_index += 1
                thresholdFile.write(str(setThreshold / setCount) + "\n")
                setCount = 0
                setThreshold = 0
            if gaze.pupils_located:
                setThreshold += gaze.horizontal_ratio()
                setCount += 1
        #upward
        elif cv2.waitKey(1) == ord('d') and direction_index == 2:
            print(setThreshold, direction_index, setCount)
            if setCount > 10:
                direction_index += 1
                thresholdFile.write(str(setThreshold / setCount) + "\n")
                setCount = 0
                setThreshold = 0
            if gaze.pupils_located:
                setThreshold += gaze.vertical_ratio()
                setCount += 1
        #under
        elif cv2.waitKey(1) == ord('f') and direction_index == 3:
            print(setThreshold, direction_index, setCount)
            if setCount > 10:
                direction_index += 1
                thresholdFile.write(str(setThreshold / setCount) + "\n")
                setCount = 0
                setThreshold = 0
            if gaze.pupils_located:
                setThreshold += gaze.vertical_ratio()
                setCount += 1


        if direction_index > 3 :
            break

        if cv2.waitKey(1) == ord('q'):
            break
    
    cv2.destroyWindow("SetUp")

def onClick():
    setup()
setup_btn = Button(root, text="setup", command=onClick)
setup_btn.grid(row=4, column=0)
video_stream()
root.mainloop()