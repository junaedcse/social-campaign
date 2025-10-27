"""
Image Processor Service
Handles image resizing, aspect ratio conversion, and multi-language text overlays.
"""

from pathlib import Path
from typing import Tuple, Optional
from PIL import Image, ImageDraw, ImageFont
from functools import lru_cache
from src.config import settings
from src.utils.logger import app_logger


class ImageProcessor:
    """Processes and manipulates images with multi-language font support."""
    
    def __init__(self):
        """Initialize image processor with font directory."""
        self.fonts_dir = Path("data/fonts")
        self._font_cache = {}
        
        # Log font directory status
        if self.fonts_dir.exists():
            app_logger.info(f"Fonts directory found: {self.fonts_dir}")
            self._log_available_fonts()
        else:
            app_logger.warning(f"Fonts directory not found: {self.fonts_dir}")
            app_logger.warning("Multi-language support may be limited")
    
    def _log_available_fonts(self):
        """Log available fonts for debugging."""
        try:
            for subdir in ['latin', 'japanese', 'fallback']:
                font_dir = self.fonts_dir / subdir
                if font_dir.exists():
                    fonts = list(font_dir.glob("*.ttf"))
                    if fonts:
                        app_logger.info(f"  {subdir}/: {', '.join(f.name for f in fonts)}")
                    else:
                        app_logger.warning(f"  {subdir}/: (empty)")
                else:
                    app_logger.warning(f"  {subdir}/: (not found)")
        except Exception as e:
            app_logger.error(f"Error listing fonts: {e}")
    
    def _find_font_file(self, font_dir: str, possible_names: list) -> Optional[Path]:
        """
        Find font file with fuzzy matching for naming variations.
        
        Args:
            font_dir: Subdirectory name (latin, japanese, fallback)
            possible_names: List of possible font filenames
        
        Returns:
            Path to font file if found, None otherwise
        """
        font_path = self.fonts_dir / font_dir
        
        if not font_path.exists():
            app_logger.debug(f"Font directory not found: {font_path}")
            return None
        
        # Try exact matches first
        for name in possible_names:
            candidate = font_path / name
            if candidate.exists():
                app_logger.debug(f"Found exact match: {candidate}")
                return candidate
        
        # Try case-insensitive and partial matches
        try:
            for font_file in font_path.glob("*.ttf"):
                font_name_lower = font_file.name.lower()
                for name in possible_names:
                    name_lower = name.lower()
                    # Check if names match (ignoring case)
                    if name_lower == font_name_lower:
                        app_logger.debug(f"Found case-insensitive match: {font_file}")
                        return font_file
                    # Check if font file contains the expected name
                    if name_lower.replace('-', '').replace('.ttf', '') in font_name_lower.replace('-', ''):
                        app_logger.debug(f"Found partial match: {font_file}")
                        return font_file
        except Exception as e:
            app_logger.error(f"Error searching fonts in {font_path}: {e}")
        
        return None
    
    def get_font_path(self, language: str = 'en') -> Path:
        """
        Get appropriate font path for language.
        
        Args:
            language: ISO 639-1 language code (en, fr, ja, es, de, etc.)
        
        Returns:
            Path to font file
        
        Raises:
            FileNotFoundError: If no suitable font found
        """
        # Normalize language code
        lang = language.lower()[:2] if language else 'en'
        
        app_logger.debug(f"Getting font for language: {lang}")
        
        # Define font search strategy
        font_searches = {
            # Latin languages - search latin folder, then fallback
            'en': [
                ('latin', ['NotoSans-Bold.ttf', 'Natosans.ttf', 'NotoSans.ttf', 'DejaVuSans-Bold.ttf']),
                ('fallback', ['DejaVuSans-Bold.ttf', 'DejaVuSans.ttf']),
            ],
            'fr': [
                ('latin', ['NotoSans-Bold.ttf', 'Natosans.ttf', 'NotoSans.ttf', 'DejaVuSans-Bold.ttf']),
                ('fallback', ['DejaVuSans-Bold.ttf', 'DejaVuSans.ttf']),
            ],
            'es': [
                ('latin', ['NotoSans-Bold.ttf', 'Natosans.ttf', 'NotoSans.ttf', 'DejaVuSans-Bold.ttf']),
                ('fallback', ['DejaVuSans-Bold.ttf', 'DejaVuSans.ttf']),
            ],
            'de': [
                ('latin', ['NotoSans-Bold.ttf', 'Natosans.ttf', 'NotoSans.ttf', 'DejaVuSans-Bold.ttf']),
                ('fallback', ['DejaVuSans-Bold.ttf', 'DejaVuSans.ttf']),
            ],
            'pt': [
                ('latin', ['NotoSans-Bold.ttf', 'Natosans.ttf', 'NotoSans.ttf', 'DejaVuSans-Bold.ttf']),
                ('fallback', ['DejaVuSans-Bold.ttf', 'DejaVuSans.ttf']),
            ],
            'it': [
                ('latin', ['NotoSans-Bold.ttf', 'Natosans.ttf', 'NotoSans.ttf', 'DejaVuSans-Bold.ttf']),
                ('fallback', ['DejaVuSans-Bold.ttf', 'DejaVuSans.ttf']),
            ],
            # Japanese - search japanese folder first
            'ja': [
                ('japanese', ['NotoSansJP-Bold.ttf', 'NotoSansJP.ttf', 'NotoSansCJK-Bold.ttf']),
                ('fallback', ['DejaVuSans-Bold.ttf', 'DejaVuSans.ttf']),
            ],
            # Chinese
            'zh': [
                ('japanese', ['NotoSansJP-Bold.ttf', 'NotoSansJP.ttf', 'NotoSansCJK-Bold.ttf']),
                ('fallback', ['DejaVuSans-Bold.ttf', 'DejaVuSans.ttf']),
            ],
            # Korean
            'ko': [
                ('japanese', ['NotoSansJP-Bold.ttf', 'NotoSansJP.ttf', 'NotoSansCJK-Bold.ttf']),
                ('fallback', ['DejaVuSans-Bold.ttf', 'DejaVuSans.ttf']),
            ],
        }
        
        # Get search strategy for language
        searches = font_searches.get(lang, font_searches['en'])
        
        # Try each search location
        for font_dir, possible_names in searches:
            font_path = self._find_font_file(font_dir, possible_names)
            if font_path:
                app_logger.info(f"✅ Using font for '{lang}': {font_path}")
                return font_path
        
        # Last resort: search all directories for any .ttf file
        app_logger.warning(f"Font for '{lang}' not found in expected locations, searching all directories...")
        
        for subdir in ['japanese', 'latin', 'fallback']:
            font_path = self.fonts_dir / subdir
            if font_path.exists():
                ttf_files = list(font_path.glob("*.ttf"))
                if ttf_files:
                    app_logger.warning(f"Using fallback font: {ttf_files[0]}")
                    return ttf_files[0]
        
        # Try system fonts as absolute last resort
        system_fonts = [
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
            Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf"),  # macOS
            Path("/System/Library/Fonts/Helvetica.ttc"),  # macOS
            Path("C:/Windows/Fonts/arialbd.ttf"),  # Windows
        ]
        
        for system_font in system_fonts:
            if system_font.exists():
                app_logger.warning(f"Using system font: {system_font}")
                return system_font
        
        # Nothing found
        raise FileNotFoundError(
            f"No suitable font found for language '{lang}'.\n"
            f"Please ensure fonts are installed in:\n"
            f"  {self.fonts_dir}/latin/ (for English, French, Spanish, etc.)\n"
            f"  {self.fonts_dir}/japanese/ (for Japanese)\n"
            f"  {self.fonts_dir}/fallback/ (for fallback)\n"
            f"\n"
            f"Expected files:\n"
            f"  latin/NotoSans-Bold.ttf (or Natosans.ttf)\n"
            f"  japanese/NotoSansJP-Bold.ttf (or NotoSansJP.ttf)\n"
            f"  fallback/DejaVuSans-Bold.ttf\n"
            f"\n"
            f"Run: python scripts/maintenance/download_fonts.py"
        )
    
    @lru_cache(maxsize=20)
    def load_font(self, language: str = 'en', size: int = None) -> ImageFont.FreeTypeFont:
        """
        Load font with caching.
        
        Args:
            language: Language code
            size: Font size in pixels (uses settings default if None)
        
        Returns:
            Loaded font object
        """
        if size is None:
            size = settings.text_font_size
        
        cache_key = (language, size)
        
        # Check cache
        if cache_key in self._font_cache:
            app_logger.debug(f"Using cached font for '{language}' at {size}px")
            return self._font_cache[cache_key]
        
        try:
            font_path = self.get_font_path(language)
            font = ImageFont.truetype(str(font_path), size)
            
            # Cache it
            self._font_cache[cache_key] = font
            
            app_logger.info(f"✅ Loaded font: {font_path.name} at {size}px for '{language}'")
            return font
            
        except FileNotFoundError:
            raise
        except Exception as e:
            app_logger.error(f"Failed to load font for '{language}': {e}")
            app_logger.warning("Attempting to load default font...")
            try:
                return ImageFont.load_default()
            except Exception as e2:
                raise RuntimeError(f"Failed to load any font: {e}, {e2}")
    
    def detect_language(self, text: str) -> str:
        """
        Detect language from text based on character ranges.
        
        Args:
            text: Text to analyze
        
        Returns:
            ISO 639-1 language code
        """
        if not text:
            return 'en'
        
        # Japanese (Hiragana, Katakana, Kanji)
        if any('\u3040' <= c <= '\u309F' or '\u30A0' <= c <= '\u30FF' or '\u4E00' <= c <= '\u9FFF' for c in text):
            app_logger.debug("Detected Japanese characters")
            return 'ja'
        
        # Chinese (Han characters)
        if any('\u4E00' <= c <= '\u9FFF' for c in text):
            app_logger.debug("Detected Chinese characters")
            return 'zh'
        
        # Korean (Hangul)
        if any('\uAC00' <= c <= '\uD7AF' for c in text):
            app_logger.debug("Detected Korean characters")
            return 'ko'
        
        # French specific characters
        if any(c in 'àâæçéèêëïîôùûüÿœÀÂÆÇÉÈÊËÏÎÔÙÛÜŸŒ' for c in text):
            app_logger.debug("Detected French characters")
            return 'fr'
        
        # Spanish specific characters
        if any(c in 'áéíñóúüÁÉÍÑÓÚÜ¿¡' for c in text):
            app_logger.debug("Detected Spanish characters")
            return 'es'
        
        # German specific characters
        if any(c in 'äöüßÄÖÜ' for c in text):
            app_logger.debug("Detected German characters")
            return 'de'
        
        # Italian
        if any(c in 'àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚ' for c in text):
            app_logger.debug("Detected Italian characters")
            return 'it'
        
        # Portuguese
        if any(c in 'ãõÃÕ' for c in text):
            app_logger.debug("Detected Portuguese characters")
            return 'pt'
        
        # Default to English
        app_logger.debug("Defaulting to English")
        return 'en'
    
    def resize_to_aspect_ratio(
        self,
        image: Image.Image,
        aspect_ratio: str,
        base_size: int = 1024,
        fill_color: Tuple[int, int, int] = (255, 255, 255)
    ) -> Image.Image:
        """
        Resize image to specific aspect ratio.
        
        Args:
            image: Source PIL Image
            aspect_ratio: Target aspect ratio (e.g., "16:9", "16x9")
            base_size: Base dimension for sizing
            fill_color: Background fill color for letterboxing
            
        Returns:
            Resized PIL Image
        """
        # Normalize aspect ratio notation
        aspect_ratio = aspect_ratio.replace('x', ':')
        
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
        
        app_logger.info(f"✅ Resized to {aspect_ratio}: {target_width}x{target_height}")
        
        return new_image
    
    def add_text_overlay(
        self,
        image: Image.Image,
        text: str,
        position: str = "bottom",
        font_size: Optional[int] = None,
        language: Optional[str] = None,
        text_color: Tuple[int, int, int] = (255, 255, 255),
        background_color: Optional[Tuple[int, int, int, int]] = (0, 0, 0, 180),
        padding: int = 20
    ) -> Image.Image:
        """
        Add text overlay to image with multi-language support.
        
        Args:
            image: Source PIL Image
            text: Text to overlay
            position: Position (top, center, bottom)
            font_size: Font size in pixels (uses config default if None)
            language: Language code (auto-detect if None)
            text_color: RGB color for text
            background_color: RGBA color for text background (None for no background)
            padding: Padding around text
            
        Returns:
            Image with text overlay
        """
        if not text:
            app_logger.warning("Empty text provided, skipping overlay")
            return image
        
        # Use config font size if not specified
        if font_size is None:
            font_size = settings.text_font_size
        
        # Detect language if not specified
        if language is None:
            language = self.detect_language(text)
            app_logger.info(f"Auto-detected language: {language}")
        
        # Create a copy to avoid modifying original
        img_copy = image.copy()
        
        # Convert to RGBA for transparency support
        if img_copy.mode != 'RGBA':
            img_copy = img_copy.convert('RGBA')
        
        # Create overlay layer
        overlay = Image.new('RGBA', img_copy.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Load appropriate font for language
        try:
            font = self.load_font(language, font_size)
            app_logger.info(f"✅ Loaded font for language '{language}' at {font_size}px")
        except Exception as e:
            app_logger.error(f"Failed to load font: {e}")
            raise
        
        # Calculate text size and position
        # Wrap text if too long
        max_width = img_copy.width - (padding * 4)
        lines = self._wrap_text(text, font, draw, max_width)
        
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
        
        app_logger.info(f"✅ Added text overlay ({language}): '{text[:50]}...'")
        
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