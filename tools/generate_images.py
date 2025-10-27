"""
Generate sample product images for testing.
Creates placeholder images that look like product photos.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


def create_product_image(product_name: str, color: tuple, size: tuple = (1024, 1024)) -> Image.Image:
    """
    Create a sample product image with gradient background.
    
    Args:
        product_name: Name of the product
        color: RGB color tuple for the product
        size: Image dimensions
        
    Returns:
        PIL Image object
    """
    # Create image with gradient
    img = Image.new('RGB', size)
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    r, g, b = color
    for y in range(size[1]):
        # Gradient from color to lighter version
        factor = y / size[1]
        new_r = int(r + (255 - r) * factor * 0.3)
        new_g = int(g + (255 - g) * factor * 0.3)
        new_b = int(b + (255 - b) * factor * 0.3)
        draw.line([(0, y), (size[0], y)], fill=(new_r, new_g, new_b))
    
    # Add a "product" shape (circle in center)
    margin = size[0] // 4
    circle_bbox = [margin, margin, size[0] - margin, size[1] - margin]
    
    # Draw product circle with lighter shade
    product_color = (
        min(255, r + 50),
        min(255, g + 50),
        min(255, b + 50)
    )
    draw.ellipse(circle_bbox, fill=product_color, outline=(255, 255, 255), width=8)
    
    # Add product name
    try:
        # Try to use a nice font, fall back to default if not available
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
    except:
        font = ImageFont.load_default()
    
    # Get text bounding box for centering
    text_bbox = draw.textbbox((0, 0), product_name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = (size[0] - text_width) // 2
    text_y = (size[1] - text_height) // 2
    
    # Draw text with shadow
    draw.text((text_x + 3, text_y + 3), product_name, fill=(0, 0, 0, 128), font=font)
    draw.text((text_x, text_y), product_name, fill=(255, 255, 255), font=font)
    
    return img


def main():
    """Generate sample product images."""
    base_path = Path("/Users/admin/Codes/creative-automation-pipeline")
    assets_dir = base_path / "data/input/assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    # Define products with colors
    products = [
        ("EcoBottle", (52, 168, 83)),      # Green
        ("SmartWatch", (66, 133, 244)),    # Blue
        ("PowerBar", (234, 67, 53)),       # Red
        ("FreshShampoo", (251, 188, 5)),   # Yellow
    ]
    
    print(" Generating sample product images...")
    print(f"📁 Target directory: {assets_dir}")
    
    for product_name, color in products:
        # Create main product image
        img = create_product_image(product_name, color, (1024, 1024))
        
        # Save image
        filename = f"{product_name.lower()}.png"
        filepath = assets_dir / filename
        img.save(filepath, "PNG")
        
        file_size = filepath.stat().st_size
        print(f" Created: {filename} ({file_size:,} bytes) - RGB{color}")
    
    print(f"\n📊 Total images created: {len(products)}")
    print(f" All images saved successfully!")
    
    # Verify files exist
    print("\n🔍 Verification:")
    for filename in assets_dir.glob("*.png"):
        size = filename.stat().st_size
        print(f"   ✓ {filename.name} - {size:,} bytes")


if __name__ == "__main__":
    main()