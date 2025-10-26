"""
Asset Manager Service
Manages loading and checking of existing product images.
"""

from pathlib import Path
from typing import Optional, Dict
from PIL import Image
from src.config import settings
from src.utils.logger import app_logger
from src.utils.validators import validate_image_file


class AssetManager:
    """Manages campaign asset files."""
    
    def __init__(self, assets_dir: Optional[Path] = None):
        """
        Initialize AssetManager.
        
        Args:
            assets_dir: Directory containing asset files (defaults to config)
        """
        self.assets_dir = assets_dir or settings.input_assets_dir
        self.assets_dir = Path(self.assets_dir)
        
        if not self.assets_dir.exists():
            app_logger.warning(f"Assets directory does not exist: {self.assets_dir}")
            self.assets_dir.mkdir(parents=True, exist_ok=True)
        
        app_logger.info(f"AssetManager initialized with directory: {self.assets_dir}")
    
    def asset_exists(self, filename: str) -> bool:
        """
        Check if an asset file exists.
        
        Args:
            filename: Name of the asset file
            
        Returns:
            True if asset exists, False otherwise
        """
        filepath = self.assets_dir / filename
        exists = filepath.exists() and filepath.is_file()
        
        if exists:
            app_logger.debug(f" Asset found: {filename}")
        else:
            app_logger.debug(f" Asset not found: {filename}")
        
        return exists
    
    def get_asset_path(self, filename: str) -> Optional[Path]:
        """
        Get the full path to an asset file if it exists.
        
        Args:
            filename: Name of the asset file
            
        Returns:
            Path object if file exists, None otherwise
        """
        if self.asset_exists(filename):
            return self.assets_dir / filename
        return None
    
    def load_image(self, filename: str) -> Optional[Image.Image]:
        """
        Load an image asset.
        
        Args:
            filename: Name of the image file
            
        Returns:
            PIL Image object if successful, None otherwise
        """
        filepath = self.get_asset_path(filename)
        
        if not filepath:
            app_logger.warning(f"Cannot load image: {filename} not found")
            return None
        
        if not validate_image_file(filepath):
            app_logger.error(f"Invalid image file format: {filename}")
            return None
        
        try:
            img = Image.open(filepath)
            app_logger.info(f" Loaded image: {filename} ({img.size[0]}x{img.size[1]})")
            return img
            
        except Exception as e:
            app_logger.error(f"Failed to load image {filename}: {e}")
            return None
    
    def save_image(self, image: Image.Image, filename: str, optimize: bool = True) -> bool:
        """
        Save an image to the assets directory.
        
        Args:
            image: PIL Image object
            filename: Output filename
            optimize: Whether to optimize the image
            
        Returns:
            True if successful, False otherwise
        """
        try:
            filepath = self.assets_dir / filename
            image.save(filepath, optimize=optimize)
            
            size = filepath.stat().st_size
            app_logger.info(f" Saved image: {filename} ({size:,} bytes)")
            return True
            
        except Exception as e:
            app_logger.error(f"Failed to save image {filename}: {e}")
            return False
    
    def get_image_info(self, filename: str) -> Optional[Dict]:
        """
        Get information about an image asset.
        
        Args:
            filename: Name of the image file
            
        Returns:
            Dictionary with image info or None
        """
        filepath = self.get_asset_path(filename)
        
        if not filepath:
            return None
        
        try:
            img = Image.open(filepath)
            info = {
                'filename': filename,
                'path': str(filepath),
                'size': filepath.stat().st_size,
                'dimensions': img.size,
                'format': img.format,
                'mode': img.mode
            }
            app_logger.debug(f"Image info for {filename}: {info}")
            return info
            
        except Exception as e:
            app_logger.error(f"Failed to get image info for {filename}: {e}")
            return None
    
    def list_assets(self) -> list[str]:
        """
        List all available asset files.
        
        Returns:
            List of asset filenames
        """
        if not self.assets_dir.exists():
            return []
        
        assets = []
        for ext in ['.png', '.jpg', '.jpeg', '.webp', '.gif']:
            assets.extend([f.name for f in self.assets_dir.glob(f'*{ext}')])
        
        app_logger.info(f"Found {len(assets)} assets in {self.assets_dir}")
        return sorted(assets)
    
    def validate_asset(self, filename: str) -> tuple[bool, Optional[str]]:
        """
        Validate an asset file.
        
        Args:
            filename: Name of the asset file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.asset_exists(filename):
            return False, f"Asset file not found: {filename}"
        
        filepath = self.assets_dir / filename
        
        if not validate_image_file(filepath):
            return False, f"Unsupported image format: {filename}"
        
        try:
            img = Image.open(filepath)
            img.verify()
            app_logger.debug(f" Asset validated: {filename}")
            return True, None
            
        except Exception as e:
            return False, f"Corrupted or invalid image: {e}"