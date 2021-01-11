import cv2
import numpy as np
import midi


# Open the camera
cap = cv2.VideoCapture(0)

# Get camera width and height
cameraWidth = int(round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
cameraHeight = int(round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

cameraWidthHalf = int(round(cameraWidth)) // 2
cameraWidthThird = int(round(cameraWidth)) // 3
cameraWidthSixth = int(round(cameraWidth)) // 6

cameraHeightHalf = int(round(cameraHeight)) // 2
cameraHeightThird = int(round(cameraHeight)) // 3
cameraHeightSixth = int(round(cameraHeight)) // 6

foreground1 = np.ones((cameraHeight, cameraWidth, 3), dtype='uint8') * 255
foreground2 = np.ones((cameraHeight, cameraWidth, 3), dtype='uint8') * 175
foreground3 = np.ones((cameraHeight, cameraWidth, 3), dtype='uint8') * 100
foreground4 = np.ones((cameraHeight, cameraWidth, 3), dtype='uint8') * 70

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


def createMask(imageslice):
    mask = np.copy(imageslice)

    # Erstellung einer Maske durch HSV-Farberkennung
    hsv = cv2.cvtColor(mask, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    hslice = cv2.inRange(h, 50, 70)
    hslice = cv2.medianBlur(hslice, msize)
    sslice = cv2.inRange(s, 60, 120)
    sslice = cv2.medianBlur(sslice, msize)
    mask = cv2.bitwise_and(hslice, sslice)
    return mask

            
while True:
    # read the background
    ret, background = cap.read()
    background = cv2.flip(background, 1)
    
    # Wird in jedem Fall ausgeführt. Dient nur dazu, den Code einklappen zu können.
    if True:
        # oben links
        imageslice1 = background[0:cameraHeightHalf, 0:cameraWidthThird, :]
        mask1 = createMask(imageslice1)

        #oben links 2
        imageslice5 = background[0:cameraHeightThird, 0:cameraWidthThird+cameraWidthSixth, :]
        mask5 = createMask(imageslice5)

        contours, hierarchy = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            contourLength = np.zeros(100, dtype=np.uint8)
            for index in range(len(contours)):
                contourLength[index] = cv2.contourArea(contours[index])
            maxlength = np.max(contourLength)
            if maxlength > csize:

                if not nodeOnUpperLeft:
                    print('links oben')
                    nodeOnUpperLeftHasChanged = True
                nodeOnUpperLeft = True
            else:
                nodeOnUpperLeft = False

        contours, hierarchy = cv2.findContours(mask5, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            contourLength = np.zeros(100, dtype=np.uint8)
            for index in range(len(contours)):
                contourLength[index] = cv2.contourArea(contours[index])
            maxlength = np.max(contourLength)
            if maxlength > csize:

                if not nodeOnUpperLeft:
                    print('links oben')
                    nodeOnUpperLeftHasChanged = True
                nodeOnUpperLeft = True
            else:
                nodeOnUpperLeft = False

        # unten links
        imageslice2 = background[cameraHeightHalf:cameraHeight, 0:cameraWidthThird, :]
        mask2 = createMask(imageslice2)

        # unten links 2
        imageslice6 = background[cameraHeightHalf + cameraHeightSixth:cameraHeight, cameraWidthThird:cameraWidthHalf, :]
        mask6 = createMask(imageslice6)

        contours, hierarchy = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            contourLength = np.zeros(100, dtype=np.uint8)
            for index in range(len(contours)):
                contourLength[index] = cv2.contourArea(contours[index])
            maxlength = np.max(contourLength)
            if maxlength > csize:

                if not nodeOnLowerLeft:
                    print('links unten')
                    nodeOnLowerLeftHasChanged = True
                nodeOnLowerLeft = True
            else:
                nodeOnLowerLeft = False

        contours, hierarchy = cv2.findContours(mask6, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            contourLength = np.zeros(100, dtype=np.uint8)
            for index in range(len(contours)):
                contourLength[index] = cv2.contourArea(contours[index])
            maxlength = np.max(contourLength)
            if maxlength > csize:

                if not nodeOnLowerLeft:
                    print('links unten')
                    nodeOnLowerLeftHasChanged = True
                nodeOnLowerLeft = True
            else:
                nodeOnLowerLeft = False

        # rechts oben
        imageslice3 = background[0:cameraHeightHalf, cameraWidthHalf+cameraWidthSixth:cameraWidth, :]
        mask3 = createMask(imageslice3)

        # rechts oben 2
        imageslice7 = background[0:cameraHeightThird, cameraWidthHalf:cameraWidthHalf+cameraWidthSixth, :]
        mask7 = createMask(imageslice7)

        contours, hierarchy = cv2.findContours(mask3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            contourLength = np.zeros(100, dtype=np.uint8)
            for index in range(len(contours)):
                contourLength[index] = cv2.contourArea(contours[index])
            maxlength = np.max(contourLength)
            if maxlength > csize:

                if not nodeOnUpperRight:
                    print('rechts oben')
                    nodeOnUpperRightHasChanged = True
                nodeOnUpperRight = True
            else:
                nodeOnUpperRight = False

        contours, hierarchy = cv2.findContours(mask7, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            contourLength = np.zeros(100, dtype=np.uint8)
            for index in range(len(contours)):
                contourLength[index] = cv2.contourArea(contours[index])
            maxlength = np.max(contourLength)
            if maxlength > csize:

                if not nodeOnUpperRight:
                    print('rechts oben')
                    nodeOnUpperRightHasChanged = True
                nodeOnUpperRight = True
            else:
                nodeOnUpperRight = False

        # rechts unten
        imageslice4 = background[cameraHeightHalf:cameraHeight, cameraWidthHalf+cameraWidthSixth:cameraWidth, :]
        mask4 = createMask(imageslice4)

        # rechts unten 2
        imageslice8 = background[cameraHeightHalf+cameraHeightSixth:cameraHeight, cameraWidthHalf:cameraWidthHalf+cameraWidthSixth, :]
        mask8 = createMask(imageslice8)

        contours, hierarchy = cv2.findContours(mask4, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            contourLength = np.zeros(100, dtype=np.uint8)
            for index in range(len(contours)):
                contourLength[index] = cv2.contourArea(contours[index])
            maxlength = np.max(contourLength)
            if maxlength > csize:
                if not nodeOnLowerRight:
                    print('rechts unten')
                    nodeOnLowerRightHasChanged = True
                nodeOnLowerRight = True
            else:
                nodeOnLowerRight = False

        contours, hierarchy = cv2.findContours(mask8, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            contourLength = np.zeros(100, dtype=np.uint8)
            for index in range(len(contours)):
                contourLength[index] = cv2.contourArea(contours[index])
            maxlength = np.max(contourLength)
            if maxlength > csize:
                if not nodeOnLowerRight:
                    print('rechts unten')
                    nodeOnLowerRightHasChanged = True
                nodeOnLowerRight = True
            else:
                nodeOnLowerRight = False

    # Select the region in the background where we want to add the image and add the images using cv2.addWeighted()

    # oben links
    added_image1 = cv2.addWeighted(imageslice1, alpha, foreground1[0:cameraHeightHalf, 0:cameraWidthThird, :], 1 - alpha, 0)
    added_image5 = cv2.addWeighted(imageslice5, alpha, foreground1[0:cameraHeightThird, 0:cameraWidthThird+cameraWidthSixth, :], 1 - alpha, 0)

    # unten links
    added_image2 = cv2.addWeighted(imageslice2, alpha, foreground2[cameraHeightHalf:cameraHeight, 0:cameraWidthThird, :], 1 - alpha, 0)
    added_image6 = cv2.addWeighted(imageslice6, alpha, foreground2[cameraHeightHalf + cameraHeightSixth:cameraHeight, cameraWidthThird:cameraWidthHalf, :], 1 - alpha, 0)

    # oben rechts
    added_image3 = cv2.addWeighted(imageslice3, alpha, foreground3[0:cameraHeightHalf, cameraWidthHalf+cameraWidthSixth:cameraWidth, ], 1 - alpha, 0)
    added_image7 = cv2.addWeighted(imageslice7, alpha, foreground3[0:cameraHeightThird, cameraWidthHalf:cameraWidthHalf+cameraWidthSixth, :], 1 - alpha, 0)

    # unten rechts
    added_image4 = cv2.addWeighted(imageslice4, alpha, foreground4[cameraHeightHalf:cameraHeight, cameraWidthHalf+cameraWidthSixth:cameraWidth, :], 1 - alpha, 0)
    added_image8 = cv2.addWeighted(imageslice8, alpha, foreground4[cameraHeightHalf+cameraHeightSixth:cameraHeight, cameraWidthHalf:cameraWidthHalf+cameraWidthSixth, :], 1 - alpha, 0)
    

    # Change the region with the result
    background[0:cameraHeightHalf, 0:cameraWidthThird] = added_image1
    background[0:cameraHeightThird, 0:cameraWidthThird+cameraWidthSixth] = added_image5

    background[cameraHeightHalf:cameraHeight, 0:cameraWidthThird] = added_image2
    background[cameraHeightHalf + cameraHeightSixth:cameraHeight, cameraWidthThird:cameraWidthHalf, :] = added_image6

    background[0:cameraHeightHalf, cameraWidthHalf+cameraWidthSixth:cameraWidth] = added_image3
    background[0:cameraHeightThird, cameraWidthHalf:cameraWidthHalf+cameraWidthSixth, :] = added_image7

    background[cameraHeightHalf:cameraHeight, cameraWidthHalf+cameraWidthSixth:cameraWidth] = added_image4
    background[cameraHeightHalf+cameraHeightSixth:cameraHeight, cameraWidthHalf:cameraWidthHalf+cameraWidthSixth] = added_image8


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