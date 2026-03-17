import os
import threading
import traceback
from typing import Optional
import torch
import numpy as np
import cv2
from PIL import Image
from diffusers import (
    StableDiffusionControlNetPipeline,
    ControlNetModel,
    DPMSolverMultistepScheduler,
)
from diffusers.utils import load_image
from api.config import settings

# Set environment variable for MPS fallback to CPU for unsupported ops
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

# Global variables for models
pipe = None
generation_lock = threading.Lock()

def load_models():
    global pipe
    if pipe is not None:
        return

    device = settings.device
    model_dtype = torch.float16 if settings.model_dtype == "float16" else torch.float32

    print(f"[AI Engine] Using device: {device}")
    print(f"[AI Engine] Loading models ({settings.base_model} + ControlNet)...")
    
    try:
        controlnet = ControlNetModel.from_pretrained(
            settings.controlnet_model, torch_dtype=model_dtype
        )
        pipe = StableDiffusionControlNetPipeline.from_pretrained(
            settings.base_model,
            controlnet=controlnet,
            torch_dtype=model_dtype,
        )

        # Completely disable safety checker
        pipe.safety_checker = None
        pipe.feature_extractor = None

        # Optimize for speed and memory
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        
        print(f"[AI Engine] Moving pipe to {device} with {model_dtype}...")
        pipe.to(device, dtype=model_dtype)
        pipe.enable_attention_slicing()
        pipe.enable_vae_slicing()
        
        print(f"[AI Engine] Models loaded successfully.")
    except Exception as e:
        print(f"[AI Engine] Failed to load models: {e}")
        traceback.print_exc()
        raise e

def generate_interior(
    image_path: str, 
    style: str, 
    room_type: str, 
    custom_prompt: Optional[str] = None,
    progress_callback: Optional[callable] = None
) -> str:
    with generation_lock:
        try:
            return _generate_interior_logic(image_path, style, room_type, custom_prompt, progress_callback)
        except Exception as e:
            error_msg = f"Error in generate_interior: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            raise e

def _generate_interior_logic(
    image_path: str, 
    style: str, 
    room_type: str, 
    custom_prompt: Optional[str] = None,
    progress_callback: Optional[callable] = None
) -> str:
    # Mapping styles to detailed prompts
    style_prompts = {
        "Minimalist": "A high-resolution photo of a modern room transformed with a minimalist interior design. The room maintains its original spatial structure and camera angle. The background walls are painted a clean, bright white. Furnishings are extremely sparse and functional. In the center, there is a very simple, low-profile dining table with a smooth concrete or natural wood top, accompanied by a single, sculptural dark wood chair. A wall-mounted, ultra-thin TV is seamlessly integrated, with no visible wires or furniture below it. The curtains are simple, floor-to-ceiling sheer white linen. Minimalist decor, like one unique ceramic vase, is placed strategically. The lighting is soft and natural daylight, highlighting the clean lines and negative space. Professional architectural photography.",
        "Scandi": "A high-resolution photo of the same room with a cozy Scandinavian (Scandi) interior design. The original structure and camera perspective are identical. The space is filled with warm, natural materials. A dining table made of light-colored pine or oak wood is surrounded by four chairs with curved wooden backs and light beige upholstered seats. A simple, low-profile wooden TV console sits under a wall-mounted TV. Floor-to-ceiling curtains in a textured, light grey linen hang from a natural wood rod. The walls are painted a soft, pale grey. Cozy elements like a chunky wool blanket draped over a chair, a large Fiddle Leaf Fig plant near the window, and a framed landscape print are present. Natural daylight makes the room feel bright and airy. Professional architectural photography.",
        "Indochine": "A high-resolution photo of the identical room with a rich, decorative Indochine interior design. The spatial structure and camera angle are unchanged. The space features dark, carved wood and rattan furniture. A large, dark mahogany dining table is surrounded by four chairs with intricate rattan webbing on the backs. A traditional, ornate dark wood cabinet houses the TV or serves as a media console. Curtains are made of a rich, patterned fabric in muted colors like turquoise and gold. An accent wall is painted in a warm, earthy terracotta or deep blue. The lighting is warm and diffused, supplemented by traditional brass or ceramic lamps. A Chinese lacquer box and a brass lantern are used as decor. Professional architectural photography.",
        "Modern": "A high-resolution photo of the same room with a sleek, contemporary Modern interior design. The original room structure and camera perspective are perfectly preserved. The room features industrial materials and bold lines. A rectangular dining table with a dark, polished concrete or smoked glass top and black steel legs is surrounded by four chairs with mid-century modern design (e.g., molded plastic). A high-gloss, sleek media console sits under a wall-mounted TV. Modern roller shades or vertical blinds in a dark grey color control the light. An accent wall is painted a deep charcoal or navy. A striking, geometric pendant light fixture hangs from the ceiling. Abstract art with bold shapes is displayed. The lighting is crisp and cool. Professional architectural photography.",
    }

    style_params = {
        "Minimalist": {"guidance_scale": 7.5, "num_inference_steps": 35},
        "Scandi": {"guidance_scale": 8.5, "num_inference_steps": 40},
        "Indochine": {"guidance_scale": 9.0, "num_inference_steps": 50},
        "Modern": {"guidance_scale": 8.5, "num_inference_steps": 45},
    }

    params = style_params.get(style, style_params["Modern"])
    guidance_scale = params["guidance_scale"]
    num_inference_steps = params["num_inference_steps"]

    prompt = custom_prompt if style == "Custom" and custom_prompt else style_prompts.get(style, style_prompts["Modern"])
    negative_prompt = "low quality, blurry, distorted, ugly, messy, person, text, watermark, deformed, bad anatomy"

    load_models()
    if pipe is None:
        raise RuntimeError("AI Models were not initialized correctly.")

    image = load_image(image_path).convert("RGB")
    
    max_size = 768
    width, height = image.size
    
    if max(width, height) > max_size:
        scale = max_size / max(width, height)
        width, height = int(width * scale), int(height * scale)
        
    width = (width // 8) * 8
    height = (height // 8) * 8
    
    image = image.resize((width, height), Image.LANCZOS)

    image_np = np.array(image)
    image_canny = cv2.Canny(image_np, 100, 200)
    image_canny = np.stack([image_canny]*3, axis=-1)
    canny_image = Image.fromarray(image_canny)

    generator = torch.Generator(device=settings.device).manual_seed(42)
    
    if hasattr(pipe.scheduler, "model_outputs"):
        pipe.scheduler.model_outputs = [None] * pipe.scheduler.config.solver_order
        
    output = pipe(
        prompt,
        image=canny_image,
        negative_prompt=negative_prompt,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        generator=generator,
        controlnet_conditioning_scale=1.0,
        callback=progress_callback,
        callback_steps=1,
    ).images[0]

    os.makedirs(settings.results_dir, exist_ok=True)
    filename = os.path.basename(image_path)
    result_path = os.path.join(settings.results_dir, f"generated_{filename}")

    output.save(result_path)
    return result_path
