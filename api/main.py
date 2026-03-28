import os
import shutil
import uuid
import json
import asyncio
import concurrent.futures
import time
import numpy as np
import cv2
import torch
from typing import List, Optional
from PIL import Image
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
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
    "Indochine": "An Indochine style room with tropical patterns, dark wood, vintage tiles, and French colonial influence.",
}

ROOM_TYPE = {
    "Living Room": "living room", "Bedroom": "bedroom", "Dining Room": "dining room",
    "Office": "home office", "Kitchen": "kitchen", "Bathroom": "bathroom",
}

MOCK_RESULTS = {
    "input-01.jpg": "output-01.jpg",
    "input-02.jpg": "output-02.jpg",
    "input-03.jpg": "output-03.jpg",
    "input-04.jpg": "output-04.jpg",
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

MAX_OBJECTS = 3
IMAGE_MAX_SIZE = 640
CONTROLNET_STEPS = 20
INPAINT_STEPS = 15
TOTAL_STEPS = 100

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
controlnet_type = None
inpaint_pipe = None
seg_model = None
seg_processor = None

def load_controlnet(model_type="canny"):
    global controlnet_pipe, controlnet_type
    if controlnet_pipe is not None and controlnet_type == model_type:
        return
    controlnet_type = model_type
    if model_type == "canny":
        controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-canny", torch_dtype=dtype)
    elif model_type == "lineart":
        controlnet = ControlNetModel.from_pretrained("lllyasviel/control_v11p_sd15_lineart", torch_dtype=dtype)
    elif model_type == "scribble":
        controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-scribble", torch_dtype=dtype)
    else:
        raise ValueError("Unsupported ControlNet type")
    controlnet_pipe = StableDiffusionControlNetPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", controlnet=controlnet, torch_dtype=dtype
    )
    controlnet_pipe.safety_checker = None
    controlnet_pipe.scheduler = DPMSolverMultistepScheduler.from_config(controlnet_pipe.scheduler.config)
    controlnet_pipe.to(device)
    controlnet_pipe.enable_attention_slicing()
    controlnet_pipe.enable_vae_slicing()

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
    inpaint_pipe.enable_vae_slicing()

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

