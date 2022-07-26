#
# Jonah Fullen
# Programming Assignment 3: Harris Corners
# 02-22-2022
#

import cv2
import numpy as np


def main():
    # Import the desired image and set up all blank copies needed
    im = cv2.imread("checkerboard.png", 0)
    imCopy = cv2.imread("checkerboard.png")
    numRows = im.shape[0]
    numCols = im.shape[1]
    Ix = np.zeros((numRows, numCols, 3), np.float32)
    Iy = np.zeros((numRows, numCols, 3), np.float32)
    IxIx = np.zeros((numRows, numCols, 3), np.float32)
    IyIy = np.zeros((numRows, numCols, 3), np.float32)
    IxIy = np.zeros((numRows, numCols, 3), np.float32)
    c = np.zeros((numRows, numCols, 3), np.float32)

    # Calculate the different values and store them in the appropriate image matrix
    for i in range(1, numRows-1):
        for j in range(1, numCols-1):
            Ix[i][j] = int(im[i+1][j]) - int(im[i-1][j])
            Iy[i][j] = int(im[i][j+1]) - int(im[i][j-1])
            IxIx[i][j] = Ix[i][j] ** 2
            IyIy[i][j] = Iy[i][j] ** 2
            IxIy[i][j] = Ix[i][j] * Iy[i][j]

    # Use the generated values to calculate the "cornerness" for each pixel
    for i in range(1, numRows-1):
        for j in range(1, numCols-1):
            IxxSum = 0
            IyySum = 0
            IxySum = 0
            for k in range(-1, 2):
                for l in range(-1, 2):
                    IxxSum += IxIx[i + k][j + l]
                    IyySum += IyIy[i + k][j + l]
                    IxySum += IxIy[i + k][j + l]
            m = [[IxxSum, IxySum], [IxySum, IyySum]]
            det = (m[0][0] * m[1][1]) - (m[0][1] * m[1][0])
            trace = m[0][0] + m[1][1]
            cness = det - 0.05 * (trace ** 2)
            c[i][j] = cness

    # Method 1 for Identifying Corners
    max = 0
    min = 0
    for i in range(1, numRows-1):
        for j in range(1, numCols-1):
            if c[i][j][0] > max:
                max = c[i][j][0]
            if c[i][j][0] < min:
                min = c[i][j][0]
    corners = np.zeros((numRows, numCols, 3), np.float32)
    for i in range(1, numRows-1):
        for j in range(1, numCols-1):
            if c[i][j][0] >= max * 0.5:  # Select corners within this % of the max
                corners[i][j] = 255
            else:
                corners[i][j] = 0

    # Method 2 for Identifying Corners
    corners2 = np.zeros((numRows, numCols, 3), np.float32)
    width = numRows // 10
    height = numCols // 10
    for a in range(10):
        for b in range(10):
            max = 0
            for x in range(a * width, (a * width) + width):
                for y in range(b * height, (b * height) + height):
                    if c[x][y][0] > max:
                        max = c[x][y][0]
            for x in range(a * width, (a * width) + width):
                for y in range(b * height, (b * height) + height):
                    if c[x][y][0] >= max * 0.95:    # Select corners within this % of the local max
                        corners2[x][y] = 255
                    else:
                        corners2[x][y] = 0

    # Turn the corners into red circles in the original image copy
    for i in range(1, numRows-1):
        for j in range(1, numCols-1):
            if corners[i][j][0] != 0:  # Change between "corners" and "corners2" to pick
                # Method 1 or Method 2 for getting corners
                cv2.circle(imCopy, (j, i), 2, (0, 0, 255), -1)

    # Bonus: Cornerness Gradient
    gradient = np.zeros((numRows, numCols, 3), np.float32)
    for i in range(1, numRows-1):
        for j in range(1, numCols-1):
            cval = c[i][j][0]
            if cval < 0:    # C-values that are negative
                perc = abs(cval)/abs(min)
                shade = perc * 127
            elif cval > 0:  # C-values that are positive
                perc = cval/max
                shade = (perc * 127) + 127
            else:
                shade = 128
            gradient[i][j] = shade

    cv2.imshow("Display the Original Image", gradient)  # Open the display window
    cv2.waitKey(0)  # Assign the window the wait key
    cv2.destroyAllWindows()

    # save the new image
    # cv2.imwrite("checkerboardBonus.png", imCopy)
    # print("Image Saved")


main()
