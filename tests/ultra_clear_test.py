#!/usr/bin/env python3
"""
Ultra-clear font size comparison - no wrapping, simple test.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from PIL import Image, ImageFont, ImageDraw
from src.services.image_processor import ImageProcessor

print("=" * 80)
print("ULTRA-CLEAR FONT SIZE TEST")
print("=" * 80)

# Create THREE separate images side by side
sizes = [30, 60, 120]
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Create a wide image
comparison = Image.new('RGB', (3072, 1024), (240, 240, 240))

for idx, size in enumerate(sizes):
    # Create individual image
    img = Image.new('RGB', (1024, 1024), (70, 130, 180))
    draw = ImageDraw.Draw(img)
    
    # Load font
    font = ImageFont.truetype(font_path, size)
    
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
    label_font = ImageFont.truetype(font_path, 60)
    label_text = f"{size}px"
    draw.text((50, 50), label_text, font=label_font, fill=(255, 255, 0))
    
    # Paste into comparison
    comparison.paste(img, (idx * 1024, 0))
    
    print(f"   {size}px: text size = {text_width}x{text_height}px")

output_path = "FONT_SIZE_PROOF.png"
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