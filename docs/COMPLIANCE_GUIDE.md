#  How to Use Brand Compliance Features

## Quick Start Guide

The brand compliance features are now integrated into the main Streamlit app!

---

## Running the App with Compliance

### Step 1: Start the App

```bash
cd /Users/admin/Codes/creative-automation-pipeline
streamlit run app.py
```

Or use the start script:
```bash
./start.sh
```

The app will open at: **http://localhost:8501**

---

## Using Compliance Features

### In the Sidebar

You'll now see a new **"🔍 Compliance"** section with:

1. **Enable Brand Compliance** checkbox
   - Turn this ON to activate compliance checking

2. **Brand Guidelines (JSON)** file uploader
   - Upload your own `brand_guidelines.json`
   - Or it will use the example file automatically

---

## Step-by-Step Usage

### Option 1: With Example Guidelines

1.  Start the app
2.  In sidebar, check **"Enable Brand Compliance"**
3.  It will automatically use `examples/brand_guidelines.json`
4.  Upload your campaign brief
5.  Click **"Generate Campaign Assets"**
6.  View compliance report in results

### Option 2: With Custom Guidelines

1.  Start the app
2.  In sidebar, check **"Enable Brand Compliance"**
3.  Upload your `brand_guidelines.json` file
4.  Upload your campaign brief
5.  Click **"Generate Campaign Assets"**
6.  View compliance report in results

### Option 3: Without Compliance (Standard Mode)

1.  Start the app
2.  Leave **"Enable Brand Compliance"** unchecked
3.  Upload campaign brief
4.  Click **"Generate Campaign Assets"**
5.  No compliance checking (faster)

---

## What You'll See

### In the Sidebar

**Without Compliance:**
```
⚙️ Configuration
  OpenAI API Key: [input field]
   API Key configured

🔍 Compliance
  ☐ Enable Brand Compliance
```

**With Compliance:**
```
⚙️ Configuration
  OpenAI API Key: [input field]
   API Key configured

🔍 Compliance
  ☑ Enable Brand Compliance
  Brand Guidelines (JSON): [upload]
   Guidelines loaded
```

---

### In the Results

**New Metrics Row:**
```
Campaign    Language    Assets    Errors    Compliance
---------   --------    ------    ------    ----------
My Campaign    EN         12        0        92%
```

**Compliance Report Section:**
Click **"🔍 Compliance Report"** to expand:

```
Total Assets: 12
Compliant: 11  
Avg Score: 91%

Most Common Issues:
- required_colors: 1 occurrence(s)
```

---

## Brand Guidelines Format

Create a `brand_guidelines.json` file:

```json
{
  "brand_name": "Your Brand",
  "required_colors": ["#34A853", "#4285F4"],
  "forbidden_colors": ["#FF0000"],
  "max_text_length": 150,
  "forbidden_words": ["cheap", "fake"],
  "min_image_quality": 70,
  "required_aspect_ratios": ["1:1", "9:16", "16:9"],
  "compliance_level": "standard"
}
```

### Guidelines Parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `brand_name` | string | Your brand name |
| `required_colors` | array | Colors that MUST appear |
| `forbidden_colors` | array | Colors that MUST NOT appear |
| `max_text_length` | number | Max text characters |
| `forbidden_words` | array | Words to avoid |
| `min_image_quality` | number | Min quality (0-100) |
| `required_aspect_ratios` | array | Allowed ratios |
| `compliance_level` | string | "strict", "standard", "relaxed" |

---

## Understanding Compliance Scores

### Score Calculation

- Each check = 1 point
- Score = (Passed / Total) × 100%
- **Compliant** if score ≥ 70% AND no critical failures

### Example Scoring

If 5 checks run:
- 5 passed = 100% 
- 4 passed = 80% 
- 3 passed = 60% 

---

## Compliance Checks

The system validates:

###  Color Compliance
- Required brand colors present?
- Forbidden colors absent?

###  Text Compliance  
- Text length within limit?
- No forbidden words?
- Readable contrast?

###  Quality Compliance
- Image quality acceptable?
- Correct aspect ratio?
- Valid file format?

---

## Example Workflow

### Scenario: Generate Campaign with Compliance

```
1. Open app → http://localhost:8501

2. Sidebar:
   - Enter API key
   - ☑ Enable Brand Compliance
   - Upload brand_guidelines.json

3. Main area:
   - Upload campaign brief (sample_brief_en.json)
   - Upload product images (or let AI generate)

4. Click " Generate Campaign Assets"

5. View results:
   - See assets generated
   - Check compliance score
   - Expand compliance report
   - Download assets
```

---

## Troubleshooting

### Compliance Not Showing?

**Check:**
-  "Enable Brand Compliance" is checked
-  Guidelines file is uploaded or example exists
-  Enhanced pipeline imported correctly

### No Compliance Report?

**Possible reasons:**
- Compliance was disabled
- Generation failed before validation
- Check logs in `logs/` directory

### Low Compliance Score?

**Review:**
- Required colors might be missing
- Text might be too long
- Forbidden words might be present
- Check compliance report for specific issues

---

## Files and Locations

### Your Guidelines
- **Create:** `brand_guidelines.json` anywhere
- **Upload:** Via sidebar in app
- **Example:** `examples/brand_guidelines.json`

### Compliance Reports
- **Location:** `data/output/{campaign}/compliance_report.json`
- **Format:** JSON with detailed results
- **View:** In app or open file directly

### Logs
- **Location:** `logs/pipeline_*.log`
- **Contains:** Detailed validation info

---

## Tips & Best Practices

###  Start Simple
- Use example guidelines first
- Test with one product
- Gradually add restrictions

###  Customize Guidelines
- Start with lenient rules
- Tighten based on results
- Document your decisions

### 📊 Monitor Compliance
- Track scores over time
- Identify common issues
- Adjust guidelines accordingly

### ⚡ Performance
- Compliance adds ~2-3 seconds per asset
- Disable for faster testing
- Enable for final production

---

## What's Different?

### Standard Pipeline
```python
# Old way (still works)
pipeline = CampaignPipeline(api_key="sk-...")
output = pipeline.run(brief_path)
```

### Enhanced Pipeline (with Compliance)
```python
# New way (integrated automatically in UI)
pipeline = EnhancedCampaignPipeline(
    api_key="sk-...",
    guidelines_path="brand_guidelines.json"
)
output = pipeline.run(brief_path, enable_compliance=True)
```

**In the UI:** Just check the box! The app handles everything.

---

## Benefits

###  Quality Assurance
- Catch issues before publishing
- Ensure brand consistency
- Automated validation

###  Efficiency
- No manual checking needed
- Instant feedback
- Detailed reports

###  Compliance
- Audit trail
- Documented validation
- Historical tracking

---

## Summary

**To use compliance features:**

1. Check ☑ "Enable Brand Compliance" in sidebar
2. Upload or use example guidelines
3. Generate campaign as usual
4. View compliance score and report

**That's it!** The app handles the rest automatically.

---

**Need Help?**
- Check `TROUBLESHOOTING.md`
- Review `PHASE4_COMPLETE.md`
- Check logs in `logs/` directory

---

**Last Updated:** October 25, 2025