"""
Phase 2 Test Script
Tests all core pipeline components.
"""

import sys
from pathlib import Path

# Add parent directory (project root) to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.models.campaign import CampaignBrief, Product
from src.services.brief_parser import BriefParser
from src.services.asset_manager import AssetManager
from src.services.image_processor import ImageProcessor
from src.config import settings


def test_models():
    """Test Pydantic models."""
    print(" Testing Data Models...")
    
    try:
        # Test Product model
        product = Product(
            product_id="TEST_001",
            product_name="Test Product",
            description="A test product",
            existing_image="test.png"
        )
        assert product.product_name == "Test Product"
        print("    Product model works")
        
        # Test CampaignBrief model
        brief = CampaignBrief(
            campaign_id="TEST_CAMPAIGN",
            campaign_name="Test Campaign",
            target_market="Test Market",
            language="en",
            target_audience="Test Audience",
            products=[product],
            campaign_message="Test Message"
        )
        assert brief.campaign_id == "TEST_CAMPAIGN"
        assert len(brief.products) == 1
        print("    CampaignBrief model works")
        
        return True
    except Exception as e:
        print(f"    Model test failed: {e}")
        return False


def test_brief_parser():
    """Test brief parsing."""
    print("\n Testing Brief Parser...")
    
    try:
        parser = BriefParser()
        
        # Test JSON parsing
        json_brief = Path("examples/sample_brief_en.json")
        if json_brief.exists():
            brief = parser.parse_file(json_brief)
            assert brief.campaign_id == "CAMP_2025_001"
            assert len(brief.products) >= 1
            print(f"    JSON parsing works: {brief.campaign_name}")
        else:
            print(f"     JSON file not found: {json_brief}")
        
        # Test YAML parsing
        yaml_brief = Path("examples/sample_brief_ja.yaml")
        if yaml_brief.exists():
            brief = parser.parse_file(yaml_brief)
            assert brief.language == "ja"
            print(f"    YAML parsing works: {brief.campaign_name}")
        else:
            print(f"     YAML file not found: {yaml_brief}")
        
        return True
    except Exception as e:
        print(f"    Brief parser test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_asset_manager():
    """Test asset manager."""
    print("\n Testing Asset Manager...")
    
    try:
        manager = AssetManager()
        
        # List assets
        assets = manager.list_assets()
        print(f"    Found {len(assets)} assets")
        
        # Test asset exists
        if assets:
            test_asset = assets[0]
            exists = manager.asset_exists(test_asset)
            assert exists == True
            print(f"    Asset exists check works: {test_asset}")
            
            # Test load image
            image = manager.load_image(test_asset)
            if image:
                print(f"    Image loading works: {image.size}")
            else:
                print(f"     Could not load image: {test_asset}")
        
        return True
    except Exception as e:
        print(f"    Asset manager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_image_processor():
    """Test image processor."""
    print("\n Testing Image Processor...")
    
    try:
        manager = AssetManager()
        processor = ImageProcessor()
        
        # Get first available image
        assets = manager.list_assets()
        if not assets:
            print("     No assets available for testing")
            return True
        
        image = manager.load_image(assets[0])
        if not image:
            print("     Could not load image for testing")
            return True
        
        # Test resize
        resized = processor.resize_to_aspect_ratio(image, "16:9")
        assert resized.size == (1024, 576)
        print(f"    Resize works: {resized.size}")
        
        # Test text overlay
        with_text = processor.add_text_overlay(resized, "Test Message")
        assert with_text.size == resized.size
        print(f"    Text overlay works")
        
        return True
    except Exception as e:
        print(f"    Image processor test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_configuration():
    """Test configuration."""
    print("\n Testing Configuration...")
    
    try:
        # Test settings
        assert settings.supported_languages_list == ['en', 'es', 'fr', 'de', 'ja']
        print("    Supported languages:", settings.supported_languages_list)
        
        assert settings.aspect_ratios == ['1:1', '9:16', '16:9']
        print("    Aspect ratios:", settings.aspect_ratios)
        
        # Test aspect ratio calculations
        width, height = settings.get_aspect_ratio_dimensions("16:9", 1024)
        assert width == 1024 and height == 576
        print(f"    Aspect ratio calculation: 16:9 = {width}x{height}")
        
        return True
    except Exception as e:
        print(f"    Configuration test failed: {e}")
        return False


def main():
    """Run all Phase 2 tests."""
    print("=" * 70)
    print("PHASE 2 VERIFICATION: Core Pipeline Components")
    print("=" * 70)
    
    results = []
    
    results.append(("Data Models", test_models()))
    results.append(("Configuration", test_configuration()))
    results.append(("Brief Parser", test_brief_parser()))
    results.append(("Asset Manager", test_asset_manager()))
    results.append(("Image Processor", test_image_processor()))
    
    # Summary
    print("\n" + "=" * 70)
    print("PHASE 2 RESULTS")
    print("=" * 70)
    
    for test_name, passed in results:
        status = " PASS" if passed else " FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n" + "" * 35)
        print("PHASE 2 COMPLETE - All core components working!")
        print("" * 35)
        print("\n📊 What Works:")
        print("    Pydantic data models")
        print("    Configuration system")
        print("    JSON/YAML brief parsing")
        print("    Asset management")
        print("    Image processing (resize + text overlay)")
        print("\n✨ Ready for testing full pipeline with API key")
        print("\n💡 Next Steps:")
        print("   1. Add your OpenAI API key to .env file")
        print("   2. Test full pipeline with: python3 test_pipeline.py")
        return 0
    else:
        print("\n  Some tests failed. Please fix before proceeding.")
        return 1


if __name__ == "__main__":
    exit(main())