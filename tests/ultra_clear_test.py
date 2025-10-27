#!/usr/bin/env python3
"""
Ultra-clear font size comparison - no wrapping, simple test.

Run from tests/ folder:
    python ultra_clear_test.py
Or from root folder:
    python tests/ultra_clear_test.py
"""

import sys
import platform
from pathlib import Path

# Add parent directory (project root) to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PIL import Image, ImageFont, ImageDraw
from src.services.image_processor import ImageProcessor

print("=" * 80)
print("ULTRA-CLEAR FONT SIZE TEST")
print("=" * 80)

# Create THREE separate images side by side
sizes = [30, 60, 120]

# Detect OS and set font path
system = platform.system()
if system == "Darwin":  # macOS
    font_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    if not Path(font_path).exists():
        font_path = "/System/Library/Fonts/Helvetica.ttc"
elif system == "Windows":
    font_path = "C:\\Windows\\Fonts\\arialbd.ttf"
else:  # Linux
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

print(f"\nUsing font: {font_path}")
print(f"OS: {system}")

# Check if font exists
if not Path(font_path).exists():
    print(f"\n⚠️  Font not found at: {font_path}")
    print("Falling back to default font...")
    use_default_font = True
else:
    use_default_font = False

# Create a wide image
comparison = Image.new('RGB', (3072, 1024), (240, 240, 240))

for idx, size in enumerate(sizes):
    # Create individual image
    img = Image.new('RGB', (1024, 1024), (70, 130, 180))
    draw = ImageDraw.Draw(img)
    
    # Load font with fallback
    try:
        if use_default_font:
            # Use PIL default font (bitmap, limited sizes)
            font = ImageFont.load_default()
            print(f"⚠️  {size}px: Using default font (size may not change)")
        else:
            font = ImageFont.truetype(font_path, size)
    except Exception as e:
        print(f"⚠️  Error loading font: {e}")
        font = ImageFont.load_default()
    
    # Simple single word
    text = "TEXT"
    
    # Get text size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center it
    x = (1024 - text_width) // 2
    y = (1024 - text_height) // 2
    
    # Draw text
    draw.text((x, y), text, font=font, fill=(255, 255, 255))
    
    # Add label at top
    try:
        if use_default_font:
            label_font = ImageFont.load_default()
        else:
            label_font = ImageFont.truetype(font_path, 60)
    except:
        label_font = ImageFont.load_default()
    
    label_text = f"{size}px"
    draw.text((50, 50), label_text, font=label_font, fill=(255, 255, 0))
    
    # Paste into comparison
    comparison.paste(img, (idx * 1024, 0))
    
    print(f"   {size}px: text size = {text_width}x{text_height}px")

output_path = project_root / "FONT_SIZE_PROOF.png"
comparison.save(output_path)

print(f"\n Created: {output_path}")
print(f"\n Open this image:")
print(f"   {output_path}")
print(f"\n   You should see:")
print(f"   Left (30px):   SMALL 'TEXT'")
print(f"   Middle (60px): MEDIUM 'TEXT'")
print(f"   Right (120px): LARGE 'TEXT'")
print(f"\n   If all three are SAME size → Font loading broken")
print(f"   If all three are DIFFERENT size → Font system works ")

print("\n" + "=" * 80)