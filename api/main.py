import os
import shutil
import threading
import traceback
import uuid
import time
import warnings
import numpy as np
import cv2
import torch
from typing import Optional, List, Dict, Any
from PIL import Image
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from diffusers import (
    StableDiffusionControlNetPipeline,
    ControlNetModel,
    DPMSolverMultistepScheduler,
)
from diffusers.utils import load_image
from transformers import (
    DPTForDepthEstimation,
    DPTImageProcessor,
    SegformerForSemanticSegmentation,
    SegformerImageProcessor,
)
from scipy import ndimage

# Suppress urllib3 v2 OpenSSL warning on macOS
warnings.filterwarnings("ignore", message="NotOpenSSLWarning")

# --- CONFIGURATION & CONSTANTS ---

# ADE20K class indices for room regions
ADE20K_FLOOR_IDX = 3
ADE20K_WALL_IDX = 0
ADE20K_CEILING_IDX = 5
ADE20K_WINDOW_IDX = 8
ADE20K_DOOR_IDX = 14
ADE20K_TABLE_IDX = 15
ADE20K_CHAIR_IDX = 19
ADE20K_SOFA_IDX = 23
ADE20K_BED_IDX = 7
ADE20K_CABINET_IDX = 10
ADE20K_SHELF_IDX = 24
ADE20K_CURTAIN_IDX = 18
ADE20K_RUG_IDX = 28
ADE20K_LAMP_IDX = 36
ADE20K_PAINTING_IDX = 22

# Object -> preferred surface mapping
OBJECT_SURFACE_MAP = {
    "sofa": "floor",
    "coffee_table": "floor",
    "dining_table": "floor",
    "chair": "floor",
    "armchair": "floor",
    "rug": "floor",
    "plant": "floor",
    "floor_lamp": "floor",
    "tv_stand": "floor",
    "bookshelf": "floor",
    "bed": "floor",
    "desk": "floor",
    "mirror": "wall",
    "painting": "wall",
    "wall_shelf": "wall",
    "clock": "wall",
    "sconce": "wall",
    "pendant_light": "ceiling",
    "chandelier": "ceiling",
    "ceiling_fan": "ceiling",
    "table_lamp": "floor",
    "vase": "floor",
    "cushion": "floor",
}

# Object descriptions for prompts
OBJECT_DESCRIPTIONS = {
    "sofa": "a stylish upholstered sofa with comfortable cushions",
    "coffee_table": "an elegant coffee table with a refined surface",
    "dining_table": "a beautifully crafted dining table",
    "chair": "a designer dining chair with clean lines",
    "armchair": "a plush armchair with refined upholstery",
    "rug": "a luxurious area rug with intricate patterns",
    "plant": "a lush potted indoor plant adding natural freshness",
    "floor_lamp": "a tall elegant floor lamp casting warm ambient light",
    "tv_stand": "a sleek media console for entertainment",
    "bookshelf": "a well-organized bookshelf with curated items",
    "bed": "a comfortable bed with premium bedding and pillows",
    "desk": "a functional designer desk with clean proportions",
    "mirror": "a decorative wall mirror with a stylish frame",
    "painting": "an artistic wall painting adding visual interest",
    "wall_shelf": "floating wall shelves with decorative items",
    "clock": "an elegant wall clock as a focal accent",
    "sconce": "wall-mounted decorative sconces with warm lighting",
    "pendant_light": "a designer pendant light hanging gracefully",
    "chandelier": "a stunning chandelier as a centerpiece",
    "ceiling_fan": "a modern ceiling fan with integrated lighting",
    "table_lamp": "a stylish table lamp with soft ambient glow",
    "vase": "a decorative ceramic vase with fresh flowers",
    "cushion": "colorful throw cushions adding comfort and style",
}

