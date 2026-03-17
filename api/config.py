import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        protected_namespaces=()
    )
    
    app_name: str = "AI Interior Decorator API"
    device: str = "cpu"
    model_dtype: str = "float32"
    port: int = 8001
    
    # Paths
    uploads_dir: str = "uploads"
    results_dir: str = "results"
    
    # Model IDs
    controlnet_model: str = "lllyasviel/sd-controlnet-canny"
    base_model: str = "runwayml/stable-diffusion-v1-5"

settings = Settings()

# Post-initialization to detect device if not set in env
if os.environ.get("DEVICE") is None:
    import torch
    if torch.cuda.is_available():
        settings.device = "cuda"
    elif torch.backends.mps.is_available():
        settings.device = "mps"
    else:
        settings.device = "cpu"

if os.environ.get("MODEL_DTYPE") is None:
    settings.model_dtype = "float16" if settings.device == "cuda" else "float32"
