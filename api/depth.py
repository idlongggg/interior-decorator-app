"""
Depth Estimation Module for ControlNet conditioning.

Uses Intel DPT (MiDaS) model to generate depth maps from room images.
The depth map preserves room structure (walls, floor, windows) for
ControlNet to maintain spatial consistency during inpainting.
"""

import numpy as np
from PIL import Image
import torch
from transformers import DPTForDepthEstimation, DPTImageProcessor

# Global model references
depth_model = None
depth_processor = None


def load_depth_model():
    """Load DPT depth estimation model (lazy loading)."""
    global depth_model, depth_processor
    if depth_model is not None:
        return

    print("[Depth] Loading Intel DPT-Large depth model...")
    model_name = "Intel/dpt-large"
    depth_processor = DPTImageProcessor.from_pretrained(model_name)
    depth_model = DPTForDepthEstimation.from_pretrained(model_name)
    depth_model.eval()
    print("[Depth] DPT depth model loaded successfully.")


def estimate_depth(image: Image.Image) -> Image.Image:
    """
    Generate a depth map from a room image.
    
    Args:
        image: PIL Image of the room (RGB)
        
    Returns:
        PIL Image of the depth map (RGB, same size as input)
    """
    load_depth_model()

    original_size = image.size  # (W, H)

    # Preprocess
    inputs = depth_processor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = depth_model(**inputs)
        predicted_depth = outputs.predicted_depth

    # Interpolate to original size
    prediction = torch.nn.functional.interpolate(
        predicted_depth.unsqueeze(1),
        size=original_size[::-1],  # (H, W)
        mode="bicubic",
        align_corners=False,
    ).squeeze()

    # Normalize to 0-255
    depth_np = prediction.cpu().numpy()
    depth_min = depth_np.min()
    depth_max = depth_np.max()

    if depth_max - depth_min > 0:
        depth_normalized = ((depth_np - depth_min) / (depth_max - depth_min) * 255).astype(np.uint8)
    else:
        depth_normalized = np.zeros_like(depth_np, dtype=np.uint8)

    # Convert to 3-channel RGB image (required by ControlNet)
    depth_image = Image.fromarray(depth_normalized).convert("RGB")

    print(f"[Depth] Generated depth map: {depth_image.size}")
    return depth_image
