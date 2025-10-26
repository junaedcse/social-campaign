"""
Validation utilities for Creative Automation Pipeline.
"""

from pathlib import Path
from typing import List
from src.config import settings
from src.utils.logger import app_logger


def validate_language_code(language: str) -> bool:
    """
    Validate if language code is supported.
    
    Args:
        language: Language code (e.g., 'en', 'es', 'fr')
        
    Returns:
        True if language is supported, False otherwise
    """
    supported = settings.supported_languages_list
    is_valid = language.lower() in supported
    
    if not is_valid:
        app_logger.warning(
            f"Language '{language}' not supported. Supported: {', '.join(supported)}"
        )
    
    return is_valid


def validate_aspect_ratio(aspect_ratio: str) -> bool:
    """
    Validate aspect ratio format.
    
    Args:
        aspect_ratio: Aspect ratio string (e.g., "16:9")
        
    Returns:
        True if valid format, False otherwise
    """
    try:
        parts = aspect_ratio.split(":")
        if len(parts) != 2:
            return False
        
        w, h = map(int, parts)
        return w > 0 and h > 0
    except (ValueError, AttributeError):
        return False


def validate_file_path(file_path: Path, must_exist: bool = False) -> bool:
    """
    Validate file path.
    
    Args:
        file_path: Path to validate
        must_exist: Whether file must already exist
        
    Returns:
        True if valid, False otherwise
    """
    if must_exist:
        return file_path.exists() and file_path.is_file()
    
    # Check if parent directory exists or can be created
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        return True
    except (PermissionError, OSError) as e:
        app_logger.error(f"Cannot access path {file_path}: {e}")
        return False


def validate_image_file(file_path: Path) -> bool:
    """
    Validate if file is a supported image format.
    
    Args:
        file_path: Path to image file
        
    Returns:
        True if valid image format, False otherwise
    """
    supported_formats = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}
    return file_path.suffix.lower() in supported_formats