# Style-specific modifiers
STYLE_MODIFIERS = {
    "Minimalist": {
        "prefix": "A high-resolution photorealistic interior photograph of a minimalist",
        "tone": "ultra-clean lines, monochromatic palette, sparse furnishing, negative space",
        "materials": "concrete, light wood, white surfaces, matte finishes",
        "lighting": "bright natural daylight flooding through large windows",
        "suffix": "Minimalist aesthetic with Scandinavian-Japanese influence. Professional architectural photography, 8K, ultra-detailed.",
    },
    "Scandi": {
        "prefix": "A high-resolution photorealistic interior photograph of a warm Scandinavian",
        "tone": "cozy hygge atmosphere, warm and inviting, organic shapes",
        "materials": "light oak wood, white linen, soft wool, natural rattan",
        "lighting": "warm golden natural light creating a cozy atmosphere",
        "suffix": "Nordic design with warm textures and natural materials. Professional architectural photography, 8K, ultra-detailed.",
    },
    "Indochine": {
        "prefix": "A high-resolution photorealistic interior photograph of a rich Indochine-style",
        "tone": "luxurious East-meets-West fusion, ornate details, cultural richness",
        "materials": "dark mahogany wood, rattan, brass, lacquerware, silk fabrics",
        "lighting": "warm diffused light from brass lanterns and natural sources",
        "suffix": "Vietnamese-French colonial Indochine aesthetic with tropical luxury. Professional architectural photography, 8K, ultra-detailed.",
    },
    "Modern": {
        "prefix": "A high-resolution photorealistic interior photograph of a sleek contemporary modern",
        "tone": "bold geometric shapes, cutting-edge design, sophisticated luxury",
        "materials": "polished concrete, smoked glass, black steel, marble accents",
        "lighting": "crisp cool lighting with dramatic accent spots",
        "suffix": "Contemporary modern design with luxury materials. Professional architectural photography, 8K, ultra-detailed.",
    },
    "Japanese Zen": {
        "prefix": "A high-resolution photorealistic interior photograph of a serene Japanese Zen",
        "tone": "tranquil harmony, wabi-sabi imperfection, meditative atmosphere",
        "materials": "bamboo, tatami, shoji screens, natural stone, paper lanterns",
        "lighting": "soft filtered light through shoji screens, peaceful ambiance",
        "suffix": "Japanese Zen aesthetic with traditional elements. Professional architectural photography, 8K, ultra-detailed.",
    },
    "Industrial": {
        "prefix": "A high-resolution photorealistic interior photograph of an industrial loft-style",
        "tone": "raw urban aesthetic, exposed structures, converted warehouse feel",
        "materials": "exposed brick, raw concrete, black iron pipes, reclaimed wood",
        "lighting": "Edison bulb pendant lights and large factory windows",
        "suffix": "Industrial loft aesthetic with raw urban character. Professional architectural photography, 8K, ultra-detailed.",
    },
}

ROOM_DESCRIPTIONS = {
    "Living Room": "living room",
    "Bedroom": "bedroom",
    "Dining Room": "dining room",
    "Office": "home office",
    "Kitchen": "kitchen",
    "Bathroom": "bathroom",
    "Studio": "studio apartment",
}

DEFAULT_NEGATIVE_PROMPT = (
    "low quality, blurry, distorted, ugly, messy, person, people, text, watermark, "
    "deformed, bad anatomy, disfigured, poorly drawn, extra limbs, mutation, "
    "out of frame, cropped, worst quality, low resolution, jpeg artifacts, "
    "cartoon, anime, sketch, drawing"
)

# Object size ratios for segmentation
OBJECT_SIZE_RATIO = {
    "sofa": 0.25, "coffee_table": 0.10, "dining_table": 0.18, "chair": 0.06,
    "armchair": 0.10, "rug": 0.20, "plant": 0.04, "floor_lamp": 0.03,
    "tv_stand": 0.12, "bookshelf": 0.10, "bed": 0.30, "desk": 0.12,
    "mirror": 0.08, "painting": 0.06, "wall_shelf": 0.08, "clock": 0.03,
    "sconce": 0.02, "pendant_light": 0.05, "chandelier": 0.08, "ceiling_fan": 0.10,
    "table_lamp": 0.03, "vase": 0.02, "cushion": 0.03,
}

# --- DEVICE & GLOBALS ---

os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

def get_device_and_dtype():
    """
    Returns (device, torch_dtype) based on available hardware.
    - CUDA: float16
    - MPS: float32 (due to MPS float16 instability)
    - CPU: float32
    """
    if torch.cuda.is_available():
        return "cuda", torch.float16
    elif torch.backends.mps.is_available():
        return "mps", torch.float32
    else:
        return "cpu", torch.float32

device, model_dtype = get_device_and_dtype()

# Global model references
pipe = None
generation_lock = threading.Lock()
depth_model = None
depth_processor = None
seg_model = None
seg_processor = None

# Task database
tasks = {}

