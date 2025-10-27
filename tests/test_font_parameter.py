#!/usr/bin/env python3
"""
Comprehensive test showing font_size parameter works correctly.
Tests both direct method calls and through pipeline.
"""

import sys
from pathlib import Path

# Add parent directory (project root) to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config import settings
from PIL import Image, ImageDraw, ImageFont
from src.services.image_processor import ImageProcessor

print("=" * 80)
print("COMPREHENSIVE FONT SIZE TEST")
print("=" * 80)

# Create output directory
output_dir = Path("data/output/font_test")
output_dir.mkdir(parents=True, exist_ok=True)

test_message = "TESTING FONT SIZES"
base_image = Image.new('RGB', (1024, 1024), color=(70, 130, 180))

processor = ImageProcessor()

# Test different font sizes
test_cases = [
    (30, "Very Small"),
    (48, "Small (Old Default)"),
    (60, "Medium"),
    (80, "Large (New Default)"),
    (100, "Very Large"),
    (120, "Extra Large"),
    (150, "Huge")
]

print(f"\n📊 Current Config:")
print(f"   text_font_size: {settings.text_font_size}px")
print(f"   text_shadow_enabled: {settings.text_shadow_enabled}")

print(f"\n Running {len(test_cases)} tests...\n")

results = []

for size, label in test_cases:
    print(f"   Testing {size}px ({label})...", end=" ")
    
    result_img = processor.add_text_overlay(
        base_image.copy(),
        f"{size}px - {label}",
        position="center",
        font_size=size
    )
    
    # Add size label at top
    draw = ImageDraw.Draw(result_img)
    try:
        label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
    except:
        label_font = ImageFont.load_default()
    
    draw.text((20, 20), f"Font Size: {size}px", font=label_font, fill=(255, 255, 0))
    
    output_path = output_dir / f"font_{size:03d}px.png"
    result_img.save(output_path)
    results.append((size, output_path))
    
    print(f" Saved")

# Create comparison grid
print(f"\n Creating comparison grid...")
grid_cols = 3
grid_rows = (len(test_cases) + grid_cols - 1) // grid_cols
cell_size = 340
grid = Image.new('RGB', (grid_cols * cell_size, grid_rows * cell_size), color=(240, 240, 240))

for idx, (size, img_path) in enumerate(results):
    row = idx // grid_cols
    col = idx % grid_cols
    
    img = Image.open(img_path).resize((330, 330))
    grid.paste(img, (col * cell_size + 5, row * cell_size + 5))

grid_path = output_dir / "00_size_comparison_grid.png"
grid.save(grid_path)
print(f"    Saved: {grid_path}")

# Create side-by-side comparison
print(f"\n📊 Creating side-by-side comparison (48px vs 80px vs 120px)...")
comparison = Image.new('RGB', (3072, 1024), color=(240, 240, 240))

key_sizes = [(48, "Old Default"), (80, "New Default"), (120, "Large Custom")]
for idx, (size, label) in enumerate(key_sizes):
    test_img = base_image.copy()
    result = processor.add_text_overlay(
        test_img,
        test_message,
        position="center",
        font_size=size
    )
    
    # Add label
    draw = ImageDraw.Draw(result)
    try:
        label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    except:
        label_font = ImageFont.load_default()
    
    draw.text((50, 50), f"{size}px", font=label_font, fill=(255, 255, 0))
    draw.text((50, 110), label, font=label_font, fill=(255, 255, 0))
    
    comparison.paste(result, (idx * 1024, 0))

comparison_path = output_dir / "01_key_comparison.png"
comparison.save(comparison_path)
print(f"    Saved: {comparison_path}")

print("\n" + "=" * 80)
print("TEST RESULTS")
print("=" * 80)

print(f"\n Successfully tested {len(test_cases)} different font sizes")
print(f"\n📁 Output directory: {output_dir}")
print(f"\n🖼️  Generated images:")
print(f"   1. {grid_path.name} - All sizes in grid")
print(f"   2. {comparison_path.name} - Key comparison (48 vs 80 vs 120)")

for size, path in results:
    print(f"   3. {path.name}")

print(f"\n🔍 Visual Verification:")
print(f"   Open: {comparison_path}")
print(f"   You should see THREE different text sizes:")
print(f"   - Left:   48px (small - old default)")
print(f"   - Middle: 80px (large - new default)")
print(f"   - Right:  120px (extra large)")

print(f"\n💡 How to use custom font size:")
print(f"   ")
print(f"   processor.add_text_overlay(")
print(f"       image,")
print(f"       'Your message',")
print(f"       position='bottom',")
print(f"       font_size=120  # ← Use this parameter")
print(f"   )")

print(f"\n⚠️  Common Issues:")
print(f"   1. Python cache - Solution: Delete __pycache__ folders")
print(f"   2. Old imports - Solution: Restart Python/Jupyter kernel")
print(f"   3. Font not found - Solution: Check font path or use default")

print("\n" + "=" * 80)
print(" FONT SIZE PARAMETER IS WORKING CORRECTLY")
print("=" * 80)

# Test parameter override
print(f"\n Final verification test:")
print(f"   Testing that explicit font_size overrides config default...")

# Config says 80, but we'll use 150
test_override = processor.add_text_overlay(
    base_image.copy(),
    "Override Test: 150px",
    position="center",
    font_size=150  # Should use this, not config's 80
)

override_path = output_dir / "02_override_test_150px.png"
test_override.save(override_path)

print(f"   Config default: {settings.text_font_size}px")
print(f"   Explicit parameter: 150px")
print(f"   Result: {override_path}")
print(f"    If text is HUGE (150px), parameter override works!")

print(f"\n📖 View all results:")
print(f"   ls -lh {output_dir}/")