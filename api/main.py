import os
import warnings
import shutil

# Suppress urllib3 v2 OpenSSL warning on macOS
warnings.filterwarnings("ignore", message="NotOpenSSLWarning")
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

from inference import generate_interior

app = FastAPI(title="AI Interior Decorator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
os.makedirs("results", exist_ok=True)

class GenerateRequest(BaseModel):
    image_path: str
    style: str
    room_type: str

@app.get("/")
def read_root():
    return {"status": "ok", "message": "AI Interior Decorator API is running."}

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"image_path": file_path, "message": "File uploaded successfully"}

@app.post("/generate")
async def generate_image(request: GenerateRequest):
    try:
        result_path = generate_interior(request.image_path, request.style, request.room_type)
        return {"result_url": f"/results/{os.path.basename(result_path)}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/results/{filename}")
async def get_result(filename: str):
    file_path = f"results/{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
