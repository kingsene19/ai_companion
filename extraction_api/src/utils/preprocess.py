import cv2
import numpy as np
import matplotlib.pyplot as plt

class Preprocessor:

    def __init__(self, im):
        self.im = im

    def getLines(self):
        thresh, binary = cv2.threshold(self.im, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        binary = 255 - binary
        kernel_len = np.array(self.im).shape[1]//100
        ver_ker = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
        hor_ker = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
        im1 = cv2.erode(binary, ver_ker,iterations=3)
        ver_lines = cv2.dilate(im1, ver_ker, iterations=3)
        im2 = cv2.erode(binary, hor_ker,iterations=3)
        hor_lines = cv2.dilate(im2, hor_ker, iterations=3)
        return ver_lines, hor_lines 
    
    def reconstructImage(self):
        ver_lines, hor_lines = self.getLines()
        img_vh = cv2.addWeighted(ver_lines, 0.5, hor_lines, 0.5, 0.0)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        img_vh = cv2.erode(~img_vh, kernel, iterations=2)
        thresh, img_vh = cv2.threshold(img_vh,128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        bitxor = cv2.bitwise_xor(self.im, img_vh)
        bitnot = cv2.bitwise_not(bitxor)
        return img_vh, bitnot
    
    def retriveAndSortContours(self):
        img_vh, bitnot = self.reconstructImage()
        contours, hierarchy = cv2.findContours(img_vh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        def sort_contours(cnts, method="left-to-right"):
            reverse = False
            i = 0
            if method == "right-to-left" or method == "bottom-to-top":
                reverse = True
            if method == "top-to-bottom" or method == "bottom-to-top":
                i = 1
            boundingBoxes = [cv2.boundingRect(c) for c in cnts]
            (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
            key=lambda b:b[1][i], reverse=reverse))
            return (cnts, boundingBoxes)
        contours, boundingBoxes = sort_contours(contours, method="top-to-bottom")
        heights = [boundingBoxes[i][3] for i in range(len(boundingBoxes))]
        mean = np.mean(heights)
        box = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if (w<1000 and h<500):
                image = cv2.rectangle(self.im,(x,y),(x+w,y+h),(0,255,0),2)
                box.append([x,y,w,h])
        row=[]
        column=[]
        for i in range(len(box)):
            if(i==0):
                column.append(box[i])
                previous=box[i]
            else:
                if(box[i][1]<=previous[1]+mean/2):
                    column.append(box[i])
                    previous=box[i]
                    if(i==len(box)-1):
                        row.append(column)
                else:
                    row.append(column)
                    column=[]
                    previous = box[i]
                    column.append(box[i])
        countcol = 0
        for i in range(len(row)):
            countcol = len(row[i])
            if countcol > countcol:
                countcol = countcol
        center = [int(row[i][j][0]+row[i][j][2]/2) for j in range(len(row[i])) if row[0]]
        center=np.array(center)
        center.sort()
        finalboxes = []
        for i in range(len(row)):
            lis=[]
            for k in range(countcol):
                lis.append([])
            for j in range(len(row[i])):
                diff = abs(center-(row[i][j][0]+row[i][j][2]/4))
                minimum = min(diff)
                indexing = list(diff).index(minimum)
                lis[indexing].append(row[i][j])
            finalboxes.append(lis)
        return finalboxes, bitnot, countcol, row