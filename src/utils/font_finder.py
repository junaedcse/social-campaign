"""
Font Finder Utility
Finds available fonts across different operating systems.
"""

import os
from pathlib import Path
from typing import Optional
from PIL import ImageFont


def find_system_font(prefer_bold: bool = True, font_size: int = 20) -> Optional[ImageFont.FreeTypeFont]:
    """
    Find and load a suitable system font across different platforms.
    
    Args:
        prefer_bold: Prefer bold fonts if available
        font_size: Font size to load
        
    Returns:
        Loaded font or None if no suitable font found
    """
    # Common font paths for different systems
    font_paths = [
        # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        
        # macOS
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/Library/Fonts/Arial.ttf",
        
        # Windows
        "C:\\Windows\\Fonts\\arialbd.ttf",  # Arial Bold
        "C:\\Windows\\Fonts\\arial.ttf",    # Arial
        "C:\\Windows\\Fonts\\calibrib.ttf", # Calibri Bold
        "C:\\Windows\\Fonts\\calibri.ttf",  # Calibri
    ]
    
    # Try each path
    for font_path in font_paths:
        try:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, font_size)
                print(f" Loaded font: {font_path}")
                return font
        except Exception as e:
            continue
    
    # Try matplotlib font finder as fallback
    try:
        from matplotlib import font_manager
        system_fonts = font_manager.findSystemFonts()
        
        # Prefer bold fonts
        if prefer_bold:
            for font_path in system_fonts:
                if 'bold' in font_path.lower():
                    try:
                        font = ImageFont.truetype(font_path, font_size)
                        print(f" Loaded bold font: {font_path}")
                        return font
                    except:
                        continue
        
        # Try any font
        for font_path in system_fonts:
            if any(name in font_path.lower() for name in ['sans', 'arial', 'helvetica']):
                try:
                    font = ImageFont.truetype(font_path, font_size)
                    print(f" Loaded font: {font_path}")
                    return font
                except:
                    continue
    except ImportError:
        pass
    
    print(" Could not find any suitable font")
    return None


def get_available_fonts() -> list:
    """
    Get list of available font paths on the system.
    
    Returns:
        List of font file paths
    """
    fonts = []
    
    # Check common directories
    font_dirs = [
        "/usr/share/fonts",
        "/System/Library/Fonts",
        "/Library/Fonts",
        "C:\\Windows\\Fonts",
        os.path.expanduser("~/Library/Fonts"),  # macOS user fonts
    ]
    
    for font_dir in font_dirs:
        if os.path.exists(font_dir):
            for root, dirs, files in os.walk(font_dir):
                for file in files:
                    if file.endswith(('.ttf', '.otf', '.ttc')):
                        fonts.append(os.path.join(root, file))
    
    return fonts


if __name__ == "__main__":
    print("=" * 80)
    print("FONT FINDER UTILITY")
    print("=" * 80)
    
    print("\n🔍 Searching for fonts...")
    font = find_system_font(prefer_bold=True, font_size=20)
    
    if font:
        print("\n Successfully found and loaded a font!")
    else:
        print("\n No suitable fonts found")
        print("\n📋 Available fonts:")
        fonts = get_available_fonts()
        for f in fonts[:20]:  # Show first 20
            print(f"   {f}")
        if len(fonts) > 20:
            print(f"   ... and {len(fonts) - 20} more")