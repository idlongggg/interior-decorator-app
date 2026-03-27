import os
import shutil
import uuid
import time
import numpy as np
import cv2
import torch
from typing import List, Optional
from PIL import Image
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from diffusers import (
    StableDiffusionControlNetPipeline,
    StableDiffusionInpaintPipeline,
    ControlNetModel,
    DPMSolverMultistepScheduler,
)
from diffusers.utils import load_image
from transformers import SegformerForSemanticSegmentation, SegformerImageProcessor

# -------------------- CONSTANTS --------------------
ADE20K_FLOOR = 3
ADE20K_WALL = 0
ADE20K_CEILING = 5

OBJECT_SURFACE = {
    "sofa": "floor", "coffee_table": "floor", "dining_table": "floor", "chair": "floor",
    "armchair": "floor", "rug": "floor", "plant": "floor", "floor_lamp": "floor",
    "tv_stand": "floor", "bookshelf": "floor", "bed": "floor", "desk": "floor",
    "mirror": "wall", "painting": "wall", "wall_shelf": "wall", "clock": "wall",
    "sconce": "wall", "pendant_light": "ceiling", "chandelier": "ceiling", "ceiling_fan": "ceiling",
    "table_lamp": "floor", "vase": "floor", "cushion": "floor",
}

OBJECT_DESC = {
    "sofa": "a stylish sofa", "coffee_table": "a coffee table", "dining_table": "a dining table",
    "chair": "a chair", "armchair": "an armchair", "rug": "a rug", "plant": "a plant",
    "floor_lamp": "a floor lamp", "tv_stand": "a TV stand", "bookshelf": "a bookshelf",
    "bed": "a bed", "desk": "a desk", "mirror": "a mirror", "painting": "a painting",
    "wall_shelf": "wall shelves", "clock": "a clock", "sconce": "wall sconces",
    "pendant_light": "a pendant light", "chandelier": "a chandelier", "ceiling_fan": "a ceiling fan",
    "table_lamp": "a table lamp", "vase": "a vase", "cushion": "cushions",
}

STYLE_TEXT = {
    "Minimalist": "A minimalist living room with clean lines, neutral colors, sparse furnishing.",
    "Scandi": "A Scandinavian living room with light wood, cozy textiles, warm lighting.",
    "Modern": "A modern living room with sleek furniture, polished surfaces, contemporary design.",
    "Japanese Zen": "A Japanese Zen room with natural materials, tatami, peaceful ambiance.",
    "Industrial": "An industrial loft with exposed brick, metal accents, raw concrete.",
}

ROOM_TYPE = {
    "Living Room": "living room", "Bedroom": "bedroom", "Dining Room": "dining room",
    "Office": "home office", "Kitchen": "kitchen", "Bathroom": "bathroom",
}

DEFAULT_NEGATIVE = "low quality, blurry, ugly, person, people, text, watermark, deformed"

OBJECT_SIZE = {
    "sofa": 0.18, "coffee_table": 0.10, "dining_table": 0.15, "chair": 0.06,
    "armchair": 0.10, "rug": 0.20, "plant": 0.04, "floor_lamp": 0.03,
    "tv_stand": 0.12, "bookshelf": 0.10, "bed": 0.25, "desk": 0.10,
    "mirror": 0.08, "painting": 0.06, "wall_shelf": 0.08, "clock": 0.03,
    "sconce": 0.02, "pendant_light": 0.05, "chandelier": 0.08, "ceiling_fan": 0.10,
    "table_lamp": 0.03, "vase": 0.02, "cushion": 0.03,
}

# Cấu hình tối ưu tốc độ
MAX_OBJECTS = 3                    # Giới hạn số object
IMAGE_MAX_SIZE = 640               # Giảm kích thước ảnh để tăng tốc
CONTROLNET_STEPS = 20              # Giảm steps từ 35 xuống 20
INPAINT_STEPS = 15                 # Giảm steps từ 25 xuống 15

# -------------------- DEVICE --------------------
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

