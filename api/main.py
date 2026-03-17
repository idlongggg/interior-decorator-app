import os
import warnings
import shutil

# Suppress urllib3 v2 OpenSSL warning on macOS
warnings.filterwarnings("ignore", message="NotOpenSSLWarning")
import uuid
import time
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from inference import generate_interior

# Database to store task status (in-memory)
tasks = {}

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
    custom_prompt: Optional[str] = None

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
async def generate_image(request: GenerateRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    
    # Pre-calculate estimated steps based on style
    style_steps = {
        "Minimalist": 35,
        "Scandi": 40,
        "Indochine": 50,
        "Modern": 45,
    }
    total_steps = style_steps.get(request.style, 45)

    tasks[task_id] = {
        "status": "processing",
        "progress": 0,
        "total_steps": total_steps,
        "result_url": None,
        "error": None,
        "start_time": time.time(),
        "estimated_total_time": total_steps * 4, # 4s per step is a safe guess for Mac
    }
    
    def progress_callback(step, timestep, latents):
        tasks[task_id]["progress"] = step
        
    def run_generation_task(t_id: str, req: GenerateRequest):
        try:
            result_path = generate_interior(
                req.image_path, 
                req.style, 
                req.room_type, 
                req.custom_prompt,
                progress_callback=progress_callback
            )
            tasks[t_id]["status"] = "completed"
            tasks[t_id]["progress"] = 100
            tasks[t_id]["result_url"] = f"/results/{os.path.basename(result_path)}"
        except Exception as e:
            tasks[t_id]["status"] = "failed"
            tasks[t_id]["error"] = str(e)

    background_tasks.add_task(run_generation_task, task_id, request)
    return {"task_id": task_id}

@app.get("/status/{task_id}")
async def get_task_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks[task_id]
    elapsed = time.time() - task["start_time"]
    
    total_steps = task["total_steps"]
    progress = task["progress"]
    
    if task["status"] == "processing" and progress > 0:
        time_per_step = elapsed / progress
        remaining_steps = total_steps - progress
        remaining_time = max(0, remaining_steps * time_per_step)
    elif task["status"] == "processing":
        # Waiting for model to load or first step
        remaining_time = task["estimated_total_time"] - elapsed
    else:
        remaining_time = 0

    return {
        "task_id": task_id,
        "status": task["status"],
        "progress": progress,
        "total_steps": total_steps,
        "remaining_time": round(max(0, remaining_time), 1),
        "result_url": task["result_url"],
        "error": task["error"]
    }

@app.get("/results/{filename}")
async def get_result(filename: str):
    file_path = f"results/{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
