# Creative Automation Pipeline

> AI-powered creative automation system for generating localized social media campaign assets at scale with brand compliance validation.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.39.0-FF4B4B.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-DALL--E--3-412991.svg)](https://openai.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [Campaign Brief Format](#campaign-brief-format)
- [Project Structure](#project-structure)
- [Utility Tools](#utility-tools)
- [Configuration](#configuration)
- [Testing](#testing)
- [Output Structure](#output-structure)
- [Technology Stack](#technology-stack)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## Overview

The Creative Automation Pipeline is an enterprise-grade solution for automating the creation of multi-format, multi-language social media campaign assets. It combines AI-powered image generation, intelligent text processing, and brand compliance validation to streamline creative production workflows.

**Perfect for:**
- Marketing teams managing multi-channel campaigns
- Social media managers needing rapid content creation
- Agencies handling multiple client accounts
- E-commerce platforms requiring product campaign automation
- Global brands requiring localized content at scale

---

## Key Features

### **Intelligent Asset Generation**
- **Smart Image Handling**: Automatically generate product images or reuse existing assets
- **AI-Powered Generation**: DALL-E 3 integration for high-quality image creation
- **Batch Processing**: Process multiple products and campaigns simultaneously

### **Multi-Format Output**
- **Instagram Posts** (1:1) - Square format for feed posts
- **Instagram Stories** (9:16) - Vertical format for Stories, Reels, TikTok
- **YouTube Thumbnails** (16:9) - Widescreen format for video platforms

### **Multilingual Support**
- English (en), Spanish (es), French (fr), German (de), Japanese (ja)
- AI-powered translation with GPT-4
- Context-aware localization

### **Brand Compliance**
- Color palette validation
- Font consistency checking
- Text placement verification
- Automated compliance reporting

### **Professional Text Rendering**
- Multi-line text wrapping with intelligent line breaks
- Shadow effects for enhanced readability
- Brand color integration
- Custom font support

### **Organized Workflow**
- Campaign-based folder structure
- Metadata tracking and export
- Comprehensive logging system
- Progress monitoring and error handling

---

## Prerequisites

### System Requirements
- **Python**: Version 3.11 or higher
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 20.04+)
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: 500MB for installation + space for generated assets

### API Requirements
- **OpenAI API Key**: Required for image generation and translation
  - Sign up at [OpenAI Platform](https://platform.openai.com)
  - Create an API key in your account dashboard
  - Ensure sufficient credits for DALL-E 3 and GPT-4 usage

### Python Package Manager
- **pip**: Built-in with Python
- **conda**: Optional but recommended for environment management

---

## Installation

### Method 1: Using pip (Recommended)

#### Step 1: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### Step 2: Install Dependencies
```bash
# Standard installation
pip install -r requirements.txt
```

#### Step 3: Handle Problematic Libraries (If Needed)

If you encounter issues with `opencv-python` or `pyarrow`, use this alternative approach:

```bash
# Remove opencv-python and pyarrow from requirements.txt
# Then install them separately:

# Install OpenCV
pip install opencv-python-headless

# Install PyArrow
pip install pyarrow

# Install remaining dependencies
pip install -r requirements.txt
```

**Note**: `opencv-python-headless` is recommended for server environments as it excludes GUI dependencies.

---

### Method 2: Using Conda

#### Step 1: Create Conda Environment
```bash
# Create environment with Python 3.12
conda create -n creative-pipeline python=3.12

# Activate environment
conda activate creative-pipeline
```

#### Step 2: Install Core Dependencies via Conda
```bash
# Install commonly problematic packages via conda first
conda install -c conda-forge opencv pillow numpy pandas

# Install PyArrow via conda (more reliable than pip)
conda install -c conda-forge pyarrow
```

#### Step 3: Install Remaining Dependencies via pip
```bash
# Install other requirements
pip install streamlit openai loguru pydantic python-dotenv pyyaml
```

---

### Verification

After installation, verify your setup:

```bash
# Check Python version
python --version  # Should be 3.11+

# Verify key packages
python -c "import streamlit, openai, PIL, cv2; print('✓ All packages installed')"

# Run setup verification script
python tests/verify_setup.py
```

---

## Quick Start

### 1. Environment Configuration

Create your environment file:

```bash
# Copy example environment file
cp .env.example .env
```

Edit `.env` with your configuration:

```bash
# Required
OPENAI_API_KEY=sk-your-actual-api-key-here

# Optional
LOG_LEVEL=INFO
MAX_IMAGE_SIZE=1024
OUTPUT_DIR=data/output
SUPPORTED_LANGUAGES=en,es,fr,de,ja
```

### 2. Launch Application

**Option A: Quick Start Script**
```bash
chmod +x start.sh
./start.sh
```

**Option B: Direct Launch**
```bash
streamlit run app.py
```

**Option C: With Custom Port**
```bash
streamlit run app.py --server.port 8080
```

The application will open automatically in your browser at `http://localhost:8501`

---

## Usage Guide

### Complete Workflow

#### Step 1: Prepare Campaign Brief

Create a JSON or YAML file with your campaign details (see [Campaign Brief Format](#campaign-brief-format))

#### Step 2: Upload Assets

1. Click **"Upload Campaign Brief"** in the sidebar
2. Select your JSON/YAML file or choose an example
3. Optionally upload product images to `data/input/assets/`
4. Missing images will be AI-generated automatically

#### Step 3: Configure Generation

1. Review campaign details in the main panel
2. Verify product list and specifications
3. Check target languages and aspect ratios
4. Review brand guidelines if applicable

#### Step 4: Generate Campaign

1. Click **"Generate Campaign Assets"**
2. Monitor progress via the progress bar
3. Review generated assets by product
4. Check compliance report if brand guidelines are active

#### Step 5: Download Results

- **Individual Downloads**: Click download buttons below each image
- **Bulk Download**: Use "Download All Assets as ZIP" button
- **Metadata**: Export campaign metadata for record-keeping

---

## Campaign Brief Format

### JSON Format (Recommended)

```json
{
  "campaign_id": "CAMP_2025_001",
  "campaign_name": "Spring Wellness Collection",
  "target_market": "United States",
  "language": "en",
  "target_audience": "Health-conscious millennials aged 25-40",
  "products": [
    {
      "product_id": "PROD_001",
      "product_name": "EcoBottle",
      "description": "Eco-friendly stainless steel water bottle with double-wall insulation",
      "existing_image": "ecobottle.png",
      "generate_image": false
    },
    {
      "product_id": "PROD_002",
      "product_name": "YogaMat",
      "description": "Premium non-slip yoga mat with alignment markers",
      "generate_image": true
    }
  ],
  "campaign_message": "Stay Healthy, Stay Active!",
  "campaign_tagline": "Empower Your Lifestyle",
  "brand_colors": ["#34A853", "#4285F4"],
  "call_to_action": "Shop Now",
  "aspect_ratios": ["1:1", "9:16", "16:9"],
  "brand_guidelines": {
    "primary_colors": ["#34A853"],
    "secondary_colors": ["#4285F4"],
    "fonts": ["Roboto", "Open Sans"],
    "compliance_level": "strict"
  }
}
```

### YAML Format

```yaml
campaign_id: CAMP_2025_002
campaign_name: Summer Tech Collection
target_market: Global
language: en
target_audience: Tech-savvy professionals

products:
  - product_id: PROD_003
    product_name: SmartWatch
    description: Advanced fitness tracker with heart rate monitoring
    existing_image: smartwatch.png
    generate_image: false
  
  - product_id: PROD_004
    product_name: WirelessEarbuds
    description: Noise-cancelling wireless earbuds with 30hr battery
    generate_image: true

campaign_message: "Experience the Future"
campaign_tagline: "Innovation Meets Style"
brand_colors:
  - "#FF6B6B"
  - "#4ECDC4"
call_to_action: "Discover More"
aspect_ratios:
  - "1:1"
  - "9:16"
  - "16:9"
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `campaign_id` | string | Yes | Unique campaign identifier |
| `campaign_name` | string | Yes | Descriptive campaign name |
| `target_market` | string | No | Geographic target market |
| `language` | string | Yes | Primary language code (en/es/fr/de/ja) |
| `target_audience` | string | No | Audience demographics |
| `products` | array | Yes | List of products (min 1) |
| `campaign_message` | string | Yes | Primary campaign message |
| `campaign_tagline` | string | No | Secondary tagline |
| `brand_colors` | array | No | Hex color codes for brand colors |
| `call_to_action` | string | No | CTA button text |
| `aspect_ratios` | array | Yes | Output formats (1:1, 9:16, 16:9) |
| `brand_guidelines` | object | No | Brand compliance rules |

**Product Object Schema:**
```json
{
  "product_id": "string (required)",
  "product_name": "string (required)",
  "description": "string (required for generation)",
  "existing_image": "string (filename in data/input/assets/)",
  "generate_image": "boolean (default: false)"
}
```

See `examples/` directory for complete sample briefs.

---

## Project Structure

```
================================================================================
PROJECT STRUCTURE: social-campaign
================================================================================

📁 social-campaign/
├── 📁 .streamlit/
│   └── 📄 config.toml
├── 📁 data/
│   ├── 📁 fonts/
│   │   ├── 📁 fallback/
│   │   │   └── 📄 NotoSans.ttf
│   │   ├── 📁 japanese/
│   │   │   └── 📄 NotoSansJP.ttf
│   │   ├── 📁 latin/
│   │   │   └── 📄 DejaVuSans-Bold.ttf
│   │   └── 📝 README.md
│   ├── 📁 input/
│   │   ├── 📁 assets/
│   │   │   ├── 📄 .gitkeep
│   │   │   ├── 🖼️ ecobottle.png
│   │   │   ├── 🖼️ freshshampoo.png
│   │   │   ├── 🖼️ powerbar.png
│   │   │   ├── 🖼️ smartwatch.png
│   │   │   ├── 🖼️ wirelessearbuds_gen.png
│   │   │   └── 🖼️ wirelessearbuds_generated.png
│   │   ├── 📁 briefs/
│   │   │   ├── 📄 .gitkeep
│   │   │   ├── ⚙️ sample_brief_de_with_generation.json
│   │   │   ├── ⚙️ sample_brief_en.json
│   │   │   ├── ⚙️ sample_brief_es.json
│   │   │   ├── ⚙️ sample_brief_fr.json
│   │   │   ├── ⚙️ sample_brief_ja.yaml
│   │   │   └── ⚙️ temp_guidelines.json
│   ├── 📁 output/
│   │   ├── 📁 CAMP_2025_002_20251027_134916/
│   │   │   ├── 📁 EcoBottle/
│   │   │   │   ├── 🖼️ 16x9.png
│   │   │   │   ├── 🖼️ 1x1.png
│   │   │   │   └── 🖼️ 9x16.png
│   │   │   ├── 📁 PowerBar/
│   │   │   │   ├── 🖼️ 16x9.png
│   │   │   │   ├── 🖼️ 1x1.png
│   │   │   │   └── 🖼️ 9x16.png
│   │   │   └── ⚙️ metadata.json
│   │   ├── 📁 CAMP_2025_002_20251027_163930/
│   │   │   ├── 📁 EcoBottle/
│   │   │   │   ├── 🖼️ 16x9.png
│   │   │   │   ├── 🖼️ 1x1.png
│   │   │   │   └── 🖼️ 9x16.png
│   │   │   ├── 📁 PowerBar/
│   │   │   │   ├── 🖼️ 16x9.png
│   │   │   │   ├── 🖼️ 1x1.png
│   │   │   │   └── 🖼️ 9x16.png
│   │   │   └── ⚙️ metadata.json
│   │   ├── 📁 CAMP_2025_003_20251027_133332/
│   │   │   ├── 📁 FreshShampoo/
│   │   │   │   ├── 🖼️ 16x9.png
│   │   │   │   ├── 🖼️ 1x1.png
│   │   │   │   └── 🖼️ 9x16.png
│   │   │   └── ⚙️ metadata.json
│   │   ├── 📁 CAMP_2025_003_20251027_133602/
│   │   │   ├── 📁 FreshShampoo/
│   │   │   │   ├── 🖼️ 16x9.png
│   │   │   │   ├── 🖼️ 1x1.png
│   │   │   │   └── 🖼️ 9x16.png
│   │   │   └── ⚙️ metadata.json
│   │   ├── 📁 CAMP_2025_003_20251027_135830/
│   │   │   ├── 📁 FreshShampoo/
│   │   │   │   ├── 🖼️ 16x9.png
│   │   │   │   ├── 🖼️ 1x1.png
│   │   │   │   └── 🖼️ 9x16.png
│   │   │   └── ⚙️ metadata.json
│   │   ├── 📁 CAMP_2025_003_20251027_165415/
│   │   │   ├── 📁 FreshShampoo/
│   │   │   │   ├── 🖼️ 16x9.png
│   │   │   │   ├── 🖼️ 1x1.png
│   │   │   │   └── 🖼️ 9x16.png
│   │   │   └── ⚙️ metadata.json
│   │   ├── 📁 CAMP_2025_005_20251027_135733/
│   │   │   ├── 📁 EcoBottle/
│   │   │   │   ├── 🖼️ 16x9.png
│   │   │   │   ├── 🖼️ 1x1.png
│   │   │   │   └── 🖼️ 9x16.png
│   │   │   ├── 📁 FreshShampoo/
│   │   │   │   ├── 🖼️ 16x9.png
│   │   │   │   ├── 🖼️ 1x1.png
│   │   │   │   └── 🖼️ 9x16.png
│   │   │   └── ⚙️ metadata.json
│   │   ├── 📁 CAMP_2025_005_20251027_161536/
│   │   │   ├── 📁 EcoBottle/
│   │   │   │   ├── 🖼️ 16x9.png
│   │   │   │   ├── 🖼️ 1x1.png
│   │   │   │   └── 🖼️ 9x16.png
│   │   │   ├── 📁 FreshShampoo/
│   │   │   │   ├── 🖼️ 16x9.png
│   │   │   │   ├── 🖼️ 1x1.png
│   │   │   │   └── 🖼️ 9x16.png
│   │   │   └── ⚙️ metadata.json
│   │   ├── 📁 font_test/
│   │   │   ├── 🖼️ 00_size_comparison_grid.png
│   │   │   ├── 🖼️ 01_key_comparison.png
│   │   │   ├── 🖼️ 02_override_test_150px.png
│   │   │   ├── 🖼️ font_030px.png
│   │   │   ├── 🖼️ font_048px.png
│   │   │   ├── 🖼️ font_060px.png
│   │   │   ├── 🖼️ font_080px.png
│   │   │   ├── 🖼️ font_100px.png
│   │   │   ├── 🖼️ font_120px.png
│   │   │   └── 🖼️ font_150px.png
│   │   └── 📄 .gitkeep
├── 📁 docs/
│   ├── 📝 COMPLIANCE_GUIDE.md
│   ├── 📝 FINAL_STATUS.md
│   ├── 📝 FONT_FIX_COMPLETE.md
│   ├── 📄 GUIDELINES_COMPARISON.MD
│   ├── 📝 GUIDELINES_UPDATE.md
│   ├── 📝 INTEGRATION_COMPLETE.md
│   ├── 📝 QUICKSTART.md
│   └── 📝 UPDATE_SUMMARY.md
├── 📁 examples/
│   ├── ⚙️ brand_guidelines.json
│   ├── ⚙️ brand_guidelines_standard.json
│   ├── ⚙️ brand_guidelines_strict.json
│   ├── ⚙️ sample_brief_de_with_generation.json
│   ├── ⚙️ sample_brief_en.json
│   ├── ⚙️ sample_brief_es.json
│   ├── ⚙️ sample_brief_fr.json
│   └── ⚙️ sample_brief_ja.yaml
├── 📁 logs/
│   ├── 📋 pipeline_2025-10-25.log
│   ├── 📋 pipeline_2025-10-26.log
│   └── 📋 pipeline_2025-10-27.log
├── 📁 src/
│   ├── 📁 compliance/
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 brand_checker.py
│   │   ├── 🐍 color_analyzer.py
│   │   └── 🐍 content_validator.py
│   ├── 📁 models/
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 campaign.py
│   │   └── 🐍 compliance.py
│   ├── 📁 services/
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 asset_manager.py
│   │   ├── 🐍 brief_parser.py
│   │   ├── 🐍 image_generator.py
│   │   ├── 🐍 image_processor.py
│   │   ├── 🐍 output_manager.py
│   │   ├── 🐍 pipeline.py
│   │   ├── 🐍 pipeline_enhanced.py
│   │   └── 🐍 translator.py
│   ├── 📁 ui/
│   │   ├── 🐍 campaign_results.py
│   │   └── 🐍 compliance_page.py
│   ├── 📁 utils/
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 font_finder.py
│   │   ├── 🐍 logger.py
│   │   └── 🐍 validators.py
│   ├── 🐍 __init__.py
│   └── 🐍 config.py
├── 📁 tests/
│   ├── 🐍 test_font_parameter.py
│   ├── 🐍 test_phase2.py
│   ├── 🐍 test_phase3.py
│   ├── 🐍 test_phase4.py
│   ├── 🐍 ultra_clear_test.py
│   └── 🐍 verify_setup.py
├── 📁 tools/
│   ├── 🐍 generate_images.py
│   └── 🐍 project_structure.py
├── 📄 .env
├── 📄 .env.example
├── 📄 .gitignore
├── 🐍 app.py
├── 📄 pyproject.toml
├── 📝 README.md
├── 📄 requirements.txt
└── 🔧 start.sh
```

---

## Utility Tools

### 1. Generate Images (`tools/generate_images.py`)

Standalone CLI tool for batch image generation without the full pipeline.

**Usage:**
```bash
# Generate single product image
python tools/generate_images.py \
  --product "Eco Water Bottle" \
  --description "Sustainable stainless steel water bottle" \
  --output data/input/assets/ecobottle.png

# Generate multiple images from CSV
python tools/generate_images.py \
  --csv products.csv \
  --output-dir data/input/assets/

# Generate with specific style
python tools/generate_images.py \
  --product "Smart Watch" \
  --description "Modern fitness tracker" \
  --style "professional product photography" \
  --size 1024x1024
```

**Features:**
- Batch processing from CSV files
- Custom image sizes and styles
- Progress tracking
- Error handling and retry logic
- Automatic naming conventions

**CSV Format for Batch Generation:**
```csv
product_name,description,output_filename
EcoBottle,Sustainable water bottle,ecobottle.png
SmartWatch,Advanced fitness tracker,smartwatch.png
YogaMat,Premium non-slip mat,yogamat.png
```

### 2. Project Structure Generator (`tools/project_structure.py`)

Automatically generates visual project structure documentation.

**Usage:**
```bash
# Generate structure with default settings
python tools/project_structure.py

# Generate with custom depth
python tools/project_structure.py --max-depth 4

# Include hidden files
python tools/project_structure.py --show-hidden

# Export to file
python tools/project_structure.py --output PROJECT_STRUCTURE.md
```

**Features:**
- Visual tree representation
- File size and line count statistics
- Automatic emoji icons by file type
- Markdown export capability
- Configurable depth and filters

---

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key for DALL-E and GPT-4 | - | Yes |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARNING/ERROR) | INFO | No |
| `MAX_IMAGE_SIZE` | Maximum image dimension in pixels | 1024 | No |
| `OUTPUT_DIR` | Output directory path | data/output | No |
| `SUPPORTED_LANGUAGES` | Comma-separated language codes | en,es,fr,de,ja | No |
| `ENABLE_COMPLIANCE` | Enable brand compliance checking | false | No |
| `FONT_PATH` | Custom font file path | - | No |

### Configuration File (`src/config.py`)

```python
from pathlib import Path
import os

class Config:
    # API Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Directory Paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    INPUT_DIR = DATA_DIR / "input"
    OUTPUT_DIR = DATA_DIR / "output"
    ASSETS_DIR = INPUT_DIR / "assets"
    BRIEFS_DIR = INPUT_DIR / "briefs"
    
    # Image Processing
    MAX_IMAGE_SIZE = int(os.getenv("MAX_IMAGE_SIZE", 1024))
    ASPECT_RATIOS = {
        "1:1": (1080, 1080),
        "9:16": (1080, 1920),
        "16:9": (1920, 1080)
    }
    
    # Supported Languages
    LANGUAGES = {
        "en": "English",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "ja": "Japanese"
    }
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR = BASE_DIR / "logs"
```

---

## Testing

### Setup Verification

```bash
# Verify installation and configuration
python tests/verify_setup.py
```

**Checks:**
- Python version compatibility
- Required packages installation
- Directory structure
- Environment variables
- API connectivity (if key provided)

### Unit Tests

```bash
# Test core pipeline functionality
python tests/test_phase2.py

# Test image processing
python tests/test_phase3.py

# Test end-to-end workflow
python tests/test_phase4.py
```

### Integration Tests

```bash
# Test with sample brief (no API required)
python -m pytest tests/ -v

# Test with API calls (requires API key)
python -m pytest tests/ -v --with-api
```

### Manual Testing

```bash
# Run pipeline with example brief
python -c "
from src.services.pipeline import CampaignPipeline
pipeline = CampaignPipeline()
pipeline.run('examples/sample_brief_en.json')
"
```

---

## Output Structure

### Campaign Output Format

```
data/output/
└── CAMP_2025_001_20251027_143022/          # Campaign folder (ID + timestamp)
    ├── EcoBottle/                           # Product subfolder
    │   ├── 1x1.png                          # Instagram post (1080x1080)
    │   ├── 9x16.png                         # Stories format (1080x1920)
    │   └── 16x9.png                         # YouTube format (1920x1080)
    │
    ├── SmartWatch/
    │   ├── 1x1.png
    │   ├── 9x16.png
    │   └── 16x9.png
    │
    ├── metadata.json                        # Campaign metadata
    └── compliance_report.json               # Brand compliance results (if enabled)
```

### Metadata File Structure

```json
{
  "campaign_id": "CAMP_2025_001",
  "campaign_name": "Spring Wellness Collection",
  "generated_at": "2025-10-27T14:30:22",
  "language": "en",
  "total_products": 2,
  "total_assets": 6,
  "products": [
    {
      "product_name": "EcoBottle",
      "product_id": "PROD_001",
      "assets_generated": 3,
      "image_source": "existing",
      "formats": ["1:1", "9:16", "16:9"]
    }
  ],
  "processing_time_seconds": 45.3,
  "api_calls": {
    "image_generation": 1,
    "translation": 0
  }
}
```

---

## Technology Stack

### Core Framework
- **[Streamlit 1.39.0](https://streamlit.io)** - Interactive web interface
- **[Python 3.11+](https://python.org)** - Primary programming language

### AI & Machine Learning
- **[OpenAI DALL-E 3](https://openai.com/dall-e-3)** - AI image generation
- **[OpenAI GPT-4](https://openai.com/gpt-4)** - Natural language translation

### Image Processing
- **[Pillow (PIL) 10.0+](https://python-pillow.org)** - Image manipulation
- **[OpenCV 4.8+](https://opencv.org)** - Advanced image processing

### Data Handling
- **[Pydantic 2.0+](https://docs.pydantic.dev)** - Data validation and parsing
- **[PyYAML](https://pyyaml.org)** - YAML file processing
- **[PyArrow](https://arrow.apache.org/docs/python/)** - Efficient data structures

### Utilities
- **[Loguru](https://github.com/Delgan/loguru)** - Advanced logging
- **[python-dotenv](https://github.com/theskumar/python-dotenv)** - Environment management
- **[Requests](https://requests.readthedocs.io)** - HTTP client

---

## Troubleshooting

### Common Installation Issues

#### Issue: OpenCV Installation Fails
```bash
# Solution 1: Use headless version
pip uninstall opencv-python
pip install opencv-python-headless

# Solution 2: Install via conda
conda install -c conda-forge opencv
```

#### Issue: PyArrow Compatibility Error
```bash
# Solution: Install specific version
pip install pyarrow==14.0.1

# Or use conda
conda install -c conda-forge pyarrow
```

#### Issue: Pillow Import Error
```bash
# Reinstall with proper dependencies
pip uninstall Pillow
pip install Pillow --no-cache-dir
```

### Runtime Issues

#### Issue: "API Key Not Found"
```bash
# Verify .env file exists and contains key
cat .env | grep OPENAI_API_KEY

# Check environment variable is loaded
python -c "import os; print(os.getenv('OPENAI_API_KEY'))"
```

#### Issue: Image Generation Fails
- Verify API key has sufficient credits
- Check internet connectivity
- Review logs in `logs/pipeline_YYYY-MM-DD.log`
- Ensure product descriptions are detailed enough

#### Issue: Font Not Found
```bash
# List available fonts
python -c "from src.utils.font_finder import FontFinder; FontFinder.list_fonts()"

# Specify custom font in .env
echo "FONT_PATH=/path/to/your/font.ttf" >> .env
```

#### Issue: Output Directory Permission Denied
```bash
# Fix permissions
chmod -R 755 data/output

# Or change output directory
export OUTPUT_DIR=/path/with/write/permission
```

### Performance Optimization

```bash
# Reduce image size for faster processing
export MAX_IMAGE_SIZE=512

# Disable compliance checking for speed
export ENABLE_COMPLIANCE=false

# Use existing images instead of generation
# Set "generate_image": false in campaign brief
```

---

## Use Cases

### Marketing Agencies
- Generate campaign variations for A/B testing
- Create multi-market campaigns with localized content
- Rapid prototyping of creative concepts
- Consistent brand application across products

### E-commerce Platforms
- Automated product launch campaigns
- Seasonal collection promotions
- Flash sale creative generation
- Product category campaigns

### Social Media Management
- Multi-platform content creation (Instagram, TikTok, YouTube)
- Story and post format optimization
- Batch content scheduling preparation
- Brand-consistent visual identity

### Enterprise Marketing
- Global campaign rollout automation
- Regional market adaptation
- Brand guideline enforcement
- Compliance documentation

---

## Roadmap

### Upcoming Features
- [ ] Video asset generation support
- [ ] Additional social platforms (Twitter, LinkedIn, Pinterest)
- [ ] Advanced text animations
- [ ] Template library management
- [ ] Collaborative workflow features
- [ ] Analytics and performance tracking
- [ ] API access for programmatic usage
- [ ] Mobile app companion

### Planned Improvements
- [ ] Enhanced AI image quality controls
- [ ] Custom brand font upload
- [ ] Advanced color palette generation
- [ ] Batch campaign processing
- [ ] Cloud storage integration
- [ ] Real-time collaboration
- [ ] Accessibility compliance (WCAG)

---

## Contributing

We welcome contributions! Please follow these guidelines:

### Development Setup
```bash
# Fork and clone repository
git clone https://github.com/yourusername/creative-automation-pipeline
cd creative-automation-pipeline

# Create feature branch
git checkout -b feature/amazing-feature

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v
```

### Code Standards
- Follow PEP 8 style guide
- Add docstrings to all functions
- Include type hints
- Write unit tests for new features
- Update documentation

### Pull Request Process
1. Update README.md with new features
2. Add tests for new functionality
3. Ensure all tests pass
4. Update version in `pyproject.toml`
5. Submit PR with clear description

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **OpenAI** for providing DALL-E 3 and GPT-4 APIs
- **Streamlit** for the excellent web framework
- **Python Pillow** team for powerful image processing
- **Open source community** for amazing tools and libraries

---

## Support & Contact

### Documentation
- [Quick Start Guide](docs/QUICKSTART.md)
- [Compliance Guide](docs/COMPLIANCE_GUIDE.md)
- [API Documentation](docs/API.md)

### Community
- Report bugs: [GitHub Issues](https://github.com/yourusername/repo/issues)
- Feature requests: [GitHub Discussions](https://github.com/yourusername/repo/discussions)

### Resources
- Ch