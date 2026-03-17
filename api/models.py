from pydantic import BaseModel
from typing import Optional

class GenerateRequest(BaseModel):
    image_path: str
    style: str
    room_type: str
    custom_prompt: Optional[str] = None

class TaskStatus(BaseModel):
    task_id: str
    status: str
    progress: int
    total_steps: int
    remaining_time: float
    result_url: Optional[str] = None
    error: Optional[str] = None

class UploadResponse(BaseModel):
    image_path: str
    message: str
