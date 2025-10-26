"""
Image Processor Service
Handles image resizing, aspect ratio conversion, and basic manipulations.
"""

from pathlib import Path
from typing import Tuple, Optional
from PIL import Image, ImageDraw, ImageFont
from src.config import settings
from src.utils.logger import app_logger


class ImageProcessor:
    """Processes and manipulates images."""
    
    @staticmethod
    def resize_to_aspect_ratio(
        image: Image.Image,
        aspect_ratio: str,
        base_size: int = 1024,
        fill_color: Tuple[int, int, int] = (255, 255, 255)
    ) -> Image.Image:
        """
        Resize image to specific aspect ratio.
        
        Args:
            image: Source PIL Image
            aspect_ratio: Target aspect ratio (e.g., "16:9")
            base_size: Base dimension for sizing
            fill_color: Background fill color for letterboxing
            
        Returns:
            Resized PIL Image
        """
        # Calculate target dimensions
        target_width, target_height = settings.get_aspect_ratio_dimensions(
            aspect_ratio, base_size
        )
        
        app_logger.debug(
            f"Resizing image from {image.size} to aspect ratio {aspect_ratio} "
            f"({target_width}x{target_height})"
        )
        
        # Create new image with target size
        new_image = Image.new('RGB', (target_width, target_height), fill_color)
        
        # Calculate scaling to fit image in target size (cover mode)
        img_aspect = image.width / image.height
        target_aspect = target_width / target_height
        
        if img_aspect > target_aspect:
            # Image is wider, scale by height
            scale = target_height / image.height
        else:
            # Image is taller, scale by width
            scale = target_width / image.width
        
        new_width = int(image.width * scale)
        new_height = int(image.height * scale)
        
        # Resize image
        resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Center the image
        x = (target_width - new_width) // 2
        y = (target_height - new_height) // 2
        
        new_image.paste(resized, (x, y))
        
        app_logger.info(f" Resized to {aspect_ratio}: {target_width}x{target_height}")
        
        return new_image
    
    @staticmethod
    def add_text_overlay(
        image: Image.Image,
        text: str,
        position: str = "bottom",
        font_size: Optional[int] = None,
        text_color: Tuple[int, int, int] = (255, 255, 255),
        background_color: Optional[Tuple[int, int, int, int]] = (0, 0, 0, 180),
        padding: int = 20
    ) -> Image.Image:
        """
        Add text overlay to image.
        
        Args:
            image: Source PIL Image
            text: Text to overlay
            position: Position (top, center, bottom)
            font_size: Font size in pixels (uses config default if None)
            text_color: RGB color for text
            background_color: RGBA color for text background (None for no background)
            padding: Padding around text
            
        Returns:
            Image with text overlay
        """
        # Use config font size if not specified
        if font_size is None:
            font_size = settings.text_font_size
        
        # Create a copy to avoid modifying original
        img_copy = image.copy()
        
        # Convert to RGBA for transparency support
        if img_copy.mode != 'RGBA':
            img_copy = img_copy.convert('RGBA')
        
        # Create overlay layer
        overlay = Image.new('RGBA', img_copy.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Load font
        try:
            # Try primary font path
            font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                font_size
            )
            app_logger.debug(f"Loaded DejaVu font at {font_size}px")
        except OSError:
            # Try alternative font paths for macOS/other systems
            alternative_paths = [
                "/System/Library/Fonts/Helvetica.ttc",
                "/Library/Fonts/Arial Bold.ttf",
                "Arial.ttf",
                "Helvetica.ttf",
            ]
            
            font_loaded = False
            for alt_path in alternative_paths:
                try:
                    font = ImageFont.truetype(alt_path, font_size)
                    app_logger.info(f"Loaded alternative font: {alt_path} at {font_size}px")
                    font_loaded = True
                    break
                except OSError:
                    continue
            
            if not font_loaded:
                # Last resort: try to load any system font
                try:
                    from matplotlib import font_manager
                    system_fonts = font_manager.findSystemFonts()
                    for font_path in system_fonts:
                        if 'bold' in font_path.lower() or 'sans' in font_path.lower():
                            try:
                                font = ImageFont.truetype(font_path, font_size)
                                app_logger.info(f"Loaded system font: {font_path} at {font_size}px")
                                font_loaded = True
                                break
                            except:
                                continue
                except ImportError:
                    pass
            
            if not font_loaded:
                app_logger.warning(f"Could not load custom font at {font_size}px, using default (text will be small)")
                font = ImageFont.load_default()
        
        # Calculate text size and position
        # Wrap text if too long
        max_width = img_copy.width - (padding * 4)
        lines = ImageProcessor._wrap_text(text, font, draw, max_width)
        
        # Calculate total text height
        line_heights = [draw.textbbox((0, 0), line, font=font)[3] for line in lines]
        total_height = sum(line_heights) + (len(lines) - 1) * 10  # 10px spacing
        
        # Determine vertical position
        if position == "top":
            y = padding * 2
        elif position == "center":
            y = (img_copy.height - total_height) // 2
        else:  # bottom
            y = img_copy.height - total_height - padding * 2
        
        # Draw background rectangle if specified
        if background_color:
            bg_height = total_height + padding * 2
            draw.rectangle(
                [(0, y - padding), (img_copy.width, y + bg_height - padding)],
                fill=background_color
            )
        
        # Draw each line of text
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (img_copy.width - text_width) // 2
            
            # Draw text with optional shadow
            if settings.text_shadow_enabled:
                shadow_offset = settings.text_shadow_offset
                draw.text(
                    (x + shadow_offset, y + shadow_offset),
                    line,
                    font=font,
                    fill=(0, 0, 0, 200)
                )
            
            # Draw main text
            draw.text((x, y), line, font=font, fill=text_color + (255,))
            
            y += text_height + 10  # Move to next line
        
        # Composite overlay onto image
        result = Image.alpha_composite(img_copy, overlay)
        
        # Convert back to RGB
        result = result.convert('RGB')
        
        app_logger.info(f" Added text overlay: '{text[:50]}...'")
        
        return result
    
    @staticmethod
    def _wrap_text(text: str, font, draw, max_width: int) -> list[str]:
        """
        Wrap text to fit within max width.
        
        Args:
            text: Text to wrap
            font: Font object
            draw: ImageDraw object
            max_width: Maximum width in pixels
            
        Returns:
            List of text lines
        """
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]
            
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines if lines else [text]
    
    @staticmethod
    def ensure_rgb(image: Image.Image) -> Image.Image:
        """
        Ensure image is in RGB mode.
        
        Args:
            image: Source PIL Image
            
        Returns:
            RGB PIL Image
        """
        if image.mode != 'RGB':
            return image.convert('RGB')
        return image
    
    @staticmethod
    def optimize_for_web(
        image: Image.Image,
        max_size: int = 1920,
        quality: int = 85
    ) -> Image.Image:
        """
        Optimize image for web delivery.
        
        Args:
            image: Source PIL Image
            max_size: Maximum dimension
            quality: JPEG quality (1-100)
            
        Returns:
            Optimized PIL Image
        """
        # Resize if too large
        if max(image.size) > max_size:
            ratio = max_size / max(image.size)
            new_size = (int(image.width * ratio), int(image.height * ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            app_logger.debug(f"Resized for web: {new_size}")
        
        return image