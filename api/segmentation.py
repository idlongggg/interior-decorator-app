"""
Semantic Segmentation Module for Room Space Analysis.

Uses SegFormer (nvidia/segformer-b2-finetuned-ade-512-512) to detect
floor, wall, ceiling regions in a room image. Then generates object placement
masks automatically within detected regions.
"""

import numpy as np
from PIL import Image
from typing import Dict, List, Tuple, Optional
import torch
from transformers import SegformerForSemanticSegmentation, SegformerImageProcessor
from scipy import ndimage

# ADE20K class indices for room regions
# Full list: https://docs.google.com/spreadsheets/d/1se8YEtb2detS7OuPE86fXGyD269pMycAWe2mtKUj2W8
ADE20K_FLOOR_IDX = 3       # "floor"
ADE20K_WALL_IDX = 0        # "wall"
ADE20K_CEILING_IDX = 5     # "ceiling"
ADE20K_WINDOW_IDX = 8      # "windowpane"
ADE20K_DOOR_IDX = 14       # "door"
ADE20K_TABLE_IDX = 15      # "table"
ADE20K_CHAIR_IDX = 19      # "chair"
ADE20K_SOFA_IDX = 23       # "sofa"
ADE20K_BED_IDX = 7         # "bed"
ADE20K_CABINET_IDX = 10    # "cabinet"
ADE20K_SHELF_IDX = 24      # "shelf"
ADE20K_CURTAIN_IDX = 18    # "curtain"
ADE20K_RUG_IDX = 28        # "rug"
ADE20K_LAMP_IDX = 36       # "lamp"
ADE20K_PAINTING_IDX = 22   # "painting"

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
    "table_lamp": "floor",  # placed on furniture but mask on floor region
    "vase": "floor",
    "cushion": "floor",
}

# Approximate relative sizes for objects (as fraction of the surface area)
OBJECT_SIZE_RATIO = {
    "sofa": 0.25,
    "coffee_table": 0.10,
    "dining_table": 0.18,
    "chair": 0.06,
    "armchair": 0.10,
    "rug": 0.20,
    "plant": 0.04,
    "floor_lamp": 0.03,
    "tv_stand": 0.12,
    "bookshelf": 0.10,
    "bed": 0.30,
    "desk": 0.12,
    "mirror": 0.08,
    "painting": 0.06,
    "wall_shelf": 0.08,
    "clock": 0.03,
    "sconce": 0.02,
    "pendant_light": 0.05,
    "chandelier": 0.08,
    "ceiling_fan": 0.10,
    "table_lamp": 0.03,
    "vase": 0.02,
    "cushion": 0.03,
}

# Global model references
seg_model = None
seg_processor = None


def load_segmentation_model():
    """Load SegFormer model for semantic segmentation (lazy loading)."""
    global seg_model, seg_processor
    if seg_model is not None:
        return

    print("[Segmentation] Loading SegFormer model...")
    model_name = "nvidia/segformer-b2-finetuned-ade-512-512"
    seg_processor = SegformerImageProcessor.from_pretrained(model_name)
    seg_model = SegformerForSemanticSegmentation.from_pretrained(model_name)
    seg_model.eval()
    print("[Segmentation] SegFormer model loaded successfully.")


def get_room_segments(image: Image.Image) -> Dict[str, np.ndarray]:
    """
    Segment the room image into floor, wall, ceiling regions.
    
    Args:
        image: PIL Image of the room
        
    Returns:
        Dict with keys 'floor', 'wall', 'ceiling' mapping to binary masks (H, W)
    """
    load_segmentation_model()

    # Preprocess
    inputs = seg_processor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = seg_model(**inputs)

    # Get segmentation map
    logits = outputs.logits  # (1, num_classes, H/4, W/4)

    # Upsample to original image size
    upsampled = torch.nn.functional.interpolate(
        logits,
        size=image.size[::-1],  # (H, W)
        mode="bilinear",
        align_corners=False,
    )
    seg_map = upsampled.argmax(dim=1).squeeze().cpu().numpy()  # (H, W)

    # Extract region masks
    floor_mask = (seg_map == ADE20K_FLOOR_IDX).astype(np.uint8)
    wall_mask = (seg_map == ADE20K_WALL_IDX).astype(np.uint8)
    ceiling_mask = (seg_map == ADE20K_CEILING_IDX).astype(np.uint8)

    # Clean up masks with morphological operations
    kernel = np.ones((5, 5), np.uint8)
    for mask_name in ['floor_mask', 'wall_mask', 'ceiling_mask']:
        mask = locals()[mask_name]
        mask = ndimage.binary_closing(mask, kernel, iterations=2).astype(np.uint8)
        mask = ndimage.binary_opening(mask, kernel, iterations=1).astype(np.uint8)
        if mask_name == 'floor_mask':
            floor_mask = mask
        elif mask_name == 'wall_mask':
            wall_mask = mask
        else:
            ceiling_mask = mask

    print(f"[Segmentation] Floor: {floor_mask.sum()} px, Wall: {wall_mask.sum()} px, Ceiling: {ceiling_mask.sum()} px")

    return {
        "floor": floor_mask,
        "wall": wall_mask,
        "ceiling": ceiling_mask,
        "full_segmap": seg_map,
    }


