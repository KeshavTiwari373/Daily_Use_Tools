from fastapi import FastAPI, UploadFile, File
import shutil
import os
from extract_text import extract_text

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/extract-text/")
async def extract_text_from_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text(file_path)
    return {"Extracted Data": extracted_text}

# Run API using: uvicorn api:app --reload