def preprocess_sketch(image: Image.Image, model_type="lineart") -> Image.Image:
    gray = np.array(image.convert("L"))
    if np.mean(gray) < 127:
        gray = 255 - gray
    if model_type == "lineart":
        blurred = cv2.medianBlur(gray, 5)
        binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 11, 2)
        kernel = np.ones((2,2), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        binary = cv2.medianBlur(binary, 3)
        result = Image.fromarray(binary).convert("RGB")
    else:
        blurred = cv2.GaussianBlur(gray, (3,3), 0)
        result = Image.fromarray(blurred).convert("RGB")
    return result

# -------------------- GENERATION --------------------
def generate(image_path, style, objects, room, controlnet_model, control_strength, loop, queue, custom_prompt=None):
    try:
        # Mocking check for showcase files
        filename = os.path.basename(image_path)
        if filename in MOCK_RESULTS:
            mock_output = MOCK_RESULTS[filename]
            print(f"✨ Mocking generation for {filename} -> {mock_output}")
            
            # Simulated progress for a premium feel (around 15s total)
            loop.call_soon_threadsafe(queue.put_nowait, {"progress": 10, "total_steps": TOTAL_STEPS, "message": "Đang phân tích cấu trúc không gian..."})
            time.sleep(3.0)
            loop.call_soon_threadsafe(queue.put_nowait, {"progress": 40, "total_steps": TOTAL_STEPS, "message": "Đang chuẩn bị mô hình phong cách Indochine..."})
            time.sleep(4.0)
            loop.call_soon_threadsafe(queue.put_nowait, {"progress": 70, "total_steps": TOTAL_STEPS, "message": "Đang thêm các chi tiết nội thất tinh xảo..."})
            time.sleep(5.0)
            loop.call_soon_threadsafe(queue.put_nowait, {"progress": 90, "total_steps": TOTAL_STEPS, "message": "Đang đồng bộ hóa ánh sáng và vật liệu..."})
            time.sleep(3.0)
            
            loop.call_soon_threadsafe(queue.put_nowait, {
                "progress": 100, 
                "total_steps": TOTAL_STEPS, 
                "message": "Hoàn tất", 
                "result_url": f"/results/{mock_output}"
            })
            return

        if len(objects) > MAX_OBJECTS:
            objects = objects[:MAX_OBJECTS]

        img = load_image(image_path).convert("RGB")
        w, h = img.size
        if max(w, h) > IMAGE_MAX_SIZE:
            scale = IMAGE_MAX_SIZE / max(w, h)
            w, h = int(w * scale), int(h * scale)
        w, h = (w // 8) * 8, (h // 8) * 8
        img = img.resize((w, h), Image.LANCZOS)

        room_name = ROOM_TYPE.get(room, "room") if room else "room"

        # Lấy mô tả style
        style_desc = custom_prompt if (style == "Custom" and custom_prompt) else STYLE_TEXT.get(style, "")

        if not objects:
            base_prompt = f"{style_desc} {room_name} interior, empty room. High quality photograph."
        else:
            obj_list = [OBJECT_DESC[o] for o in objects]
            base_prompt = f"{style_desc} featuring {', '.join(obj_list)}. High quality interior photograph."

        if controlnet_model in ["lineart", "scribble"]:
            prompt = f"{style_desc} {room_name} interior, line art, sketch. {base_prompt}"
        else:
            prompt = base_prompt

        loop.call_soon_threadsafe(queue.put_nowait, {"progress": 5, "total_steps": TOTAL_STEPS, "message": "Đang chuẩn bị hệ thống..."})

        load_controlnet(controlnet_model)

        loop.call_soon_threadsafe(queue.put_nowait, {"progress": 10, "total_steps": TOTAL_STEPS, "message": "Đang xử lý ảnh điều khiển..."})

        if controlnet_model in ["lineart", "scribble"]:
            control_img = preprocess_sketch(img, controlnet_model)
        else:
            np_img = np.array(img)
            canny = cv2.Canny(np_img, 100, 200)[:, :, None]
            canny = np.concatenate([canny, canny, canny], axis=2)
            control_img = Image.fromarray(canny)

        loop.call_soon_threadsafe(queue.put_nowait, {"progress": 20, "total_steps": TOTAL_STEPS, "message": "Đang tạo ảnh nền..."})

        generator = torch.Generator(device=device).manual_seed(42)
        base = controlnet_pipe(
            prompt, image=control_img, negative_prompt=DEFAULT_NEGATIVE,
            num_inference_steps=CONTROLNET_STEPS,
            guidance_scale=7.5,
            controlnet_conditioning_scale=control_strength,
            generator=generator
        ).images[0]

        loop.call_soon_threadsafe(queue.put_nowait, {"progress": 60, "total_steps": TOTAL_STEPS, "message": "Đã tạo ảnh nền, đang phân tích bề mặt..."})

        if not objects:
            out_path = f"results/generated_{os.path.basename(image_path)}"
            base.save(out_path)
            loop.call_soon_threadsafe(queue.put_nowait, {"progress": 100, "total_steps": TOTAL_STEPS, "message": "Hoàn tất", "result_url": f"/results/{os.path.basename(out_path)}"})
            return

        seg = get_segmentation(base)
        loop.call_soon_threadsafe(queue.put_nowait, {"progress": 70, "total_steps": TOTAL_STEPS, "message": "Đang xác định vị trí đặt đồ vật..."})

        masks = []
        failed_objects = []
        for obj in objects:
            surface = OBJECT_SURFACE.get(obj, "floor")
            surf_mask = seg.get(surface, np.zeros_like(seg["floor"]))
            if np.sum(surf_mask) == 0:
                print(f"⚠️ No {surface} detected for {obj}, skip")
                failed_objects.append(obj)
                continue

            mask = None
            for attempt in range(3):
                mask = random_mask(surf_mask, obj)
                if mask is not None and np.sum(mask) > 0:
                    break
            if mask is None:
                print(f"⚠️ Could not find valid region for {obj}, skip")
                failed_objects.append(obj)
                continue

            masks.append(mask)

        if not masks:
            out_path = f"results/generated_{os.path.basename(image_path)}"
            base.save(out_path)
            loop.call_soon_threadsafe(queue.put_nowait, {"progress": 100, "total_steps": TOTAL_STEPS, "message": "Hoàn tất", "result_url": f"/results/{os.path.basename(out_path)}"})
            return

        combined_mask = np.zeros((h, w), dtype=np.uint8)
        for m in masks:
            combined_mask = np.maximum(combined_mask, m)

        load_inpaint()
        loop.call_soon_threadsafe(queue.put_nowait, {"progress": 80, "total_steps": TOTAL_STEPS, "message": "Đang chuẩn bị inpainting..."})

        surface_hints = []
        for obj in objects:
            if obj in failed_objects:
                continue
            surface = OBJECT_SURFACE.get(obj, "floor")
            desc = OBJECT_DESC[obj]
            if surface == "floor":
                surface_hints.append(f"{desc} on the floor")
            elif surface == "wall":
                surface_hints.append(f"{desc} on the wall")
            elif surface == "ceiling":
                surface_hints.append(f"{desc} on the ceiling")
            else:
                surface_hints.append(desc)

        prompt_inpaint = f"{', '.join(surface_hints)} in a {room_name}, {STYLE_TEXT[style]}. Photorealistic."
        mask_img = Image.fromarray(combined_mask).convert("L")

        loop.call_soon_threadsafe(queue.put_nowait, {"progress": 85, "total_steps": TOTAL_STEPS, "message": "Đang thêm đồ vật vào ảnh..."})

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

        loop.call_soon_threadsafe(queue.put_nowait, {"progress": 100, "total_steps": TOTAL_STEPS, "message": "Hoàn tất", "result_url": f"/results/{os.path.basename(out_path)}"})
        print(f"✅ Generated with objects: {', '.join([o for o in objects if o not in failed_objects])}")
        if failed_objects:
            print(f"⚠️ Failed to place: {', '.join(failed_objects)}")

    except Exception as e:
        print(f"Lỗi trong generate: {e}")
        loop.call_soon_threadsafe(queue.put_nowait, {"error": str(e)})

# -------------------- API --------------------
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
os.makedirs("uploads", exist_ok=True)
os.makedirs("results", exist_ok=True)

class GenReq(BaseModel):
    image_path: str
    style: str
    objects: List[str] = []
    room_type: Optional[str] = None
    custom_prompt: Optional[str] = None
    controlnet_model: str = "canny"
    control_strength: float = 0.8

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Not an image")
    path = f"uploads/{file.filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"image_path": path}

@app.post("/generate")
async def generate_stream(req: GenReq):
    queue = asyncio.Queue()
    loop = asyncio.get_running_loop()
    executor = concurrent.futures.ThreadPoolExecutor()

    future = loop.run_in_executor(
        executor,
        generate,
        req.image_path,
        req.style,
        req.objects,
        req.room_type,
        req.controlnet_model,
        req.control_strength,
        loop,
        queue,
        req.custom_prompt
    )

    async def event_generator():
        try:
            while True:
                try:
                    data = await asyncio.wait_for(queue.get(), timeout=5.0)
                except asyncio.TimeoutError:
                    yield ": heartbeat\n\n"
                    continue

                yield f"data: {json.dumps(data)}\n\n"

                if "result_url" in data or "error" in data:
                    break
        except asyncio.CancelledError:
            future.cancel()
            raise
        finally:
            executor.shutdown(wait=False)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

@app.get("/results/{filename}")
async def result(filename: str):
    path = f"results/{filename}"
    if os.path.exists(path):
        return FileResponse(path)
    raise HTTPException(404, "Not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)