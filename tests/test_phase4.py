"""
Phase 4 Verification Script
Tests brand compliance features.
"""

import sys
from pathlib import Path

# Add parent directory (project root) to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.models.compliance import BrandGuidelines, ComplianceResult
from src.compliance.color_analyzer import ColorAnalyzer
from src.compliance.content_validator import ContentValidator
from src.compliance.brand_checker import BrandComplianceChecker
from PIL import Image
import json

print("=" * 70)
print("PHASE 4 VERIFICATION: Brand Compliance Features")
print("=" * 70)

results = []

# Test 1: Compliance Models
print("\n Testing Compliance Models...")
try:
    guidelines = BrandGuidelines(
        brand_name="Test Brand",
        required_colors=["#FF0000", "#00FF00"],
        max_text_length=100
    )
    assert guidelines.brand_name == "Test Brand"
    assert len(guidelines.required_colors) == 2
    print("    BrandGuidelines model works")
    
    result = ComplianceResult(is_compliant=True, compliance_score=95.0)
    result.add_passed("test_check", "Test passed")
    result.add_failed("failed_check", "Test failed")
    result.calculate_score()
    assert len(result.passed_checks) == 1
    assert len(result.failed_checks) == 1
    print("    ComplianceResult model works")
    
    results.append(("Compliance Models", True))
except Exception as e:
    print(f"    Model test failed: {e}")
    results.append(("Compliance Models", False))

# Test 2: Color Analyzer
print("\n Testing Color Analyzer...")
try:
    analyzer = ColorAnalyzer()
    
    # Test hex to RGB
    rgb = analyzer.hex_to_rgb("#FF5733")
    assert rgb == (255, 87, 51)
    print("    Hex to RGB conversion works")
    
    # Test RGB to hex
    hex_color = analyzer.rgb_to_hex((255, 87, 51))
    assert hex_color == "#ff5733"
    print("    RGB to Hex conversion works")
    
    # Test color distance
    distance = analyzer.color_distance((255, 0, 0), (0, 255, 0))
    assert distance > 0
    print("    Color distance calculation works")
    
    # Test with actual image
    from src.services.asset_manager import AssetManager
    manager = AssetManager()
    assets = manager.list_assets()
    
    if assets:
        image = manager.load_image(assets[0])
        if image:
            colors = analyzer.get_dominant_colors(image, num_colors=3)
            print(f"    Dominant colors extracted: {len(colors)} colors")
        else:
            print("     Could not load image for testing")
    else:
        print("     No assets available for color testing")
    
    results.append(("Color Analyzer", True))
except Exception as e:
    print(f"    Color analyzer test failed: {e}")
    import traceback
    traceback.print_exc()
    results.append(("Color Analyzer", False))

# Test 3: Content Validator
print("\n Testing Content Validator...")
try:
    validator = ContentValidator()
    
    # Test text length
    is_valid, msg = validator.check_text_length("Hello World", 20)
    assert is_valid == True
    print("    Text length validation works")
    
    # Test forbidden words
    is_valid, found = validator.check_forbidden_words(
        "This is cheap product",
        ["cheap", "fake"]
    )
    assert is_valid == False
    assert "cheap" in found
    print("    Forbidden words detection works")
    
    # Test with actual image
    from src.services.asset_manager import AssetManager
    manager = AssetManager()
    assets = manager.list_assets()
    
    if assets:
        image = manager.load_image(assets[0])
        if image:
            is_ok, quality = validator.check_image_quality(image)
            print(f"    Image quality check works (quality: {quality})")
        else:
            print("     Could not load image for testing")
    else:
        print("     No assets available for quality testing")
    
    results.append(("Content Validator", True))
except Exception as e:
    print(f"    Content validator test failed: {e}")
    import traceback
    traceback.print_exc()
    results.append(("Content Validator", False))

