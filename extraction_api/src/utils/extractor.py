import cv2
import numpy as np
import pandas as pd
import pytesseract
    

class MenuExtractor:

    def __init__(self, bboxes, bitnot, countcol, row):
        self.bboxes = bboxes
        self.bitnot = bitnot
        self.countcol = countcol
        self.row = row
        self.outer = []


    def extractText(self):
        for i in range(len(self.bboxes)):
            for j in range(len(self.bboxes[i])):
                inner=''
                if(len(self.bboxes[i][j])==0):
                    self.outer.append(' ')
                else:
                    for k in range(len(self.bboxes[i][j])):
                        y,x,w,h = self.bboxes[i][j][k][0],self.bboxes[i][j][k][1], self.bboxes[i][j][k][2],self.bboxes[i][j][k][3]
                        finalimg = self.bitnot[x:x+h, y:y+w]
                        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
                        border = cv2.copyMakeBorder(finalimg,2,2,2,2,   cv2.BORDER_CONSTANT,value=[255,255])
                        resizing = cv2.resize(border, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                        dilation = cv2.dilate(resizing, kernel,iterations=1)
                        erosion = cv2.erode(dilation, kernel,iterations=1)
                        out = pytesseract.image_to_string(erosion)
                        if(len(out)==0):
                            out = pytesseract.image_to_string(erosion, config='--psm 3')
                        inner = inner +" "+ out
                    self.outer.append(inner)

    def retrieveResult(self):
        self.extractText()
        arr = np.array(self.outer)
        dataframe = pd.DataFrame(arr.reshape(len(self.row),self.countcol))
        res = {}
        for i in range(dataframe.shape[0]):
            if dataframe.iloc[i].str.contains("Jours").any():
                j = dataframe.columns[dataframe.iloc[i].str.contains("Jours")]
                res["jours"] = (j[0], i)
        for i in range(dataframe.shape[0]):
            if dataframe.iloc[i].str.contains("jeuner").any():
                j = dataframe.columns[dataframe.iloc[i].str.contains("jeuner")]
                res["dejeuner"] = (j[0], i)
        for i in range(dataframe.shape[0]):
            if dataframe.iloc[i].str.contains("iner").any():
                j = dataframe.columns[dataframe.iloc[i].str.contains("iner")]
                res["diner"] = (j[0], i)
        df1 = dataframe[res['jours'][0]][res['jours'][1]:]
        df2 = dataframe[res['dejeuner'][0]][res['dejeuner'][1]:]
        df3 = dataframe[res['diner'][0]][res['diner'][1]:]
        info = {}
        for i in range(res['jours'][1]+1, dataframe.shape[0]):
            key = df1[i].strip()
            if key != "":
                info[key] = {
                    "lunch": df2[i].strip().lower(),
                    "dinner": df3[i].strip().lower()
                }
        d = {"Lundi": "Monday", "Mardi": "Tuesday", "Mercredi": "Wednesday", "Jeudi": "Thrusday", "Vendredi": "Friday", "Samedi": "Saturday", "Dimanche": "Sunday"}
        info = dict((d[key], value) for (key, value) in info.items())
        return info


class ScheduleExtractor:

    def __init__(self, bboxes, bitnot, countcol, row):
        self.bboxes = bboxes
        self.bitnot = bitnot
        self.countcol = countcol
        self.row = row
        self.outer = []


    def extractText(self):
        for i in range(len(self.bboxes)):
            for j in range(len(self.bboxes[i])):
                inner=''
                if(len(self.bboxes[i][j])==0):
                    self.outer.append(' ')
                else:
                    for k in range(len(self.bboxes[i][j])):
                        y,x,w,h = self.bboxes[i][j][k][0],self.bboxes[i][j][k][1], self.bboxes[i][j][k][2],self.bboxes[i][j][k][3]
                        finalimg = self.bitnot[x:x+h, y:y+w]
                        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
                        border = cv2.copyMakeBorder(finalimg,2,2,2,2,   cv2.BORDER_CONSTANT,value=[255,255])
                        resizing = cv2.resize(border, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                        dilation = cv2.dilate(resizing, kernel,iterations=1)
                        erosion = cv2.erode(dilation, kernel,iterations=1)
                        out = pytesseract.image_to_string(erosion)
                        if(len(out)==0):
                            out = pytesseract.image_to_string(erosion, config='--psm 3')
                        inner = inner +" "+ out
                    self.outer.append(inner)

    def retrieveResult(self):
        self.extractText()
        arr = np.array(self.outer)
        dataframe = pd.DataFrame(arr.reshape(len(self.row),self.countcol))
        df = dataframe.iloc[0]
        print(df)
        info = dict()
        lis = []
        daysDict = {}
        days = ["Monday", "Tuesday", "Wednesday", "Thrusday", "Friday", "Saturday"]
        for i in range(dataframe.shape[1]):
            if "E" in  df[i]:
                lis.append(i)
        if (9 in lis) or (11 in lis) or (13 in lis) or (15 in lis) or (17 in lis) or (19 in lis):
            keys = [i+2 for i in range(7, 18, 2)] 
        elif (8 in lis) or (10 in lis) or (12 in lis) or (14 in lis) or (16 in lis) or (18 in lis):
            keys = [i+2 for i in range(6, 17, 2)]
        for i in zip(keys,days):
            daysDict[i[0]] = i[1]
        for i in keys:
            if len(df[i].strip().split('\n\n')) > 1:
                info[str(daysDict[i])] = {
                "08H - 09H" : preprocess_result(df[i].strip().split('\n\n')[0]),
                "09H - 10H".strip() : preprocess_result(df[i].strip().split('\n\n')[0]),
                "10H - 11H".strip() : preprocess_result(df[i].strip().split('\n\n')[0]),
                "11H - 12H".strip() : preprocess_result(df[i].strip().split('\n\n')[0]),
                "15H - 16H".strip() : preprocess_result(df[i].strip().split('\n\n')[1]),
                "16H - 17H".strip() : preprocess_result(df[i].strip().split('\n\n')[1]),
                "17H - 18H".strip() : preprocess_result(df[i].strip().split('\n\n')[1]),
                "18H - 19H".strip() : preprocess_result(df[i].strip().split('\n\n')[1])
                }
            else:
                info[str(daysDict[i])] = {
                "08H - 09H" : preprocess_result(df[i].strip().split('\n\n')[0]),
                "09H - 10H".strip() : preprocess_result(df[i].strip().split('\n\n')[0]),
                "10H - 11H".strip() : preprocess_result(df[i].strip().split('\n\n')[0]),
                "11H - 12H".strip() : preprocess_result(df[i].strip().split('\n\n')[0]),
                "15H - 16H".strip() : "",
                "16H - 17H".strip() : "",
                "17H - 18H".strip() : "",
                "18H - 19H".strip() : ""
            }
        return info

def preprocess_result(data):
  index = data.find("M.")
  return data[:index].replace("E.C:", "").replace("EC:", "").replace("\n", " ").replace("EC;", "").replace("E.C;", "").replace("‘", "").replace("E.C:\n", "").replace("Sall", "Salle").strip()