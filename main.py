from fastapi import FastAPI,  UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from fastapi.responses import FileResponse,Response
from pdf_converter import convert_to_pdf
import os
from starlette.background import BackgroundTask
import base64

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://document-scanner-be.onrender.com/"
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
    with open(f'{pdfFileName}.pdf','rb') as pdfFile:
        base64string= base64.b64encode(pdfFile.read())
    # return base64string
    # return FileResponse(
    #     f'{pdfFileName}.pdf', background=BackgroundTask(deleteFile, pdfFileName), media_type="application/pdf"
    # )
    return Response(content=base64string,media_type="application/pdf",background=BackgroundTask(deleteFile, pdfFileName))
    
    



