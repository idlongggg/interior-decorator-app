"""
Prompt Builder Module for AI Interior Design.

Builds professional Stable Diffusion prompts from a style name and
a list of furniture/decor objects. Uses template-based approach 
(no LLM required) for fast, deterministic prompt generation.
"""

from typing import List, Optional

# Detailed object descriptions for professional prompts
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

# Style-specific modifiers that adjust the object description tone
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

# Room type modifiers
ROOM_DESCRIPTIONS = {
    "Living Room": "living room",
    "Bedroom": "bedroom",
    "Dining Room": "dining room",
    "Office": "home office",
    "Kitchen": "kitchen",
    "Bathroom": "bathroom",
    "Studio": "studio apartment",
}

# Default negative prompt
DEFAULT_NEGATIVE_PROMPT = (
    "low quality, blurry, distorted, ugly, messy, person, people, text, watermark, "
    "deformed, bad anatomy, disfigured, poorly drawn, extra limbs, mutation, "
    "out of frame, cropped, worst quality, low resolution, jpeg artifacts, "
    "cartoon, anime, sketch, drawing"
)


def build_prompt(
    style: str,
    objects_list: List[str],
    room_type: str = "Living Room",
    custom_prompt: Optional[str] = None,
) -> dict:
    """
    Build a professional SD prompt from style + objects checklist.
    
    Args:
        style: Style name (e.g. 'Minimalist', 'Modern')
        objects_list: List of object keys (e.g. ['sofa', 'coffee_table', 'rug'])
        room_type: Type of room
        custom_prompt: Optional override prompt
        
    Returns:
        Dict with 'prompt' and 'negative_prompt' keys
    """
    if style == "Custom" and custom_prompt:
        return {
            "prompt": custom_prompt,
            "negative_prompt": DEFAULT_NEGATIVE_PROMPT,
        }

    style_info = STYLE_MODIFIERS.get(style, STYLE_MODIFIERS["Modern"])
    room_desc = ROOM_DESCRIPTIONS.get(room_type, "room")

    # Build object descriptions
    obj_descriptions = []
    for obj in objects_list:
        desc = OBJECT_DESCRIPTIONS.get(obj, f"a {obj.replace('_', ' ')}")
        obj_descriptions.append(desc)

    # Construct the full prompt
    objects_text = ", ".join(obj_descriptions) if obj_descriptions else "tasteful furnishings"

    prompt = (
        f"{style_info['prefix']} {room_desc} featuring {objects_text}. "
        f"The room maintains its original spatial structure and camera angle. "
        f"Style elements: {style_info['tone']}. "
        f"Materials: {style_info['materials']}. "
        f"Lighting: {style_info['lighting']}. "
        f"{style_info['suffix']}"
    )

    print(f"[PromptBuilder] Generated prompt ({len(prompt)} chars): {prompt[:120]}...")

    return {
        "prompt": prompt,
        "negative_prompt": DEFAULT_NEGATIVE_PROMPT,
    }


def get_style_params(style: str) -> dict:
    """
    Get inference parameters optimized for each style.
    
    Returns:
        Dict with guidance_scale, num_inference_steps, controlnet_conditioning_scale
    """
    params = {
        "Minimalist": {
            "guidance_scale": 7.5,
            "num_inference_steps": 35,
            "controlnet_conditioning_scale": 0.8,
        },
        "Scandi": {
            "guidance_scale": 8.5,
            "num_inference_steps": 40,
            "controlnet_conditioning_scale": 0.85,
        },
        "Indochine": {
            "guidance_scale": 9.0,
            "num_inference_steps": 50,
            "controlnet_conditioning_scale": 0.9,
        },
        "Modern": {
            "guidance_scale": 8.5,
            "num_inference_steps": 45,
            "controlnet_conditioning_scale": 0.85,
        },
        "Japanese Zen": {
            "guidance_scale": 8.0,
            "num_inference_steps": 40,
            "controlnet_conditioning_scale": 0.85,
        },
        "Industrial": {
            "guidance_scale": 8.5,
            "num_inference_steps": 45,
            "controlnet_conditioning_scale": 0.85,
        },
    }
    return params.get(style, params["Modern"])
