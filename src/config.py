"""
Configuration management for Creative Automation Pipeline.
Handles environment variables and application settings.
"""

from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    openai_api_key: str = Field(default="", description="OpenAI API key")
    
    # Application Settings
    log_level: str = Field(default="INFO", description="Logging level")
    max_image_size: int = Field(default=1024, description="Maximum image dimension")
    
    # Supported Languages
    supported_languages: str = Field(
        default="en,es,fr,de,ja",
        description="Comma-separated list of supported language codes"
    )
    
    # Directory Settings
    output_base_dir: Path = Field(default=Path("data/output"))
    input_assets_dir: Path = Field(default=Path("data/input/assets"))
    input_briefs_dir: Path = Field(default=Path("data/input/briefs"))
    
    # Image Generation Settings
    dalle_model: str = Field(default="dall-e-3", description="DALL-E model version")
    dalle_quality: str = Field(default="standard", description="Image quality: standard or hd")
    dalle_size: str = Field(default="1024x1024", description="Generated image size")
    
    # Translation Settings
    translation_model: str = Field(default="gpt-4o-mini", description="Model for translations")
    
    # Aspect Ratios
    aspect_ratios: List[str] = Field(
        default=["1:1", "9:16", "16:9"],
        description="Target aspect ratios for output"
    )
    
    # Text Overlay Settings
    text_font_size: int = Field(default=20, description="Font size for text overlays")
    text_shadow_enabled: bool = Field(default=False, description="Enable shadow effect on text")
    text_shadow_offset: int = Field(default=2, description="Shadow offset in pixels")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @property
    def supported_languages_list(self) -> List[str]:
        """Return supported languages as a list."""
        return [lang.strip() for lang in self.supported_languages.split(",")]
    
    def get_aspect_ratio_dimensions(self, aspect_ratio: str, base_size: int = 1024) -> tuple[int, int]:
        """
        Calculate dimensions for a given aspect ratio.
        
        Args:
            aspect_ratio: Aspect ratio in format "W:H"
            base_size: Base dimension to calculate from
            
        Returns:
            Tuple of (width, height)
        """
        w, h = map(int, aspect_ratio.split(":"))
        
        if w > h:
            width = base_size
            height = int(base_size * h / w)
        elif h > w:
            height = base_size
            width = int(base_size * w / h)
        else:
            width = height = base_size
            
        return width, height
    
    def ensure_directories(self):
        """Create necessary directories if they don't exist."""
        self.output_base_dir.mkdir(parents=True, exist_ok=True)
        self.input_assets_dir.mkdir(parents=True, exist_ok=True)
        self.input_briefs_dir.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()