def get_device():
    if torch.cuda.is_available():
        return "cuda", torch.float16
    elif torch.backends.mps.is_available():
        return "mps", torch.float32
    else:
        return "cpu", torch.float32

device, dtype = get_device()

# -------------------- MODELS --------------------
controlnet_pipe = None
inpaint_pipe = None
seg_model = None
seg_processor = None

def load_controlnet():
    global controlnet_pipe
    if controlnet_pipe is not None:
        return
    controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-canny", torch_dtype=dtype)
    controlnet_pipe = StableDiffusionControlNetPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", controlnet=controlnet, torch_dtype=dtype
    )
    controlnet_pipe.safety_checker = None
    controlnet_pipe.scheduler = DPMSolverMultistepScheduler.from_config(controlnet_pipe.scheduler.config)
    controlnet_pipe.to(device)
    controlnet_pipe.enable_attention_slicing()
    controlnet_pipe.enable_vae_slicing()  # Thêm để giảm VRAM

def load_inpaint():
    global inpaint_pipe
    if inpaint_pipe is not None:
        return
    inpaint_pipe = StableDiffusionInpaintPipeline.from_pretrained(
        "runwayml/stable-diffusion-inpainting", torch_dtype=dtype
    )
    inpaint_pipe.safety_checker = None
    inpaint_pipe.scheduler = DPMSolverMultistepScheduler.from_config(inpaint_pipe.scheduler.config)
    inpaint_pipe.to(device)
    inpaint_pipe.enable_attention_slicing()
    inpaint_pipe.enable_vae_slicing()  # Thêm để giảm VRAM

def load_segmentation():
    global seg_model, seg_processor
    if seg_model is not None:
        return
    seg_processor = SegformerImageProcessor.from_pretrained("nvidia/segformer-b2-finetuned-ade-512-512")
    seg_model = SegformerForSemanticSegmentation.from_pretrained("nvidia/segformer-b2-finetuned-ade-512-512")
    seg_model.eval()

# -------------------- HELPERS --------------------
def get_segmentation(image):
    load_segmentation()
    inputs = seg_processor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = seg_model(**inputs)
    logits = outputs.logits
    upsampled = torch.nn.functional.interpolate(logits, size=image.size[::-1], mode="bilinear")
    seg = upsampled.argmax(dim=1).squeeze().cpu().numpy()
    return {
        "floor": (seg == ADE20K_FLOOR).astype(np.uint8),
        "wall": (seg == ADE20K_WALL).astype(np.uint8),
        "ceiling": (seg == ADE20K_CEILING).astype(np.uint8),
    }

