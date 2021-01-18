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
cameraWidthEighth = int(round(cameraWidth)) // 8

cameraHeightHalf = int(round(cameraHeight)) // 2
cameraHeightThird = int(round(cameraHeight)) // 3
cameraHeightSixth = int(round(cameraHeight)) // 6
cameraHeightEighth = int(round(cameraHeight)) // 8

foreground1 = np.ones((cameraHeight, cameraWidth, 3), dtype='uint8') * 255
foreground2 = np.ones((cameraHeight, cameraWidth, 3), dtype='uint8') * 175
foreground3 = np.ones((cameraHeight, cameraWidth, 3), dtype='uint8') * 100
foreground4 = np.ones((cameraHeight, cameraWidth, 3), dtype='uint8') * 70

crash_image = cv2.imread('images/crash.png', cv2.IMREAD_COLOR)
hihat_image = cv2.imread('images/hihat.png', cv2.IMREAD_COLOR)
bassdrum_image = cv2.imread('images/bd.png', cv2.IMREAD_COLOR)
snaredrum_image = cv2.imread('images/sd.png', cv2.IMREAD_COLOR)

crash_image_resized = cv2.resize(crash_image, (cameraWidthEighth, cameraHeightEighth))
hihat_image_resized = cv2.resize(hihat_image, (cameraWidthEighth, cameraHeightEighth))
bassdrum_image_resized = cv2.resize(bassdrum_image, (cameraWidthEighth, cameraHeightEighth))
snaredrum_image_resized = cv2.resize(snaredrum_image, (cameraWidthEighth, cameraHeightEighth))

# Set initial value of weights
alpha = 0.7
msize = 5
csize = 5

# variables
nodeOnUpperLeft = -5
nodeOnUpperRight = -5
nodeOnLowerLeft = -5
nodeOnLowerRight = -5

nodeOnUpperLeftHasChanged = False
nodeOnUpperRightHasChanged = False
nodeOnLowerLeftHasChanged = False
nodeOnLowerRightHasChanged = False


