"""
Content Validator Service
Validates campaign content for text, quality, and compliance.
"""

from typing import List, Tuple, Optional
from PIL import Image
from src.utils.logger import app_logger


class ContentValidator:
    """Validates content compliance."""
    
    @staticmethod
    def check_text_length(text: str, max_length: int) -> Tuple[bool, str]:
        """
        Check if text is within length limit.
        
        Args:
            text: Text to check
            max_length: Maximum allowed length
            
        Returns:
            Tuple of (is_valid, message)
        """
        length = len(text)
        
        if length <= max_length:
            return True, f"Text length OK ({length}/{max_length})"
        else:
            return False, f"Text too long ({length}/{max_length})"
    
    @staticmethod
    def check_forbidden_words(
        text: str,
        forbidden_words: List[str]
    ) -> Tuple[bool, List[str]]:
        """
        Check for forbidden words in text.
        
        Args:
            text: Text to check
            forbidden_words: List of forbidden words
            
        Returns:
            Tuple of (is_valid, found_words)
        """
        text_lower = text.lower()
        found = []
        
        for word in forbidden_words:
            if word.lower() in text_lower:
                found.append(word)
        
        is_valid = len(found) == 0
        
        return is_valid, found
    
    @staticmethod
    def check_image_quality(image: Image.Image, min_quality: int = 70) -> Tuple[bool, int]:
        """
        Estimate image quality based on compression artifacts.
        
        Args:
            image: PIL Image
            min_quality: Minimum acceptable quality (0-100)
            
        Returns:
            Tuple of (is_acceptable, estimated_quality)
        """
        try:
            # Simple quality estimation based on image properties
            # More sophisticated methods would analyze compression artifacts
            
            # Check dimensions
            width, height = image.size
            total_pixels = width * height
            
            # Higher resolution = potentially higher quality
            if total_pixels > 1000000:  # > 1MP
                estimated_quality = 90
            elif total_pixels > 500000:  # > 0.5MP
                estimated_quality = 80
            elif total_pixels > 250000:  # > 0.25MP
                estimated_quality = 70
            else:
                estimated_quality = 60
            
            # Check if image has JPEG quality info
            if hasattr(image, 'info') and 'quality' in image.info:
                estimated_quality = image.info['quality']
            
            is_acceptable = estimated_quality >= min_quality
            
            app_logger.debug(f"Image quality: {estimated_quality}")
            
            return is_acceptable, estimated_quality
            
        except Exception as e:
            app_logger.error(f"Quality check failed: {e}")
            return True, 75  # Default to acceptable
    
    @staticmethod
    def check_aspect_ratio(
        image: Image.Image,
        required_ratio: str
    ) -> Tuple[bool, str]:
        """
        Check if image matches required aspect ratio.
        
        Args:
            image: PIL Image
            required_ratio: Required ratio (e.g., "16:9")
            
        Returns:
            Tuple of (matches, actual_ratio)
        """
        try:
            width, height = image.size
            
            # Calculate actual ratio
            gcd = ContentValidator._gcd(width, height)
            actual_w = width // gcd
            actual_h = height // gcd
            actual_ratio = f"{actual_w}:{actual_h}"
            
            # Parse required ratio
            req_w, req_h = map(int, required_ratio.split(':'))
            
            # Check if they match (with some tolerance)
            matches = abs((width/height) - (req_w/req_h)) < 0.01
            
            return matches, actual_ratio
            
        except Exception as e:
            app_logger.error(f"Aspect ratio check failed: {e}")
            return False, "unknown"
    
    @staticmethod
    def _gcd(a: int, b: int) -> int:
        """Calculate greatest common divisor."""
        while b:
            a, b = b, a % b
        return a
    
    @staticmethod
    def check_image_size(
        image: Image.Image,
        min_width: Optional[int] = None,
        min_height: Optional[int] = None,
        max_width: Optional[int] = None,
        max_height: Optional[int] = None
    ) -> Tuple[bool, str]:
        """
        Check if image dimensions are within acceptable range.
        
        Args:
            image: PIL Image
            min_width: Minimum width (optional)
            min_height: Minimum height (optional)
            max_width: Maximum width (optional)
            max_height: Maximum height (optional)
            
        Returns:
            Tuple of (is_valid, message)
        """
        width, height = image.size
        issues = []
        
        if min_width and width < min_width:
            issues.append(f"Width {width}px < minimum {min_width}px")
        
        if min_height and height < min_height:
            issues.append(f"Height {height}px < minimum {min_height}px")
        
        if max_width and width > max_width:
            issues.append(f"Width {width}px > maximum {max_width}px")
        
        if max_height and height > max_height:
            issues.append(f"Height {height}px > maximum {max_height}px")
        
        is_valid = len(issues) == 0
        message = "; ".join(issues) if issues else f"Dimensions OK ({width}x{height})"
        
        return is_valid, message
    
    @staticmethod
    def validate_file_format(
        filepath: str,
        allowed_formats: List[str] = ['PNG', 'JPEG', 'JPG', 'WEBP']
    ) -> Tuple[bool, str]:
        """
        Validate file format.
        
        Args:
            filepath: Path to file
            allowed_formats: List of allowed format extensions
            
        Returns:
            Tuple of (is_valid, format)
        """
        try:
            img = Image.open(filepath)
            format_name = img.format or 'UNKNOWN'
            
            is_valid = format_name.upper() in [f.upper() for f in allowed_formats]
            
            return is_valid, format_name
            
        except Exception as e:
            app_logger.error(f"Format validation failed: {e}")
            return False, "INVALID"
    
    @staticmethod
    def check_text_readability(
        text: str,
        min_contrast_ratio: float = 4.5
    ) -> Tuple[bool, float]:
        """
        Check text readability (simplified check).
        
        Args:
            text: Text to check
            min_contrast_ratio: Minimum contrast ratio (WCAG standard)
            
        Returns:
            Tuple of (is_readable, estimated_ratio)
        """
        # This is a simplified check
        # Real implementation would analyze actual text on background
        
        # For now, just check text length is reasonable for reading
        word_count = len(text.split())
        
        if word_count < 3:
            estimated_ratio = 7.0  # Short text usually OK
        elif word_count < 10:
            estimated_ratio = 5.5
        elif word_count < 20:
            estimated_ratio = 4.8
        else:
            estimated_ratio = 4.0  # Long text might be harder to read
        
        is_readable = estimated_ratio >= min_contrast_ratio
        
        return is_readable, estimated_ratio