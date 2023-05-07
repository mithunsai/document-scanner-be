from fastapi import FastAPI,  UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from fastapi.responses import FileResponse
from pdf_converter import convert_to_pdf
import os
from starlette.background import BackgroundTask

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

def deleteFile(pdfFileName):
    os.remove(f'{pdfFileName}.pdf')
    
    
@app.post("/uploadImages/")
async def uploadImages(imageFiles: List[UploadFile]):
    pdfFileName= await convert_to_pdf(imageFiles)
    return FileResponse(
        f'{pdfFileName}.pdf', background=BackgroundTask(deleteFile, pdfFileName)
    )
    
    



