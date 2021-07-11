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
first_now = datetime.now()  # 캠키자마자 찍히는 시간
first_now = first_now.second

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
root.title('화면')
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
button.grid(row=4, column=0)
def video_stream():
    global study_time, are_you_study, start_study_time, no_monitor_time
    global first_now, before_blink, blink_count
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
        label3.configure(text = str(study_time))

        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

        now = now_study_time.second # 현재 시간

        # 눈깜박임 횟수 세서 팝업창띄우기(15회미만이고 1분이 지났으면)
        if blink_count <= 15 and now == first_now:
            label1.configure(text = f"{blink_count}, 건조해!")
            blink_count = 0
        elif now == first_now:
            label1.configure(text = f"{blink_count}, 안 건조해!")
            blink_count = 0

        face_loc = gaze.face_coords()
        if face_loc != None:
            face_x, face_y = face_loc.center().x, face_loc.center().y
            if face_std_x == 0 and face_std_y == 0:
                label2.configure(text="안 고쳐도 될 듯?")
                pose_time = datetime.now()
                face_std_x = face_x
                face_std_y = face_y
            elif abs(face_std_x - face_x) > 100 or abs(face_std_y - face_y) > 50:
                label2.configure(text="안 고쳐도 될 듯?")
                pose_time = datetime.now()
                face_std_x = face_x
                face_std_y = face_y
            elif (now_study_time - pose_time) > timedelta(minutes=1):
                label2.configure(text="슬슬 자세를 고쳐")
            print((now_study_time - pose_time))
            cv2.putText(frame, "C", (face_loc.center().x, face_loc.center().y), cv2.FONT_HERSHEY_DUPLEX, 0.3, (147, 58, 31), 1)

            # cv2.imshow("Eye Dear", frame)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        label_cam.imgtk = imgtk
        label_cam.configure(image=imgtk)
        label_cam.after(1, video_stream)


video_stream()
root.mainloop()