# --- MODEL LOADING (LAZY) ---

def load_depth_model():
    global depth_model, depth_processor
    if depth_model is not None:
        return
    print("[Depth] Loading Intel DPT-Large depth model...")
    model_name = "Intel/dpt-large"
    depth_processor = DPTImageProcessor.from_pretrained(model_name)
    depth_model = DPTForDepthEstimation.from_pretrained(model_name)
    depth_model.eval()
    print("[Depth] DPT depth model loaded successfully.")

def load_segmentation_model():
    global seg_model, seg_processor
    if seg_model is not None:
        return
    print("[Segmentation] Loading SegFormer model...")
    model_name = "nvidia/segformer-b2-finetuned-ade-512-512"
    seg_processor = SegformerImageProcessor.from_pretrained(model_name)
    seg_model = SegformerForSemanticSegmentation.from_pretrained(model_name)
    seg_model.eval()
    print("[Segmentation] SegFormer model loaded successfully.")

def load_ai_models():
    global pipe
    if pipe is not None:
        return
    print(f"[AI Engine] Using device: {device}, dtype: {model_dtype}")
    print("[AI Engine] Loading models (SD 1.5 + ControlNet Canny)...")
    try:
        controlnet = ControlNetModel.from_pretrained(
            "lllyasviel/sd-controlnet-canny", torch_dtype=model_dtype
        )
        pipe = StableDiffusionControlNetPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            controlnet=controlnet,
            torch_dtype=model_dtype,
        )
        pipe.safety_checker = None
        pipe.feature_extractor = None
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        pipe.to(device)
        pipe.enable_attention_slicing()
        pipe.enable_vae_slicing()
        print("[AI Engine] Models loaded successfully.")
    except Exception as e:
        print(f"[AI Engine] Failed to load models: {e}")
        traceback.print_exc()
        raise e

# --- UTILITY FUNCTIONS ---

def estimate_depth(image: Image.Image) -> Image.Image:
    load_depth_model()
    original_size = image.size
    inputs = depth_processor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = depth_model(**inputs)
        predicted_depth = outputs.predicted_depth
    prediction = torch.nn.functional.interpolate(
        predicted_depth.unsqueeze(1),
        size=original_size[::-1],
        mode="bicubic",
        align_corners=False,
    ).squeeze()
    depth_np = prediction.cpu().numpy()
    depth_min, depth_max = depth_np.min(), depth_np.max()
    if depth_max - depth_min > 0:
        depth_normalized = ((depth_np - depth_min) / (depth_max - depth_min) * 255).astype(np.uint8)
    else:
        depth_normalized = np.zeros_like(depth_np, dtype=np.uint8)
    return Image.fromarray(depth_normalized).convert("RGB")

def build_prompt(style: str, objects_list: List[str], room_type: str = "Living Room", custom_prompt: Optional[str] = None) -> dict:
    if style == "Custom" and custom_prompt:
        return {"prompt": custom_prompt, "negative_prompt": DEFAULT_NEGATIVE_PROMPT}

    style_info = STYLE_MODIFIERS.get(style, STYLE_MODIFIERS["Modern"])
    room_desc = ROOM_DESCRIPTIONS.get(room_type, "room")
    obj_descriptions = [OBJECT_DESCRIPTIONS.get(obj, f"a {obj.replace('_', ' ')}") for obj in objects_list]
    objects_text = ", ".join(obj_descriptions) if obj_descriptions else "tasteful furnishings"

    prompt = (
        f"{style_info['prefix']} {room_desc} featuring {objects_text}. "
        f"The room maintains its original spatial structure and camera angle. "
        f"Style elements: {style_info['tone']}. "
        f"Materials: {style_info['materials']}. "
        f"Lighting: {style_info['lighting']}. "
        f"{style_info['suffix']}"
    )
    return {"prompt": prompt, "negative_prompt": DEFAULT_NEGATIVE_PROMPT}

def get_room_segments(image: Image.Image) -> Dict[str, np.ndarray]:
    load_segmentation_model()
    inputs = seg_processor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = seg_model(**inputs)
    logits = outputs.logits
    upsampled = torch.nn.functional.interpolate(logits, size=image.size[::-1], mode="bilinear", align_corners=False)
    seg_map = upsampled.argmax(dim=1).squeeze().cpu().numpy()
    floor_mask = (seg_map == ADE20K_FLOOR_IDX).astype(np.uint8)
    wall_mask = (seg_map == ADE20K_WALL_IDX).astype(np.uint8)
    ceiling_mask = (seg_map == ADE20K_CEILING_IDX).astype(np.uint8)
    return {"floor": floor_mask, "wall": wall_mask, "ceiling": ceiling_mask, "full_segmap": seg_map}

