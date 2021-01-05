import cv2
import numpy as np
import midi

# width 640 and height 480
foreground1 = np.ones((240, 320, 3), dtype='uint8') * 255
foreground2 = np.ones((240, 320, 3), dtype='uint8') * 175
foreground3 = np.ones((240, 320, 3), dtype='uint8') * 100
foreground4 = np.ones((240, 320, 3), dtype='uint8') * 25
# Open the camera
cap = cv2.VideoCapture(0)
# Set initial value of weights
alpha = 0.7
msize = 5
csize = 5
# variables
nodeOnUpperLeft = False
nodeOnUpperRight = False
nodeOnLowerLeft = False
nodeOnLowerRight = False

nodeOnUpperLeftHasChanged = False
nodeOnUpperRightHasChanged = False
nodeOnLowerLeftHasChanged = False
nodeOnLowerRightHasChanged = False

while True:
    # read the background
    ret, background = cap.read()
    background = cv2.flip(background, 1)

    ###########################################################################
    # hier kommt code
    # oben links
    imageslice1 = background[0:240, 0:320, :]
    mask1 = np.copy(imageslice1)
    # Erstellung einer Maske durch HSV-Farberkennung
    hsv = cv2.cvtColor(mask1, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    hslice = cv2.inRange(h, 50, 70)
    hslice = cv2.medianBlur(hslice, msize)
    sslice = cv2.inRange(s, 60, 120)
    sslice = cv2.medianBlur(sslice, msize)
    mask1 = cv2.bitwise_and(hslice, sslice)
    # Contour-Erkennung
    # Größte Contour berechnen. Falls groß genug -> trigger
    contours, hierarchy = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        contourLength = np.zeros(100, dtype=np.uint8)
        for index in range(len(contours)):
            contourLength[index] = cv2.contourArea(contours[index])
        maxlength = np.max(contourLength)
        if maxlength > csize:
            print('links oben')
            if not nodeOnUpperLeft:
                nodeOnUpperLeftHasChanged = True
            nodeOnUpperLeft = True
        else:
            nodeOnUpperLeft = False
    # links unten
    imageslice2 = background[240:480, 0:320, :]
    mask2 = np.copy(imageslice2)
    # Erstellung einer Maske durch HSV-Farberkennung
    hsv = cv2.cvtColor(mask2, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    hslice = cv2.inRange(h, 50, 70)
    hslice = cv2.medianBlur(hslice, msize)
    sslice = cv2.inRange(s, 60, 120)
    sslice = cv2.medianBlur(sslice, msize)
    mask2 = cv2.bitwise_and(hslice, sslice)
    # Contour-Erkennung
    # Größte Contour berechnen. Falls groß genug -> trigger
    contours, hierarchy = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        contourLength = np.zeros(100, dtype=np.uint8)
        for index in range(len(contours)):
            contourLength[index] = cv2.contourArea(contours[index])
        maxlength = np.max(contourLength)
        if maxlength > csize:
            print('links unten')
            if not nodeOnLowerLeft:
                nodeOnLowerLeftHasChanged = True
            nodeOnLowerLeft = True
        else:
            nodeOnLowerLeft = False
    # rechts oben
    imageslice3 = background[0:240, 320:640, :]
    mask3 = np.copy(imageslice3)
    # Erstellung einer Maske durch HSV-Farberkennung
    hsv = cv2.cvtColor(mask3, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    hslice = cv2.inRange(h, 50, 70)
    hslice = cv2.medianBlur(hslice, msize)
    sslice = cv2.inRange(s, 60, 120)
    sslice = cv2.medianBlur(sslice, msize)
    mask3 = cv2.bitwise_and(hslice, sslice)
    # Contour-Erkennung
    # Größte Contour berechnen. Falls groß genug -> trigger
    contours, hierarchy = cv2.findContours(mask3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        contourLength = np.zeros(100, dtype=np.uint8)
        for index in range(len(contours)):
            contourLength[index] = cv2.contourArea(contours[index])
        maxlength = np.max(contourLength)
        if maxlength > csize:
            print('rechts oben')
            if not nodeOnUpperRight:
                nodeOnUpperRightHasChanged = True
            nodeOnUpperRight = True
        else:
            nodeOnUpperRight = False
    # rechts unten
    imageslice4 = background[240:480, 320:640, :]
    mask4 = np.copy(imageslice4)
    # Erstellung einer Maske durch HSV-Farberkennung
    hsv = cv2.cvtColor(mask4, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    hslice = cv2.inRange(h, 50, 70)
    hslice = cv2.medianBlur(hslice, msize)
    sslice = cv2.inRange(s, 60, 120)
    sslice = cv2.medianBlur(sslice, msize)
    mask4 = cv2.bitwise_and(hslice, sslice)
    # Contour-Erkennung
    # Größte Contour berechnen. Falls groß genug -> trigger
    contours, hierarchy = cv2.findContours(mask4, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        contourLength = np.zeros(100, dtype=np.uint8)
        for index in range(len(contours)):
            contourLength[index] = cv2.contourArea(contours[index])
        maxlength = np.max(contourLength)
        if maxlength > csize:
            print('rechts unten')

            if not nodeOnLowerRight:
                nodeOnLowerRightHasChanged = True
            nodeOnLowerRight = True
        else:
            nodeOnLowerRight = False
    #######################################################################
    # Select the region in the background where we want to add the image and add the images using cv2.addWeighted()
    added_image1 = cv2.addWeighted(background[0:240, 0:320, :], alpha, foreground1[0:240, 0:320, :], 1 - alpha, 0)
    added_image2 = cv2.addWeighted(background[240:480, 0:320, :], alpha, foreground2[0:240, 0:320, :], 1 - alpha, 0)
    added_image3 = cv2.addWeighted(background[0:240, 320:640, :], alpha, foreground3[0:240, 0:320, :], 1 - alpha, 0)
    added_image4 = cv2.addWeighted(background[240:480, 320:640, :], alpha, foreground4[0:240, 0:320, :], 1 - alpha, 0)
    # Change the region with the result
    background[0:240, 0:320] = added_image1
    background[240:480, 0:320] = added_image2
    background[0:240, 320:640] = added_image3
    background[240:480, 320:640] = added_image4

    if nodeOnUpperLeftHasChanged:
        midi.send_control_change(1)
        nodeOnUpperLeftHasChanged = False
    if nodeOnLowerLeftHasChanged:
        midi.send_control_change(2)
        nodeOnLowerLeftHasChanged = False
    if nodeOnUpperRightHasChanged:
        midi.send_control_change(3)
        nodeOnUpperRightHasChanged = False
    if nodeOnLowerRightHasChanged:
        midi.send_control_change(4)
        nodeOnLowerRightHasChanged = False

    cv2.imshow('Projekt', background)

    # cv2.imshow('Projekta', mask1)
    # cv2.imshow('Projektb', mask2)
    k = cv2.waitKey(10)
    # Press q to break
    if cv2.waitKey(25) != -1:
        break;
# Release the camera and destroy all windows
cap.release()
cv2.destroyAllWindows()
