import os
import shutil

# To save resources and avoid waiting for 15GB+ model weights to download on every dev run,
# we simulate the AI logic first. If you want true inference, uncomment the Stable Diffusion imports.

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

# Set environment variable for MPS fallback to CPU for unsupported ops
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

# Set device to MPS for Apple Silicon Mac, else CPU
device = "mps" if torch.backends.mps.is_available() else "cpu"

# Global variables for models
pipe = None


def load_models():
    global pipe
    if pipe is not None:
        return

    print(f"[AI Engine] Using device: {device}")
    print("[AI Engine] Loading models (SD 1.5 + ControlNet Canny)...")
    try:
        # Use float32 on MPS to avoid black images (NaNs common in float16 on MPS)
        model_dtype = torch.float32 if device == "mps" else torch.float16

        controlnet = ControlNetModel.from_pretrained(
            "lllyasviel/sd-controlnet-canny", torch_dtype=model_dtype
        )
        pipe = StableDiffusionControlNetPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            controlnet=controlnet,
            torch_dtype=model_dtype,
        )

        # Completely disable safety checker
        pipe.safety_checker = None
        pipe.feature_extractor = None

        # Optimize for speed and memory (DPMSolver is very stable on Mac)
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        pipe.to(device)
        pipe.enable_attention_slicing()
        pipe.enable_vae_slicing()
        # pipe.enable_model_cpu_offload() # Uncomment if memory is still an issue
        print(f"[AI Engine] Models loaded successfully using {model_dtype}.")
    except Exception as e:
        print(f"[AI Engine] Failed to load models: {e}")
        traceback.print_exc()
        raise e


# Remove top level loading logic

import traceback


def generate_interior(image_path: str, style: str, room_type: str) -> str:
    """
    Simulates or runs the actual Stable Diffusion XL + ControlNet generation.
    Returns the path to the generated image.
    """
    try:
        return _generate_interior_logic(image_path, style, room_type)
    except Exception as e:
        error_msg = f"Error in generate_interior: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        with open("error_log.txt", "w") as f:
            f.write(error_msg)
        raise e


def _generate_interior_logic(image_path: str, style: str, room_type: str) -> str:
    # Mapping styles to detailed prompts
    style_prompts = {
        "Minimalist": "A high-resolution photo of a modern room transformed with a minimalist interior design. The room maintains its original spatial structure and camera angle. The background walls are painted a clean, bright white. Furnishings are extremely sparse and functional. In the center, there is a very simple, low-profile dining table with a smooth concrete or natural wood top, accompanied by a single, sculptural dark wood chair. A wall-mounted, ultra-thin TV is seamlessly integrated, with no visible wires or furniture below it. The curtains are simple, floor-to-ceiling sheer white linen. Minimalist decor, like one unique ceramic vase, is placed strategically. The lighting is soft and natural daylight, highlighting the clean lines and negative space. Professional architectural photography.",
        "Scandi": "A high-resolution photo of the same room with a cozy Scandinavian (Scandi) interior design. The original structure and camera perspective are identical. The space is filled with warm, natural materials. A dining table made of light-colored pine or oak wood is surrounded by four chairs with curved wooden backs and light beige upholstered seats. A simple, low-profile wooden TV console sits under a wall-mounted TV. Floor-to-ceiling curtains in a textured, light grey linen hang from a natural wood rod. The walls are painted a soft, pale grey. Cozy elements like a chunky wool blanket draped over a chair, a large Fiddle Leaf Fig plant near the window, and a framed landscape print are present. Natural daylight makes the room feel bright and airy. Professional architectural photography.",
        "Indochine": "A high-resolution photo of the identical room with a rich, decorative Indochine interior design. The spatial structure and camera angle are unchanged. The space features dark, carved wood and rattan furniture. A large, dark mahogany dining table is surrounded by four chairs with intricate rattan webbing on the backs. A traditional, ornate dark wood cabinet houses the TV or serves as a media console. Curtains are made of a rich, patterned fabric in muted colors like turquoise and gold. An accent wall is painted in a warm, earthy terracotta or deep blue. The lighting is warm and diffused, supplemented by traditional brass or ceramic lamps. A Chinese lacquer box and a brass lantern are used as decor. Professional architectural photography.",
        "Modern": "A high-resolution photo of the same room with a sleek, contemporary Modern interior design. The original room structure and camera perspective are perfectly preserved. The room features industrial materials and bold lines. A rectangular dining table with a dark, polished concrete or smoked glass top and black steel legs is surrounded by four chairs with mid-century modern design (e.g., molded plastic). A high-gloss, sleek media console sits under a wall-mounted TV. Modern roller shades or vertical blinds in a dark grey color control the light. An accent wall is painted a deep charcoal or navy. A striking, geometric pendant light fixture hangs from the ceiling. Abstract art with bold shapes is displayed. The lighting is crisp and cool. Professional architectural photography.",
    }

    # Style-specific parameters
    style_params = {
        "Minimalist": {"guidance_scale": 7.5, "num_inference_steps": 35},
        "Scandi": {"guidance_scale": 8.5, "num_inference_steps": 40},
        "Indochine": {"guidance_scale": 9.0, "num_inference_steps": 50},
        "Modern": {"guidance_scale": 8.5, "num_inference_steps": 45},
    }

    params = style_params.get(style, style_params["Modern"])
    guidance_scale = params["guidance_scale"]
    num_inference_steps = params["num_inference_steps"]

    prompt = style_prompts.get(style, style_prompts["Modern"])
    negative_prompt = "low quality, blurry, distorted, ugly, messy, person, text, watermark, deformed, bad anatomy"

    print(f"[AI Engine] Running inference for {image_path}")
    print(f"[AI Engine] Prompt: {prompt}")

    # Ensure models are loaded
    load_models()
    if pipe is None:
        raise RuntimeError(
            "AI Models were not initialized correctly. Please check api logs."
        )

    # Actual inference logic
    image = load_image(image_path).convert("RGB")
    print(f"[AI Engine] Original image size: {image.size}")

    # Resize image to a manageable size for SD 1.5 on MPS (max 768 on the long side recommended)
    max_size = 768
    if max(image.size) > max_size:
        print(f"[AI Engine] Resizing image from {image.size} to max {max_size}px")
        image.thumbnail((max_size, max_size), Image.LANCZOS)
        print(f"[AI Engine] New image size: {image.size}")

    # Preprocess image for Canny ControlNet
    image_np = np.array(image)
    low_threshold = 100
    high_threshold = 200
    image_canny = cv2.Canny(image_np, low_threshold, high_threshold)
    image_canny = image_canny[:, :, None]
    image_canny = np.concatenate([image_canny, image_canny, image_canny], axis=2)
    canny_image = Image.fromarray(image_canny)

    # Generate
    generator = torch.Generator(device=device).manual_seed(42)
    output = pipe(
        prompt,
        image=canny_image,
        negative_prompt=negative_prompt,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        generator=generator,
        controlnet_conditioning_scale=1.0,
    ).images[0]

    os.makedirs("results", exist_ok=True)
    filename = os.path.basename(image_path)
    result_path = f"results/generated_{filename}"

    output.save(result_path)
    print(f"[AI Engine] Finished. Saved at {result_path}")

    return result_path