# --- INFERENCE LOGIC ---

def generate_interior(
    image_path: str, style: str, room_type: str, custom_prompt: Optional[str] = None, progress_callback: Optional[Any] = None
) -> str:
    with generation_lock:
        try:
            prompt_data = build_prompt(style, [], room_type, custom_prompt)
            prompt = prompt_data["prompt"]
            negative_prompt = prompt_data["negative_prompt"]

            # Style-specific parameters
            style_params = {
                "Minimalist": {"gs": 7.5, "steps": 35},
                "Scandi": {"gs": 8.5, "steps": 40},
                "Indochine": {"gs": 9.0, "steps": 50},
                "Modern": {"gs": 8.5, "steps": 45},
                "Japanese Zen": {"gs": 8.0, "steps": 40},
                "Industrial": {"gs": 8.5, "steps": 45},
            }
            params = style_params.get(style, style_params["Modern"])
            guidance_scale = params["gs"]
            num_inference_steps = params["steps"]

            print(f"[AI Engine] Running inference for {image_path}")
            load_ai_models()
            if pipe is None:
                raise RuntimeError("AI Models not initialized.")

            image = load_image(image_path).convert("RGB")
            max_size = 768
            width, height = image.size
            if max(width, height) > max_size:
                scale = max_size / max(width, height)
                width, height = int(width * scale), int(height * scale)
            width = (width // 8) * 8
            height = (height // 8) * 8
            if image.size != (width, height):
                image = image.resize((width, height), Image.LANCZOS)

            image_np = np.array(image)
            image_canny = cv2.Canny(image_np, 100, 200)[:, :, None]
            image_canny = np.concatenate([image_canny, image_canny, image_canny], axis=2)
            canny_image = Image.fromarray(image_canny)

            generator = torch.Generator(device=device).manual_seed(42)
            # Reset scheduler internal state if needed (DPMSolverMultistepScheduler)
            if hasattr(pipe.scheduler, "model_outputs"):
                pipe.scheduler.model_outputs = [None] * pipe.scheduler.config.solver_order

            output = pipe(
                prompt, image=canny_image, negative_prompt=negative_prompt,
                num_inference_steps=num_inference_steps, guidance_scale=guidance_scale,
                generator=generator, controlnet_conditioning_scale=1.0,
                callback=progress_callback, callback_steps=1,
            ).images[0]

            os.makedirs("results", exist_ok=True)
            result_path = f"results/generated_{os.path.basename(image_path)}"
            output.save(result_path)
            return result_path
        except Exception as e:
            traceback.print_exc()
            with open("error_log.txt", "w") as f:
                f.write(traceback.format_exc())
            raise e

# --- FASTAPI APP ---

app = FastAPI(title="AI Interior Decorator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    style_steps = {"Minimalist": 35, "Scandi": 40, "Indochine": 50, "Modern": 45, "Japanese Zen": 40, "Industrial": 45}
    total_steps = style_steps.get(request.style, 45)
    tasks[task_id] = {
        "status": "processing", "progress": 0, "total_steps": total_steps,
        "result_url": None, "error": None, "start_time": time.time(),
        "estimated_total_time": total_steps * 4,
    }
    def progress_callback(step, timestep, latents):
        tasks[task_id]["progress"] = step
    def run_generation_task(t_id: str, req: GenerateRequest):
        try:
            result_path = generate_interior(req.image_path, req.style, req.room_type, req.custom_prompt, progress_callback=progress_callback)
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
    total_steps, progress = task["total_steps"], task["progress"]
    if task["status"] == "processing" and progress > 0:
        remaining_time = max(0, (total_steps - progress) * (elapsed / progress))
    elif task["status"] == "processing":
        remaining_time = task["estimated_total_time"] - elapsed
    else:
        remaining_time = 0
    return {
        "task_id": task_id, "status": task["status"], "progress": progress,
        "total_steps": total_steps, "remaining_time": round(max(0, remaining_time), 1),
        "result_url": task["result_url"], "error": task["error"]
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