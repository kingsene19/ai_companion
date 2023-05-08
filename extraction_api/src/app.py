from fastapi import FastAPI, UploadFile, File
from PIL import Image, UnidentifiedImageError
import io
from utils.extractor import MenuExtractor, ScheduleExtractor
from utils.preprocess import Preprocessor
import uvicorn
import numpy as np
import cv2
import json
import os

app = FastAPI()


@app.post("/extract_menu")
async def extract(file: UploadFile):
    file_content = await file.read()

    Metadata = dict()
    Metadata["image_name"] = file.filename

    try:
        img = Image.open(io.BytesIO(file_content))
        Metadata["width"], Metadata["height"] = img.size
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    except Exception as e:
        Info = dict()
        if e is UnidentifiedImageError:
            Info['error'] = "Assurez vous que le fichier est bien une image de facture sénélec, seneau ou sonatel"
            return {
                'bill_infos': Info,
                'metadata': Metadata,
                'status': 'KO'}
        else:
            Info['error'] = repr(e)
            return {
                'bill_infos': Info,
                'metadata': Metadata,
                'status': 'KO'}
        
    # finalboxes, bitnot, countcol, row = Preprocessor(img).retriveAndSortContours()
    # result = MenuExtractor(finalboxes, bitnot, countcol, row).retrieveResult()

    # with open('src/data/menu.json', 'w') as f:
    #     json.dump(result, f)

    return {
        "metadata": Metadata,
        "status": 'OK'
    }

@app.post("/extract_schedule")
async def extract(file: UploadFile, classe: str = "dic2" , field: str = "git"):
    file_content = await file.read()

    Metadata = dict()
    Metadata["image_name"] = file.filename

    try:
        img = Image.open(io.BytesIO(file_content))
        Metadata["width"], Metadata["height"] = img.size
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    except Exception as e:
        Info = dict()
        if e is UnidentifiedImageError:
            Info['error'] = "Assurez vous que le fichier est bien une image de facture sénélec, seneau ou sonatel"
            return {
                'bill_infos': Info,
                'metadata': Metadata,
                'status': 'KO'}
        else:
            Info['error'] = repr(e)
            return {
                'bill_infos': Info,
                'metadata': Metadata,
                'status': 'KO'}
        
    finalboxes, bitnot, countcol, row = Preprocessor(img).retriveAndSortContours()
    # result = ScheduleExtractor(finalboxes, bitnot, countcol, row).retrieveResult()

    # with open(f'src/data/{classe}/{field}.json', 'w') as f:
    #     json.dump(result, f)

    return {
        "metadata": Metadata,
        "status": 'OK'
    }

@app.get("/get_menu")
async def getMenu():
    with open('src/data/menu.json') as json_file:
        data = json.load(json_file)

    return data

@app.get("/get_schedule")
async def getSchedule(classe: str, field: str):
    with open(f'src/data/{classe}/{field}.json') as json_file:
        data = json.load(json_file)

    return data

if __name__ == "__main__":
    uvicorn.run("app:app", host = "0.0.0.0", port=5000)