def generate_object_mask_within_area(
    surface_mask: np.ndarray,
    obj_name: str,
    image_size: Tuple[int, int],
    occupied_mask: np.ndarray = None,
    padding: int = 10,
) -> Optional[np.ndarray]:
    """
    Generate a rectangular mask for an object within the given surface area.
    
    Places object in an unoccupied region of the surface mask, avoiding overlap
    with already-placed objects.
    
    Args:
        surface_mask: Binary mask of the surface (floor/wall/ceiling)
        obj_name: Name of the object to place
        image_size: (width, height) of the image
        occupied_mask: Binary mask of already-occupied regions
        padding: Padding around placed objects
        
    Returns:
        Binary mask (H, W) for the object, or None if no space found
    """
    h, w = surface_mask.shape[:2]
    size_ratio = OBJECT_SIZE_RATIO.get(obj_name, 0.08)

    # Calculate available area
    available = surface_mask.copy()
    if occupied_mask is not None:
        # Dilate occupied mask to add spacing between objects
        dilated_occupied = ndimage.binary_dilation(
            occupied_mask, iterations=padding
        ).astype(np.uint8)
        available = available & (~dilated_occupied).astype(np.uint8)

    # Find the bounding box of available area
    coords = np.argwhere(available > 0)
    if len(coords) < 100:  # Too little space
        print(f"[Segmentation] Not enough space for {obj_name}")
        return None

    min_y, min_x = coords.min(axis=0)
    max_y, max_x = coords.max(axis=0)

    avail_h = max_y - min_y
    avail_w = max_x - min_x

    # Calculate object dimensions based on size ratio
    surface_area = available.sum()
    obj_area = int(surface_area * size_ratio)
    
    # Aspect ratio varies by object type
    aspect_ratios = {
        "sofa": 2.5,
        "coffee_table": 1.8,
        "dining_table": 1.5,
        "rug": 1.6,
        "bed": 1.4,
        "tv_stand": 3.0,
        "bookshelf": 0.5,
        "mirror": 0.7,
        "painting": 1.3,
        "wall_shelf": 3.0,
        "desk": 1.8,
    }
    aspect = aspect_ratios.get(obj_name, 1.0)

    obj_w = int(np.sqrt(obj_area * aspect))
    obj_h = int(obj_area / obj_w) if obj_w > 0 else int(np.sqrt(obj_area))

    # Clamp to available area
    obj_w = min(obj_w, avail_w - 2 * padding)
    obj_h = min(obj_h, avail_h - 2 * padding)

    if obj_w <= 0 or obj_h <= 0:
        print(f"[Segmentation] Object {obj_name} too large for available space")
        return None

    # Find a good placement position
    # Strategy: scan from center outward to find a region with maximum overlap with surface mask
    center_y = (min_y + max_y) // 2
    center_x = (min_x + max_x) // 2

    best_pos = None
    best_overlap = 0

    # Search grid (center-outward spiral approximation)
    step_y = max(obj_h // 3, 5)
    step_x = max(obj_w // 3, 5)

    for dy in range(-avail_h // 2, avail_h // 2, step_y):
        for dx in range(-avail_w // 2, avail_w // 2, step_x):
            cy = center_y + dy
            cx = center_x + dx

            y1 = max(0, cy - obj_h // 2)
            y2 = min(h, y1 + obj_h)
            x1 = max(0, cx - obj_w // 2)
            x2 = min(w, x1 + obj_w)

            if y2 - y1 < obj_h * 0.8 or x2 - x1 < obj_w * 0.8:
                continue

            region = available[y1:y2, x1:x2]
            overlap = region.sum() / region.size

            if overlap > best_overlap:
                best_overlap = overlap
                best_pos = (y1, x1, y2, x2)

    if best_pos is None or best_overlap < 0.5:
        print(f"[Segmentation] Could not find good position for {obj_name} (best overlap: {best_overlap:.2f})")
        return None

    # Create mask
    obj_mask = np.zeros((h, w), dtype=np.uint8)
    y1, x1, y2, x2 = best_pos
    obj_mask[y1:y2, x1:x2] = 1

    # Intersect with surface mask to ensure mask stays within surface
    obj_mask = obj_mask & surface_mask

    print(f"[Segmentation] Placed {obj_name} at ({x1},{y1})-({x2},{y2}), overlap={best_overlap:.2f}")
    return obj_mask


def generate_all_object_masks(
    segments: Dict[str, np.ndarray],
    objects_list: List[str],
    image_size: Tuple[int, int],
) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
    """
    Generate masks for all requested objects within the appropriate room regions.
    
    Args:
        segments: Output from get_room_segments()
        objects_list: List of object names to place
        image_size: (width, height) of the image
        
    Returns:
        Tuple of (combined_inpainting_mask, individual_masks_dict)
    """
    h, w = image_size[1], image_size[0]
    combined_mask = np.zeros((h, w), dtype=np.uint8)
    occupied_mask = np.zeros((h, w), dtype=np.uint8)
    individual_masks = {}

    # Sort objects by size (largest first for better placement)
    sorted_objects = sorted(
        objects_list,
        key=lambda x: OBJECT_SIZE_RATIO.get(x, 0.08),
        reverse=True,
    )

    for obj_name in sorted_objects:
        surface_type = OBJECT_SURFACE_MAP.get(obj_name, "floor")
        surface_mask = segments.get(surface_type)

        if surface_mask is None or surface_mask.sum() < 100:
            print(f"[Segmentation] No {surface_type} detected for {obj_name}, skipping.")
            continue

        obj_mask = generate_object_mask_within_area(
            surface_mask, obj_name, image_size, occupied_mask
        )

        if obj_mask is not None:
            individual_masks[obj_name] = obj_mask
            combined_mask = combined_mask | obj_mask
            occupied_mask = occupied_mask | obj_mask

    print(f"[Segmentation] Generated masks for {len(individual_masks)}/{len(objects_list)} objects")
    return combined_mask, individual_masks
