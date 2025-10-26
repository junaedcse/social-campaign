"""
Image Generator Service
Generates images using OpenAI DALL-E 3.
"""

import requests
from pathlib import Path
from typing import Optional
from PIL import Image
from io import BytesIO
from openai import OpenAI
from src.config import settings
from src.utils.logger import app_logger


class ImageGenerator:
    """Generates images using OpenAI DALL-E."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize ImageGenerator.
        
        Args:
            api_key: OpenAI API key (defaults to config)
        """
        self.api_key = api_key or settings.openai_api_key
        
        if not self.api_key:
            app_logger.warning("No OpenAI API key provided")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)
            app_logger.info("ImageGenerator initialized with OpenAI client")
    
    def generate_product_image(
        self,
        product_name: str,
        description: str,
        prompt: Optional[str] = None,
        size: str = "1024x1024",
        quality: str = "standard"
    ) -> Optional[Image.Image]:
        """
        Generate a product image using DALL-E 3.
        
        Args:
            product_name: Name of the product
            description: Product description
            prompt: Custom generation prompt (optional)
            size: Image size (1024x1024, 1792x1024, or 1024x1792)
            quality: Image quality (standard or hd)
            
        Returns:
            PIL Image object if successful, None otherwise
        """
        if not self.client:
            app_logger.error("OpenAI client not initialized. Check API key.")
            return None
        
        # Build prompt
        if prompt:
            full_prompt = prompt
        else:
            full_prompt = (
                f"Professional product photography of {product_name}. "
                f"{description}. "
                f"High quality, clean background, centered composition, "
                f"studio lighting, commercial photography style."
            )
        
        app_logger.info(f" Generating image for '{product_name}'...")
        app_logger.debug(f"Prompt: {full_prompt}")
        
        try:
            response = self.client.images.generate(
                model=settings.dalle_model,
                prompt=full_prompt,
                size=size,
                quality=quality,
                n=1
            )
            
            # Get image URL from response
            image_url = response.data[0].url
            app_logger.info(f" Image generated successfully")
            
            # Download image
            image = self._download_image(image_url)
            
            if image:
                app_logger.info(
                    f" Downloaded generated image: {image.size[0]}x{image.size[1]}"
                )
            
            return image
            
        except Exception as e:
            app_logger.error(f"Failed to generate image for '{product_name}': {e}")
            return None
    
    def _download_image(self, url: str) -> Optional[Image.Image]:
        """
        Download image from URL.
        
        Args:
            url: Image URL
            
        Returns:
            PIL Image object if successful, None otherwise
        """
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            image = Image.open(BytesIO(response.content))
            return image
            
        except Exception as e:
            app_logger.error(f"Failed to download image from URL: {e}")
            return None
    
    def generate_and_save(
        self,
        product_name: str,
        description: str,
        output_path: Path,
        prompt: Optional[str] = None,
        size: str = "1024x1024",
        quality: str = "standard"
    ) -> bool:
        """
        Generate image and save directly to file.
        
        Args:
            product_name: Name of the product
            description: Product description
            output_path: Path to save the image
            prompt: Custom generation prompt (optional)
            size: Image size
            quality: Image quality
            
        Returns:
            True if successful, False otherwise
        """
        image = self.generate_product_image(
            product_name=product_name,
            description=description,
            prompt=prompt,
            size=size,
            quality=quality
        )
        
        if not image:
            return False
        
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            image.save(output_path, optimize=True)
            
            file_size = output_path.stat().st_size
            app_logger.info(f" Saved generated image to: {output_path} ({file_size:,} bytes)")
            return True
            
        except Exception as e:
            app_logger.error(f"Failed to save generated image: {e}")
            return False
    
    def is_available(self) -> bool:
        """
        Check if image generation is available.
        
        Returns:
            True if API key is configured, False otherwise
        """
        return self.client is not None