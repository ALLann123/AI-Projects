#!/usr/bin/python3
import threading
import winsound
import cv2
import imutils

#---We are building a motion detection Alarm System in python

#select the camera
cap=cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#get the differences to detect motion 
#Get a value from the camera
_, start_frame=cap.read()

start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

#inthe begin the alarm is turned off
alarm=False
alarm_mode=False
#how long do we want to have movements for the alarm to be called
alarm_counter=0

#this function consists of actions we want to occure when motion is detected
"""
Actions :
1.can be add a voice agent thats triggered and calls you immediately
2.Upload current video stream to FTP server
3.Send an email to me immediately
4. Turn on/off some systems
5. Lock somethings or make a loud sound alarm
"""
def beep_alarm():
    global alarm
    #call the function in alarm mode, and press T to cancel alarm
    for _ in range(5):
        if not alarm_mode:
            break
        print("ALARM")
        winsound.Beep(2500, 1000)
    alarm=False


while True:
    _, frame = cap.read()
    frame = imutils.resize(frame, width=500)

    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        #calculate the difference between the difference to identify the motions between the frames
        difference=cv2.absdiff(frame_bw, start_frame)

        #have all sorts of gray pixels, we want to have 256
        threshold=cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]

        #set the start frame after alteration to the current frame
        start_frame=frame_bw

        #these controls the sensitivity of the alarm i.e 1 is more sensitive and 1000 is less sensitive to trigger the alarm
        if threshold.sum() > 1000:
            alarm_counter+=1
        else:
            if alarm_counter > 0:
                alarm_counter-=1

        cv2.imshow("Cam", threshold)

    else:
        #show the camera
        cv2.imshow("Cam", frame)

    if alarm_counter > 20:
        if not alarm:
            alarm=True
            threading.Thread(target=beep_alarm).start()

    
    key_pressed=cv2.waitKey(30)
    if key_pressed == ord("t"):
        alarm_mode=not alarm_mode
        alarm_counter=0

    if key_pressed==ord("q"):
        alarm_mode=False
        break

cap.release()
cv2.destroyAllWindows()

