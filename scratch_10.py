import cv2
import numpy as np
import matplotlib.pyplot as plt

def getContours(img,cThr = [100,100],showCanny = False,minArea = 10,filter = 0,draw = False):
    #converting image to grayscale
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    #blurring the image,ksize =(5,5) and sigmaX = 1
    imgBlur = cv2.blur(imgGray,(5,5),0)

    #it is canny edge detection which is used
    imgCanny = cv2.Canny(imgBlur, cThr[0], cThr[1],apertureSize=3)
    imgCanny = cv2.resize(imgCanny, (600,600))
    #findingcontours of the image
    cont, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #As i am not getting proper contour encircling the image,
    #I draw lines from various small contours
    lines = cv2.HoughLinesP(imgCanny, 1, np.pi / 2, 50, None, 5, 50)
    point_y_max = 0  # maximum of y
    point_y_min = 1000  # minimum of y
    min = []    #array storing values of point_y_min
    mit = []    #array storing values of point_y_max
    if lines is not None:
        for i in range(0, len(lines)):
            l = lines[i][0]
            if point_y_max < l[1]:
                point_y_max = l[1]
            if point_y_min > l[1]:
                point_y_min = l[1]
        y_mo = point_y_min + 30
        y_mi = point_y_min - 20
        print(y_mi, y_mo)
        for i in range(0, len(lines)):
            l = lines[i][0]
            if l[1] in range(y_mi, y_mo):
                mit.append(l[0])
            if l[3] in range(y_mi, y_mo):
                mit.append(l[2])
        y_more = point_y_max + 30
        y_min = point_y_max - 20
        for i in range(0, len(lines)):
            l = lines[i][0]
            if l[1] in range(y_min,y_more):
                min.append(l[0])
            if l[3] in range(y_min,y_more):
                min.append(l[2])
        point1 = np.min(mit), point_y_min
        point2 = np.max(mit), point_y_min
        point3 = np.min(min),point_y_max
        point4 = np.max(min),point_y_max

        cv2.line(img, (point1), (point2), (255, 0, 255), 3, cv2.LINE_AA)
        cv2.line(img, (point3), (point4), (255, 0, 255), 3, cv2.LINE_AA)

        if (point2[0]-point1[0] == point4[0] - point3[0]):
            img = cv2.putText(img,"Centre",(300,300),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
        print("1 point",point1,point2,point3,point4)

    return img