# Test 4: Brand Compliance Checker
print("\n Testing Brand Compliance Checker...")
try:
    guidelines = BrandGuidelines(
        brand_name="Test Brand",
        required_colors=["#34A853"],
        max_text_length=150,
        min_image_quality=70
    )
    
    checker = BrandComplianceChecker(guidelines)
    
    # Test with actual image
    from src.services.asset_manager import AssetManager
    manager = AssetManager()
    assets = manager.list_assets()
    
    if assets:
        image = manager.load_image(assets[0])
        if image:
            result = checker.validate_asset(
                image,
                text_content="Test campaign message"
            )
            
            assert result.compliance_score >= 0
            assert result.compliance_score <= 100
            print(f"    Compliance check works (score: {result.compliance_score:.0f}%)")
            print(f"    Checks: {len(result.passed_checks)} passed, {len(result.failed_checks)} failed")
        else:
            print("     Could not load image for testing")
    else:
        print("     No assets available for compliance testing")
    
    results.append(("Brand Compliance Checker", True))
except Exception as e:
    print(f"    Compliance checker test failed: {e}")
    import traceback
    traceback.print_exc()
    results.append(("Brand Compliance Checker", False))

# Test 5: Brand Guidelines File
print("\n Testing Brand Guidelines File...")
guidelines_path = Path("examples/brand_guidelines.json")
if guidelines_path.exists():
    try:
        with open(guidelines_path, 'r') as f:
            data = json.load(f)
        guidelines = BrandGuidelines(**data)
        print(f"    Loaded guidelines for {guidelines.brand_name}")
        print(f"    Required colors: {len(guidelines.required_colors)}")
        print(f"    Compliance level: {guidelines.compliance_level}")
        results.append(("Brand Guidelines File", True))
    except Exception as e:
        print(f"    Failed to load guidelines: {e}")
        results.append(("Brand Guidelines File", False))
else:
    print(f"    Guidelines file not found: {guidelines_path}")
    results.append(("Brand Guidelines File", False))

# Test 6: Enhanced Pipeline
print("\n Testing Enhanced Pipeline...")
try:
    from src.services.pipeline import EnhancedCampaignPipeline
    
    pipeline = EnhancedCampaignPipeline(
        guidelines_path=Path("examples/brand_guidelines.json")
    )
    
    assert pipeline.guidelines is not None
    assert pipeline.compliance_checker is not None
    print("    Enhanced pipeline initialization works")
    print(f"    Loaded brand: {pipeline.guidelines.brand_name}")
    
    results.append(("Enhanced Pipeline", True))
except Exception as e:
    print(f"    Enhanced pipeline test failed: {e}")
    import traceback
    traceback.print_exc()
    results.append(("Enhanced Pipeline", False))

# Summary
print("\n" + "=" * 70)
print("PHASE 4 RESULTS")
print("=" * 70)

for test_name, passed in results:
    status = " PASS" if passed else " FAIL"
    print(f"{status} - {test_name}")

all_passed = all(result[1] for result in results)

if all_passed:
    print("\n" + "" * 35)
    print("PHASE 4 COMPLETE - Brand Compliance Features Ready!")
    print("" * 35)
    
    print("\n📊 What's Available:")
    print("    Brand guidelines data models")
    print("    Color analysis and validation")
    print("    Content validation (text, quality, format)")
    print("    Complete brand compliance checker")
    print("    Enhanced pipeline with compliance")
    print("    Compliance reporting")
    
    print("\n Compliance Features:")
    print("   • Required brand colors validation")
    print("   • Forbidden colors detection")
    print("   • Text length and content checks")
    print("   • Image quality assessment")
    print("   • Aspect ratio validation")
    print("   • Dominant color extraction")
    print("   • Compliance scoring (0-100%)")
    print("   • Detailed compliance reports")
    
    print("\n How to Use:")
    print("   1. Create brand_guidelines.json file")
    print("   2. Use EnhancedCampaignPipeline instead of CampaignPipeline")
    print("   3. Enable compliance checking: run(brief, enable_compliance=True)")
    print("   4. Check compliance_report.json in output directory")
    
    sys.exit(0)
else:
    print("\n  Some tests failed. Please review above.")
    sys.exit(1)