import os
import uuid
import time
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from api.models import GenerateRequest, TaskStatus, UploadResponse
from api.inference import generate_interior
from api.config import settings

router = APIRouter()

# In-memory task store
tasks = {}

@router.get("/")
def read_root():
    return {"status": "ok", "message": settings.app_name + " is running."}

@router.post("/upload", response_model=UploadResponse)
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    os.makedirs(settings.uploads_dir, exist_ok=True)
    file_path = os.path.join(settings.uploads_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"image_path": file_path, "message": "File uploaded successfully"}

@router.post("/generate")
async def generate_image(request: GenerateRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    
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
        "estimated_total_time": total_steps * 4,
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

@router.get("/status/{task_id}", response_model=TaskStatus)
async def get_task_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks[task_id]
    elapsed = time.time() - task["start_time"]
    progress = task["progress"]
    total_steps = task["total_steps"]
    
    remaining_time = 0
    if task["status"] == "processing":
        if progress > 0:
            time_per_step = elapsed / progress
            remaining_time = max(0, (total_steps - progress) * time_per_step)
        else:
            remaining_time = task["estimated_total_time"] - elapsed

    return {
        "task_id": task_id,
        "status": task["status"],
        "progress": progress,
        "total_steps": total_steps,
        "remaining_time": round(max(0, remaining_time), 1),
        "result_url": task["result_url"],
        "error": task["error"]
    }

@router.get("/results/{filename}")
async def get_result(filename: str):
    file_path = os.path.join(settings.results_dir, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")
