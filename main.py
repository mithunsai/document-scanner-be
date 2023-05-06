from fastapi import FastAPI,  UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import cv2
import numpy as np


app = FastAPI()

origins = [
    "http://localhost:3000",
    "*"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/uploadImages/")
async def uploadImages(imageFiles: List[UploadFile]):
    images= []
    for imageFile in imageFiles:
        content = await imageFile.read()
        nparray = np.fromstring(content, np.uint8)
        image = cv2.imdecode(nparray, cv2.IMREAD_COLOR)
        images.append(image)
    
    return {"filenames": [imageFile.filename for imageFile in imageFiles]}
    
    