def random_mask(surface_mask, obj_name):
    h, w = surface_mask.shape
    size = max(32, int(min(h, w) * OBJECT_SIZE.get(obj_name, 0.1)))
    ys, xs = np.where(surface_mask > 0)
    if len(xs) == 0:
        return None
    idx = np.random.randint(len(xs))
    cx, cy = xs[idx], ys[idx]
    x1 = max(0, cx - size//2)
    x2 = min(w, cx + size//2)
    y1 = max(0, cy - size//2)
    y2 = min(h, cy + size//2)
    mask = np.zeros((h, w), dtype=np.uint8)
    mask[y1:y2, x1:x2] = 255
    return mask

# Hàm add_object đã được gộp trong generate, không cần dùng riêng
# def add_object(...) - bỏ

# -------------------- GENERATION --------------------
def generate(image_path, style, objects, room=None):
    # Giới hạn số object
    if len(objects) > MAX_OBJECTS:
        objects = objects[:MAX_OBJECTS]

    # Load base image
    img = load_image(image_path).convert("RGB")
    w, h = img.size
    # Resize về kích thước tối đa IMAGE_MAX_SIZE
    if max(w, h) > IMAGE_MAX_SIZE:
        scale = IMAGE_MAX_SIZE / max(w, h)
        w, h = int(w * scale), int(h * scale)
    # Đảm bảo chia hết cho 8
    w, h = (w // 8) * 8, (h // 8) * 8
    img = img.resize((w, h), Image.LANCZOS)

    # Room type
    if room is None:
        room = "Living Room"
    room_name = ROOM_TYPE.get(room, "room")

    # Prompt cho base image
    if not objects:
        prompt = f"{STYLE_TEXT[style]} {room_name} interior, empty room. High quality photograph."
    else:
        obj_list = [OBJECT_DESC[o] for o in objects]
        prompt = f"{STYLE_TEXT[style]} featuring {', '.join(obj_list)}. High quality interior photograph."

    # ControlNet
    load_controlnet()
    np_img = np.array(img)
    canny = cv2.Canny(np_img, 100, 200)[:, :, None]
    canny = np.concatenate([canny, canny, canny], axis=2)
    canny_img = Image.fromarray(canny)

    gen = torch.Generator(device=device).manual_seed(42)

    # Sinh base image với số bước giảm
    base = controlnet_pipe(
        prompt, image=canny_img, negative_prompt=DEFAULT_NEGATIVE,
        num_inference_steps=CONTROLNET_STEPS, guidance_scale=7.5, generator=gen
    ).images[0]

    # Nếu không có object, trả về luôn
    if not objects:
        out_path = f"results/generated_{os.path.basename(image_path)}"
        base.save(out_path)
        return out_path

    # Segmentation một lần
    seg = get_segmentation(base)

    # Tạo mask tổng hợp
    combined_mask = np.zeros((h, w), dtype=np.uint8)
    for obj in objects:
        surface = OBJECT_SURFACE.get(obj, "floor")
        surf_mask = seg.get(surface, np.zeros_like(seg["floor"]))
        if np.sum(surf_mask) == 0:
            print(f"⚠️ No {surface} detected for {obj}, skip")
            continue
        mask = random_mask(surf_mask, obj)
        if mask is None:
            print(f"⚠️ No region for {obj}, skip")
            continue
        combined_mask = np.maximum(combined_mask, mask)

    # Nếu không có mask, trả về base
    if np.sum(combined_mask) == 0:
        out_path = f"results/generated_{os.path.basename(image_path)}"
        base.save(out_path)
        return out_path

    # Inpainting một lần
    load_inpaint()
    prompt_inpaint = f"{', '.join([OBJECT_DESC[o] for o in objects])} in a {room_name}, {STYLE_TEXT[style]} Photorealistic."
    mask_img = Image.fromarray(combined_mask).convert("L")
    result = inpaint_pipe(
        prompt=prompt_inpaint,
        image=base,
        mask_image=mask_img,
        negative_prompt=DEFAULT_NEGATIVE,
        num_inference_steps=INPAINT_STEPS,
        guidance_scale=7.5,
    ).images[0]

    out_path = f"results/generated_{os.path.basename(image_path)}"
    result.save(out_path)
    return out_path

# -------------------- API --------------------
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
os.makedirs("uploads", exist_ok=True)
os.makedirs("results", exist_ok=True)

tasks = {}

class GenReq(BaseModel):
    image_path: str
    style: str
    objects: List[str] = []
    room_type: Optional[str] = None
    custom_prompt: Optional[str] = None  # chưa sử dụng nhưng giữ để tương thích

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Not an image")
    path = f"uploads/{file.filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"image_path": path}

@app.post("/generate")
async def gen(req: GenReq, background: BackgroundTasks):
    tid = str(uuid.uuid4())
    tasks[tid] = {"status": "processing", "result": None, "error": None}
    def run():
        try:
            out = generate(req.image_path, req.style, req.objects, req.room_type)
            tasks[tid]["status"] = "completed"
            tasks[tid]["result"] = f"/results/{os.path.basename(out)}"
        except Exception as e:
            tasks[tid]["status"] = "failed"
            tasks[tid]["error"] = str(e)
    background.add_task(run)
    return {"task_id": tid}

@app.get("/status/{tid}")
def status(tid: str):
    if tid not in tasks:
        raise HTTPException(404, "Not found")
    return tasks[tid]

@app.get("/results/{filename}")
def result(filename: str):
    path = f"results/{filename}"
    if os.path.exists(path):
        return FileResponse(path)
    raise HTTPException(404, "Not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)