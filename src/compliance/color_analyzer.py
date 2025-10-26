"""
Color Analysis Service
Analyzes images for color compliance and dominant colors.
"""

from typing import List, Tuple
from PIL import Image
import numpy as np
from src.utils.logger import app_logger


class ColorAnalyzer:
    """Analyzes image colors for brand compliance."""
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """
        Convert hex color to RGB tuple.
        
        Args:
            hex_color: Hex color string (e.g., "#FF5733")
            
        Returns:
            RGB tuple (r, g, b)
        """
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
        """
        Convert RGB tuple to hex color.
        
        Args:
            rgb: RGB tuple (r, g, b)
            
        Returns:
            Hex color string
        """
        return '#{:02x}{:02x}{:02x}'.format(*rgb)
    
    @staticmethod
    def color_distance(color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> float:
        """
        Calculate Euclidean distance between two RGB colors.
        
        Args:
            color1: First RGB color
            color2: Second RGB color
            
        Returns:
            Distance value
        """
        return np.sqrt(sum((a - b) ** 2 for a, b in zip(color1, color2)))
    
    @staticmethod
    def get_dominant_colors(image: Image.Image, num_colors: int = 5) -> List[str]:
        """
        Extract dominant colors from image.
        
        Args:
            image: PIL Image
            num_colors: Number of dominant colors to extract
            
        Returns:
            List of hex color strings
        """
        try:
            # Resize for faster processing
            img = image.copy()
            img.thumbnail((200, 200))
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Get pixel data
            pixels = np.array(img).reshape(-1, 3)
            
            # Use k-means clustering to find dominant colors
            from sklearn.cluster import KMeans
            
            kmeans = KMeans(n_clusters=min(num_colors, len(pixels)), random_state=42, n_init=10)
            kmeans.fit(pixels)
            
            # Get cluster centers (dominant colors)
            colors = kmeans.cluster_centers_.astype(int)
            
            # Convert to hex
            hex_colors = [ColorAnalyzer.rgb_to_hex(tuple(color)) for color in colors]
            
            app_logger.debug(f"Extracted {len(hex_colors)} dominant colors")
            return hex_colors
            
        except ImportError:
            # Fallback if sklearn not available
            app_logger.warning("sklearn not available, using simple color extraction")
            return ColorAnalyzer._simple_dominant_colors(image, num_colors)
        
        except Exception as e:
            app_logger.error(f"Failed to extract dominant colors: {e}")
            return []
    
    @staticmethod
    def _simple_dominant_colors(image: Image.Image, num_colors: int = 5) -> List[str]:
        """
        Simple dominant color extraction without sklearn.
        
        Args:
            image: PIL Image
            num_colors: Number of colors to extract
            
        Returns:
            List of hex color strings
        """
        try:
            # Resize image
            img = image.copy()
            img.thumbnail((100, 100))
            
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Get all colors and their counts
            colors = img.getcolors(10000)
            
            if not colors:
                return []
            
            # Sort by frequency
            colors.sort(reverse=True, key=lambda x: x[0])
            
            # Get top colors
            top_colors = [ColorAnalyzer.rgb_to_hex(color[1]) for color in colors[:num_colors]]
            
            return top_colors
            
        except Exception as e:
            app_logger.error(f"Simple color extraction failed: {e}")
            return []
    
    @staticmethod
    def check_color_presence(
        image: Image.Image,
        target_color: str,
        tolerance: int = 30
    ) -> Tuple[bool, float]:
        """
        Check if a color is present in the image.
        
        Args:
            image: PIL Image
            target_color: Hex color to search for
            tolerance: Color matching tolerance (0-255)
            
        Returns:
            Tuple of (is_present, percentage)
        """
        try:
            target_rgb = ColorAnalyzer.hex_to_rgb(target_color)
            
            # Resize for faster processing
            img = image.copy()
            img.thumbnail((200, 200))
            
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Get pixel data
            pixels = np.array(img).reshape(-1, 3)
            
            # Count matching pixels
            matches = 0
            for pixel in pixels:
                if ColorAnalyzer.color_distance(pixel, target_rgb) <= tolerance:
                    matches += 1
            
            percentage = (matches / len(pixels)) * 100
            is_present = percentage > 0.1  # At least 0.1% of image
            
            app_logger.debug(f"Color {target_color}: {percentage:.2f}% of image")
            
            return is_present, percentage
            
        except Exception as e:
            app_logger.error(f"Color presence check failed: {e}")
            return False, 0.0
    
    @staticmethod
    def check_forbidden_colors(
        image: Image.Image,
        forbidden_colors: List[str],
        tolerance: int = 30
    ) -> List[Tuple[str, float]]:
        """
        Check for presence of forbidden colors.
        
        Args:
            image: PIL Image
            forbidden_colors: List of forbidden hex colors
            tolerance: Color matching tolerance
            
        Returns:
            List of (color, percentage) tuples for forbidden colors found
        """
        found = []
        
        for color in forbidden_colors:
            is_present, percentage = ColorAnalyzer.check_color_presence(
                image, color, tolerance
            )
            if is_present:
                found.append((color, percentage))
        
        return found
    
    @staticmethod
    def validate_brand_colors(
        image: Image.Image,
        required_colors: List[str],
        tolerance: int = 30
    ) -> Tuple[bool, List[str]]:
        """
        Validate that required brand colors are present.
        
        Args:
            image: PIL Image
            required_colors: List of required hex colors
            tolerance: Color matching tolerance
            
        Returns:
            Tuple of (all_present, missing_colors)
        """
        missing = []
        
        for color in required_colors:
            is_present, _ = ColorAnalyzer.check_color_presence(
                image, color, tolerance
            )
            if not is_present:
                missing.append(color)
        
        all_present = len(missing) == 0
        
        return all_present, missing