def create_mask(imageslice):
    mask = np.copy(imageslice)

    # Erstellung einer Maske durch HSV-Farberkennung
    hsv = cv2.cvtColor(mask, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    hslice = cv2.inRange(h, 50, 80)
    hslice = cv2.medianBlur(hslice, msize)
    sslice = cv2.inRange(s, 60, 120)
    sslice = cv2.medianBlur(sslice, msize)
    mask = cv2.bitwise_and(hslice, sslice)
    return mask


def create_image_layer(mask):
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        contourLength = np.zeros(300, dtype=np.uint8)
        for index in range(len(contours)):
            contourLength[index] = cv2.contourArea(contours[index])
        maxlength = np.max(contourLength)
        if maxlength > csize:
            return True
        else:
            return False


while True:
    # read the background
    ret, background = cap.read()
    background = cv2.flip(background, 1)

    # top left
    top_left_corner = background[0:cameraHeightHalf, 0:cameraWidthThird, :]
    top_left_hihat = background[0:cameraHeightThird, 0:cameraWidthThird + cameraWidthSixth, :]

    if create_image_layer(create_mask(top_left_corner)):
        vorher = nodeOnUpperLeft
        if nodeOnUpperLeft + 1 <= 5:
            nodeOnUpperLeft += 1

        if vorher == 0 and nodeOnUpperLeft == 1:
            print('links oben')
            nodeOnUpperLeftHasChanged = True
    else:
        if nodeOnUpperLeft - 1 > -5:
            nodeOnUpperLeft -= 1

    # bottom left
    bottom_left_corner = background[cameraHeightHalf:cameraHeight, 0:cameraWidthThird, :]
    bottom_left_basedrum = background[cameraHeightHalf + cameraHeightSixth:cameraHeight,
                           cameraWidthThird:cameraWidthHalf, :]

    if create_image_layer(create_mask(bottom_left_corner)):
        vorher = nodeOnLowerLeft
        if nodeOnLowerLeft + 1 <= 5:
            nodeOnLowerLeft += 1

        if vorher == 0 and nodeOnUpperLeft == 1:
            print('links unten')
            nodeOnLowerLeftHasChanged = True
    else:
        if nodeOnLowerLeft - 1 > -5:
            nodeOnLowerLeft -= 1

    # top right
    top_right_corner = background[0:cameraHeightHalf, cameraWidthHalf + cameraWidthSixth:cameraWidth, :]
    top_right_crash = background[0:cameraHeightThird, cameraWidthHalf:cameraWidthHalf + cameraWidthSixth, :]

    if create_image_layer(create_mask(top_right_corner)):
        vorher = nodeOnUpperRight
        if nodeOnUpperRight + 1 <= 5:
            nodeOnUpperRight += 1

        if vorher == 0 and nodeOnUpperRight == 1:
            print('rechts oben')
            nodeOnUpperRightHasChanged = True
    else:
        if nodeOnUpperRight - 1 > -5:
            nodeOnUpperRight -= 1

    # bottom right
    bottom_right_corner = background[cameraHeightHalf:cameraHeight, cameraWidthHalf + cameraWidthSixth:cameraWidth,
                          :]
    bottom_right_snare = background[cameraHeightHalf + cameraHeightSixth:cameraHeight,
                         cameraWidthHalf:cameraWidthHalf + cameraWidthSixth, :]

    if create_image_layer(create_mask(bottom_right_corner)):
        vorher = nodeOnLowerRight
        if nodeOnLowerRight + 1 <= 5:
            nodeOnLowerRight += 1

        if vorher == 0 and nodeOnLowerRight == 1:
            print('rechts unten')
            nodeOnLowerRightHasChanged = True
    else:
        if nodeOnLowerRight - 1 > -5:
            nodeOnLowerRight -= 1

    # Select the region in the background where we want to add the image and add the images using cv2.addWeighted()

    # top left
    added_image1 = cv2.addWeighted(top_left_corner, alpha, foreground1[0:cameraHeightHalf, 0:cameraWidthThird, :],
                                   1 - alpha, 0)
    added_image5 = cv2.addWeighted(top_left_hihat, alpha,
                                   foreground1[0:cameraHeightThird, 0:cameraWidthThird + cameraWidthSixth, :],
                                   1 - alpha, 0)

    # bottom left
    added_image2 = cv2.addWeighted(bottom_left_corner, alpha,
                                   foreground2[cameraHeightHalf:cameraHeight, 0:cameraWidthThird, :], 1 - alpha, 0)
    added_image6 = cv2.addWeighted(bottom_left_basedrum, alpha,
                                   foreground2[cameraHeightHalf + cameraHeightSixth:cameraHeight,
                                   cameraWidthThird:cameraWidthHalf, :], 1 - alpha, 0)

    # top right
    added_image3 = cv2.addWeighted(top_right_corner, alpha,
                                   foreground3[0:cameraHeightHalf, cameraWidthHalf + cameraWidthSixth:cameraWidth, ],
                                   1 - alpha, 0)
    added_image7 = cv2.addWeighted(top_right_crash, alpha,
                                   foreground3[0:cameraHeightThird, cameraWidthHalf:cameraWidthHalf + cameraWidthSixth,
                                   :], 1 - alpha, 0)

    # bottom right
    added_image4 = cv2.addWeighted(bottom_right_corner, alpha, foreground4[cameraHeightHalf:cameraHeight,
                                                               cameraWidthHalf + cameraWidthSixth:cameraWidth, :],
                                   1 - alpha, 0)
    added_image8 = cv2.addWeighted(bottom_right_snare, alpha,
                                   foreground4[cameraHeightHalf + cameraHeightSixth:cameraHeight,
                                   cameraWidthHalf:cameraWidthHalf + cameraWidthSixth, :],
                                   1 - alpha, 0)

    # Hihat Image, top left
    added_image9 = cv2.addWeighted(top_left_corner[0:hihat_image_resized.shape[0], 0:hihat_image_resized.shape[1], :],
                                   0,
                                   hihat_image_resized, 1, 0)

    # Crash Image, top right
    added_image10 = cv2.addWeighted(top_right_corner[0:crash_image_resized.shape[0], 0:crash_image_resized.shape[1], :],
                                    0,
                                    crash_image_resized, 1, 0)

    # Bassdrum Image, bottom left
    added_image11 = cv2.addWeighted(
        bottom_left_corner[0:bassdrum_image_resized.shape[0], 0:bassdrum_image_resized.shape[1], :], 0,
        bassdrum_image_resized,
        1, 0)

    # Snaredrum Image, bottom left
    added_image12 = cv2.addWeighted(
        bottom_right_corner[0:snaredrum_image_resized.shape[0], 0:snaredrum_image_resized.shape[1], :], 0,
        snaredrum_image_resized, 1, 0)

    # Change the region with the result
    # Zones
    background[0:cameraHeightHalf, 0:cameraWidthThird] = added_image1
    background[0:cameraHeightThird, 0:cameraWidthThird + cameraWidthSixth] = added_image5

    background[cameraHeightHalf:cameraHeight, 0:cameraWidthThird] = added_image2
    background[cameraHeightHalf + cameraHeightSixth:cameraHeight, cameraWidthThird:cameraWidthHalf, :] = added_image6

    background[0:cameraHeightHalf, cameraWidthHalf + cameraWidthSixth:cameraWidth] = added_image3
    background[0:cameraHeightThird, cameraWidthHalf:cameraWidthHalf + cameraWidthSixth, :] = added_image7

    background[cameraHeightHalf:cameraHeight, cameraWidthHalf + cameraWidthSixth:cameraWidth] = added_image4
    background[cameraHeightHalf + cameraHeightSixth:cameraHeight,
    cameraWidthHalf:cameraWidthHalf + cameraWidthSixth] = added_image8

    # Drum images
    background[0:hihat_image_resized.shape[0], 0:hihat_image_resized.shape[1]] = added_image9
    background[0:crash_image_resized.shape[0], cameraWidth - crash_image_resized.shape[1]:cameraWidth] = added_image10
    background[cameraHeight - bassdrum_image_resized.shape[0]: cameraHeight,
    0:bassdrum_image_resized.shape[1]] = added_image11
    background[cameraHeight - snaredrum_image_resized.shape[0]: cameraHeight,
    cameraWidth - bassdrum_image_resized.shape[1]:cameraWidth] = added_image12

    if nodeOnUpperLeftHasChanged:
        midi.send_control_change(4)
        nodeOnUpperLeftHasChanged = False
    if nodeOnLowerLeftHasChanged:
        midi.send_control_change(3)
        nodeOnLowerLeftHasChanged = False
    if nodeOnUpperRightHasChanged:
        midi.send_control_change(1)
        nodeOnUpperRightHasChanged = False
    if nodeOnLowerRightHasChanged:
        midi.send_control_change(2)
        nodeOnLowerRightHasChanged = False

    cv2.imshow('Projekt', background)

    k = cv2.waitKey(10)
    # Press q to break
    if cv2.waitKey(25) != -1:
        break;
# Release the camera and destroy all windows
cap.release()
cv2.destroyAllWindows()
