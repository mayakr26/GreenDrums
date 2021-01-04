import numpy as np
import cv2

def do_nothing(e):
    return

cap = cv2.VideoCapture(0)

while cap.isOpened():

    ret, frame = cap.read()
    crashImg = cv2.imread('images/crash.png')
    # sum = cv2.add(frame, crashImg)
    frame = cv2.line(frame,(0,360),(320,360),(0,0,0),3)
    frame = cv2.line(frame,(480,720),(480,480),(0,0,0),3)
    frame = cv2.line(frame,(640,360),(960,360),(0,0,0),3)
    frame = cv2.line(frame,(480,0),(480,240),(0,0,0),3)
    frame = cv2.line(frame,(320,240),(320,480),(0,0,0),3)
    frame = cv2.line(frame,(320,480),(640,480),(0,0,0),3)
    frame = cv2.line(frame,(640,480),(640,240),(0,0,0),3)
    frame = cv2.line(frame,(640,240),(320,240),(0,0,0),3)



    cv2.imshow('Green Drums', frame)


    if cv2.waitKey(25) != -1:
        break

cap.release()
cv2.destroyAllWindows()