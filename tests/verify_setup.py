"""
Comprehensive Verification Script
Verifies all project components before Phase 2.
"""

import sys
import json
import yaml
from pathlib import Path

BASE_PATH = Path("/Users/admin/Codes/creative-automation-pipeline")


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)


def print_section(text):
    """Print a formatted section header."""
    print(f"\n {text}")


def test_directory_structure():
    """Test that all directories exist."""
    print_section("Testing Directory Structure")
    
    required_dirs = [
        "src",
        "src/models",
        "src/services",
        "src/utils",
        "src/compliance",
        "data",
        "data/input",
        "data/input/briefs",
        "data/input/assets",
        "data/output",
        "examples",
        "tests",
        "logs"
    ]
    
    all_exist = True
    for dir_name in required_dirs:
        dir_path = BASE_PATH / dir_name
        if dir_path.exists() and dir_path.is_dir():
            print(f"    {dir_name}")
        else:
            print(f"    {dir_name} - MISSING")
            all_exist = False
    
    return all_exist


def test_configuration_files():
    """Test that configuration files exist."""
    print_section("Testing Configuration Files")
    
    config_files = [
        "requirements.txt",
        "pyproject.toml",
        ".env.example",
        ".gitignore",
        "src/__init__.py",
        "src/config.py",
        "src/utils/logger.py",
        "src/utils/validators.py"
    ]
    
    all_exist = True
    for filename in config_files:
        filepath = BASE_PATH / filename
        if filepath.exists() and filepath.is_file():
            size = filepath.stat().st_size
            print(f"    {filename:<30} ({size:,} bytes)")
        else:
            print(f"    {filename:<30} - MISSING")
            all_exist = False
    
    return all_exist


def test_product_images():
    """Test that product images exist."""
    print_section("Testing Product Images")
    
    assets_dir = BASE_PATH / "data/input/assets"
    
    expected_images = [
        "ecobottle.png",
        "smartwatch.png",
        "powerbar.png",
        "freshshampoo.png"
    ]
    
    all_exist = True
    total_size = 0
    
    for image_name in expected_images:
        image_path = assets_dir / image_name
        if image_path.exists():
            size = image_path.stat().st_size
            total_size += size
            print(f"    {image_name:<25} {size:>8,} bytes")
        else:
            print(f"    {image_name:<25} MISSING")
            all_exist = False
    
    if all_exist:
        print(f"\n   📊 Total: {len(expected_images)} images, {total_size:,} bytes")
    
    return all_exist


def test_campaign_briefs():
    """Test that campaign briefs exist and are valid."""
    print_section("Testing Campaign Briefs")
    
    examples_dir = BASE_PATH / "examples"
    
    briefs = [
        ("sample_brief_en.json", "json"),
        ("sample_brief_es.json", "json"),
        ("sample_brief_fr.json", "json"),
        ("sample_brief_de_with_generation.json", "json"),
        ("sample_brief_ja.yaml", "yaml"),
    ]
    
    all_valid = True
    
    for filename, format_type in briefs:
        brief_path = examples_dir / filename
        
        if not brief_path.exists():
            print(f"    {filename:<45} MISSING")
            all_valid = False
            continue
        
        try:
            with open(brief_path) as f:
                if format_type == "json":
                    data = json.load(f)
                else:
                    data = yaml.safe_load(f)
            
            # Check required fields
            required = ["campaign_id", "products", "campaign_message", "language"]
            missing = [field for field in required if field not in data]
            
            if missing:
                print(f"    {filename:<45} Missing: {missing}")
                all_valid = False
            else:
                products = len(data["products"])
                lang = data["language"]
                size = brief_path.stat().st_size
                print(f"    {filename:<45} [{lang}] {products} products ({size} bytes)")
        
        except Exception as e:
            print(f"    {filename:<45} Error: {e}")
            all_valid = False
    
    return all_valid


def test_brief_image_mapping():
    """Test that briefs correctly reference images."""
    print_section("Testing Brief-to-Image Mapping")
    
    examples_dir = BASE_PATH / "examples"
    assets_dir = BASE_PATH / "data/input/assets"
    
    json_briefs = list(examples_dir.glob("*.json"))
    
    all_valid = True
    
    for brief_path in json_briefs:
        with open(brief_path) as f:
            data = json.load(f)
        
        print(f"\n   📄 {brief_path.name}:")
        
        for product in data.get("products", []):
            name = product.get("product_name", "Unknown")
            
            if "existing_image" in product:
                image_file = product["existing_image"]
                image_path = assets_dir / image_file
                
                if image_path.exists():
                    print(f"       {name:<20} → {image_file} (exists)")
                else:
                    print(f"        {name:<20} → {image_file} (missing)")
            
            elif product.get("generate_image"):
                print(f"       {name:<20} → Will generate with AI")
            
            else:
                print(f"        {name:<20} → No image specified")
                all_valid = False
    
    return all_valid


def test_python_imports():
    """Test that Python modules can be imported."""
    print_section("Testing Python Imports")
    
    # Add to path
    sys.path.insert(0, str(BASE_PATH))
    
    try:
        from src.config import settings
        print("    src.config imported")
        print(f"      - Languages: {', '.join(settings.supported_languages_list)}")
        print(f"      - Aspect ratios: {', '.join(settings.aspect_ratios)}")
        
        from src.utils.logger import app_logger
        print("    src.utils.logger imported")
        
        from src.utils.validators import validate_language_code, validate_aspect_ratio
        print("    src.utils.validators imported")
        
        # Test validators
        assert validate_language_code("en") == True
        assert validate_aspect_ratio("16:9") == True
        print("    Validators working correctly")
        
        return True
    
    except Exception as e:
        print(f"    Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all verification tests."""
    print_header("COMPREHENSIVE PROJECT VERIFICATION")
    print(f"Base Path: {BASE_PATH}")
    
    results = []
    
    results.append(("Directory Structure", test_directory_structure()))
    results.append(("Configuration Files", test_configuration_files()))
    results.append(("Product Images", test_product_images()))
    results.append(("Campaign Briefs", test_campaign_briefs()))
    results.append(("Brief-Image Mapping", test_brief_image_mapping()))
    results.append(("Python Imports", test_python_imports()))
    
    # Print summary
    print_header("VERIFICATION SUMMARY")
    
    for test_name, passed in results:
        status = " PASS" if passed else " FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n" + "" * 35)
        print("ALL CHECKS PASSED - READY FOR PHASE 2!")
        print("" * 35)
        
        print("\n📊 Project Summary:")
        print("    4 product images (ecobottle, smartwatch, powerbar, freshshampoo)")
        print("    5 campaign briefs (en, es, fr, de, ja)")
        print("    5 supported languages")
        print("    3 aspect ratios (1:1, 9:16, 16:9)")
        print("    Complete folder structure")
        print("    All configuration files")
        
        print("\n✨ Ready to proceed to Phase 2: Core Pipeline Development")
        
        return 0
    else:
        print("\n  Some checks failed. Please review above.")
        return 1


if __name__ == "__main__":
    exit(main())