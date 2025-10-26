#  Creative Automation Pipeline

AI-powered creative automation pipeline for generating localized social media campaign assets at scale.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.39.0-FF4B4B.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-DALL--E--3-412991.svg)](https://openai.com)

---

## 🌟 Features

- ** Smart Asset Generation**: Automatically generate or reuse product images
- **📐 Multiple Aspect Ratios**: Create assets for Instagram (1:1), Stories (9:16), and YouTube (16:9)
- **🌍 Multi-Language Support**: 5 languages (English, Spanish, French, German, Japanese)
- **✨ Text Overlays**: Automatic campaign message placement with wrapping
- **📦 Organized Output**: Assets structured by campaign, product, and aspect ratio
- **🖥️ Interactive UI**: User-friendly Streamlit web interface

---

## 📋 Prerequisites

- Python 3.11 or higher
- OpenAI API key (for image generation and translation)
- pip (Python package manager)

---

##  Quick Start

### 1. Install Dependencies

```bash
cd /Users/admin/Codes/creative-automation-pipeline
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-key-here
```

### 3. Run the Application

**Option A: Using the start script**
```bash
./start.sh
```

**Option B: Direct command**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📖 Usage Guide

### Step 1: Upload Campaign Brief

1. Click **"Upload campaign brief"** 
2. Select a JSON or YAML file with your campaign details
3. Or choose an example from the dropdown

### Step 2: Upload Product Images (Optional)

1. Upload product images if you have them
2. If images are missing, AI will generate them automatically

### Step 3: Generate Assets

1. Click **"Generate Campaign Assets"**
2. Wait for processing (progress bar shows status)
3. View generated assets grouped by product

### Step 4: Download Results

- Download individual assets using the buttons below each image
- Or download all assets as a ZIP file

---

## 📄 Campaign Brief Format

### JSON Example

```json
{
  "campaign_id": "CAMP_2025_001",
  "campaign_name": "Spring Wellness Collection",
  "target_market": "United States",
  "language": "en",
  "target_audience": "Health-conscious millennials",
  "products": [
    {
      "product_id": "PROD_001",
      "product_name": "EcoBottle",
      "description": "Sustainable water bottle",
      "existing_image": "ecobottle.png"
    }
  ],
  "campaign_message": "Stay Healthy, Stay Active!",
  "campaign_tagline": "Empower Your Lifestyle",
  "brand_colors": ["#34A853", "#4285F4"],
  "call_to_action": "Shop Now",
  "aspect_ratios": ["1:1", "9:16", "16:9"]
}
```

### YAML Example

```yaml
campaign_id: CAMP_2025_002
campaign_name: Summer Collection
language: es
products:
  - product_name: PowerBar
    description: High-protein energy bar
    existing_image: powerbar.png
campaign_message: "Fuel Your Passion!"
aspect_ratios: ["1:1", "9:16", "16:9"]
```

See `examples/` directory for more samples.

---

## 📁 Project Structure

```
creative-automation-pipeline/
├── app.py                      # Streamlit UI (main entry point)
├── start.sh                    # Quick start script
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
│
├── src/
│   ├── models/
│   │   └── campaign.py        # Data models
│   ├── services/
│   │   ├── pipeline.py        # Main pipeline orchestrator
│   │   ├── brief_parser.py    # JSON/YAML parser
│   │   ├── asset_manager.py   # Asset management
│   │   ├── image_generator.py # DALL-E integration
│   │   ├── image_processor.py # Image processing
│   │   ├── translator.py      # Translation service
│   │   └── output_manager.py  # Output organization
│   ├── utils/
│   │   ├── logger.py          # Logging
│   │   └── validators.py      # Validation
│   └── config.py              # Configuration
│
├── data/
│   ├── input/
│   │   ├── assets/            # Product images
│   │   └── briefs/            # Campaign briefs
│   └── output/                # Generated campaigns
│
├── examples/                  # Sample campaign briefs
└── tests/                     # Test scripts
```

---

##  Supported Features

### Languages
- 🇺🇸 English (en)
- 🇪🇸 Spanish (es)
- 🇫🇷 French (fr)
- 🇩🇪 German (de)
- 🇯🇵 Japanese (ja)

### Aspect Ratios
- **1:1** - Instagram posts, profile pictures
- **9:16** - Instagram Stories, TikTok, Reels
- **16:9** - YouTube thumbnails, website banners

### Image Processing
- Automatic resizing to target aspect ratios
- Text overlay with campaign messages
- Multi-line text wrapping
- Shadow effects for readability
- Brand color support

---

## 🔧 Configuration

Edit `src/config.py` or use environment variables:

```bash
# Required
OPENAI_API_KEY=your_key_here

# Optional
LOG_LEVEL=INFO
MAX_IMAGE_SIZE=1024
SUPPORTED_LANGUAGES=en,es,fr,de,ja
```

---

##  Testing

### Test Phase 1 (Setup)
```bash
python3 verify_setup.py
```

### Test Phase 2 (Core Pipeline)
```bash
python3 test_phase2.py
```

### Test Full Pipeline (with API key)
```bash
python3 -c "from src.services.pipeline import CampaignPipeline; \
pipeline = CampaignPipeline(); \
pipeline.run('examples/sample_brief_en.json')"
```

---

## 📊 Output Structure

Generated campaigns are organized as:

```
data/output/
└── CAMP_2025_001_20251025_143022/
    ├── EcoBottle/
    │   ├── 1x1.png          # Instagram post
    │   ├── 9x16.png         # Stories format
    │   └── 16x9.png         # YouTube format
    ├── SmartWatch/
    │   ├── 1x1.png
    │   ├── 9x16.png
    │   └── 16x9.png
    └── metadata.json        # Campaign metadata
```

---

##  Use Cases

- **Marketing Teams**: Generate campaign assets at scale
- **Social Media Managers**: Create multi-format content quickly
- **Agencies**: Automate creative production for multiple clients
- **E-commerce**: Generate product campaign images automatically
- **Localization**: Adapt campaigns for different markets

---

## 🛠️ Technology Stack

- **[Streamlit](https://streamlit.io)** - Web interface
- **[OpenAI DALL-E 3](https://openai.com/dall-e-3)** - Image generation
- **[OpenAI GPT-4](https://openai.com/gpt-4)** - Translation
- **[Pillow](https://python-pillow.org)** - Image processing
- **[Pydantic](https://docs.pydantic.dev)** - Data validation
- **[Loguru](https://github.com/Delgan/loguru)** - Logging

---

## 📝 Notes

### Without API Key
You can still use the pipeline with existing images:
-  Parse campaign briefs
-  Load and process existing images
-  Resize to multiple aspect ratios
-  Add text overlays
-  AI image generation (requires API key)
-  Translation (requires API key)

### With API Key
All features enabled:
-  Everything from above
-  Generate missing product images
-  Translate campaign messages

---

## 🤝 Contributing

This is a proof-of-concept project. Feel free to extend it with:
- Additional aspect ratios
- More image processing effects
- Brand compliance validation
- Performance analytics
- Batch processing

---

## 📄 License

This project is for demonstration purposes.

---

## 🙏 Acknowledgments

- OpenAI for DALL-E 3 and GPT-4 APIs
- Streamlit for the amazing web framework
- Pillow for image processing capabilities

---

## 📞 Support

For issues or questions:
1. Check the documentation in this README
2. Review example briefs in `examples/`
3. Check logs in `logs/` directory

---

**Built with ❤️ using Python and AI**