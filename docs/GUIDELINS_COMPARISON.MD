# Brand Guidelines Comparison

## Available Guideline Files

The project includes three levels of brand compliance guidelines to suit different needs:

---

## 1. Relaxed Guidelines (Default)

**File:** `examples/brand_guidelines.json`

**Best for:** 
- Development and testing
- Quick iterations
- Proof of concept
- First-time users

**Settings:**
```json
{
  "brand_name": "EcoTech Solutions",
  "required_colors": [],           ← No required colors
  "forbidden_colors": [],          ← No forbidden colors
  "color_tolerance": 50,           ← Wide tolerance
  "max_text_length": 200,          ← Generous limit
  "forbidden_words": [],           ← No forbidden words
  "min_image_quality": 60,         ← Lower quality threshold
  "compliance_level": "relaxed"
}
```

**Compliance Rate:** ~100% 
- Almost all assets will pass
- Minimal restrictions
- Focus on format validation only

---

## 2. Standard Guidelines

**File:** `examples/brand_guidelines_standard.json`

**Best for:**
- Production environments
- Balanced approach
- Real-world scenarios
- Brand consistency

**Settings:**
```json
{
  "brand_name": "EcoTech Solutions - Standard",
  "required_colors": [],           ← Optional brand colors
  "forbidden_colors": ["#FF0000"], ← Avoid bright red
  "color_tolerance": 60,
  "max_text_length": 200,
  "forbidden_words": ["polluting", "toxic", "harmful"],
  "min_image_quality": 60,
  "compliance_level": "standard"
}
```

**Compliance Rate:** ~85-95% 
- Reasonable restrictions
- Brand-appropriate content
- Quality control

---

## 3. Strict Guidelines

**File:** `examples/brand_guidelines_strict.json`

**Best for:**
- Regulated industries
- High-profile campaigns
- Premium brands
- Legal compliance

**Settings:**
```json
{
  "brand_name": "EcoTech Solutions - Strict",
  "required_colors": [],
  "forbidden_colors": ["#FF0000"],
  "color_tolerance": 40,           ← Tighter tolerance
  "max_text_length": 180,          ← Shorter text
  "forbidden_words": ["cheap", "inferior"],
  "min_image_quality": 65,         ← Higher quality
  "compliance_level": "standard"
}
```

**Compliance Rate:** ~70-85% 
- Stricter validation
- Higher quality bar
- More rejections possible

---

## Comparison Table

| Feature | Relaxed | Standard | Strict |
|---------|---------|----------|--------|
| **Required Colors** | None | None | None |
| **Forbidden Colors** | None | Red only | Red only |
| **Color Tolerance** | 50 | 60 | 40 |
| **Max Text** | 200 chars | 200 chars | 180 chars |
| **Forbidden Words** | None | 3 words | 2 words |
| **Min Quality** | 60% | 60% | 65% |
| **Pass Rate** | ~100% | ~90% | ~75% |

---

## How to Choose

### Use Relaxed When:
-  You're just getting started
-  Testing the pipeline
-  Need quick results
-  Don't have strict brand rules

### Use Standard When:
-  Running production campaigns
-  Need brand consistency
-  Want quality control
-  Balance speed and quality

### Use Strict When:
-  High-stakes campaigns
-  Regulated content
-  Premium brands
-  Legal requirements

---

## Customization Guide

### Creating Your Own Guidelines

**Step 1: Start with a template**
```bash
cp examples/brand_guidelines.json my_brand_guidelines.json
```

**Step 2: Customize settings**

#### Color Requirements
```json
"required_colors": ["#34A853", "#4285F4"],  // Must have these
"forbidden_colors": ["#FF0000", "#000000"],  // Must NOT have these
"color_tolerance": 30                         // How close (0-255)
```

**Tips:**
- Leave empty `[]` for no color requirements
- Use tolerance 40-60 for realistic matching
- Only forbid truly problematic colors (e.g., competitor colors)

#### Text Requirements
```json
"max_text_length": 150,                      // Max characters
"min_text_size": 24,                         // Min pixels
"forbidden_words": ["cheap", "fake"]         // Avoid these words
```

**Tips:**
- Social media: 100-150 chars
- Print ads: 150-200 chars
- Billboards: 50-100 chars

#### Quality Requirements
```json
"min_image_quality": 70,                     // 0-100 scale
"required_aspect_ratios": ["1:1", "16:9"]   // Allowed formats
```

**Tips:**
- Web: 60-70% quality OK
- Print: 70-85% quality
- High-end: 85%+ quality

---

## Testing Your Guidelines

### Quick Test
```bash
# Use in app
1. Check "Enable Brand Compliance"
2. Upload your guidelines JSON
3. Generate campaign
4. Check compliance score
```

### Command Line Test
```python
from src.models.compliance import BrandGuidelines
from src.compliance.brand_checker import BrandComplianceChecker

# Load your guidelines
with open('my_guidelines.json') as f:
    data = json.load(f)
guidelines = BrandGuidelines(**data)

# Create checker
checker = BrandComplianceChecker(guidelines)

# Test an asset
result = checker.validate_asset(image, text)
print(f"Score: {result.compliance_score}%")
```

---

## Common Scenarios

### Scenario 1: Too Many Failures
**Problem:** 90% of assets failing compliance

**Solutions:**
1. Remove color requirements temporarily
2. Increase color_tolerance to 60+
3. Increase max_text_length
4. Remove forbidden_words
5. Lower min_image_quality

### Scenario 2: Too Lenient
**Problem:** Everything passes, even bad content

**Solutions:**
1. Add specific forbidden colors (competitor colors)
2. Add forbidden words relevant to your brand
3. Increase min_image_quality to 70+
4. Reduce max_text_length for cleaner designs
5. Add required_aspect_ratios

### Scenario 3: Color Matching Issues
**Problem:** Required colors not detected

**Solutions:**
1. Increase color_tolerance (try 50-70)
2. Check hex colors are correct format (#RRGGBB)
3. Use dominant colors from actual assets
4. Consider removing required_colors

---

## Best Practices

###  DO:
- Start relaxed, tighten gradually
- Test with real assets before production
- Document why each rule exists
- Review compliance reports regularly
- Adjust based on actual results

###  DON'T:
- Copy someone else's rules blindly
- Make rules too strict initially
- Forbid common colors (black, white) unless necessary
- Set unrealistic text lengths
- Ignore compliance feedback

---

## Example Workflows

### Workflow 1: Development → Production

```
1. Development Phase
   → Use: brand_guidelines.json (relaxed)
   → Goal: Test functionality
   → Expected: 100% pass rate

2. Staging Phase
   → Use: brand_guidelines_standard.json
   → Goal: Validate approach
   → Expected: 85-95% pass rate

3. Production Phase
   → Use: Custom strict guidelines
   → Goal: Brand compliance
   → Expected: 70-90% pass rate
```

### Workflow 2: Multi-Brand

```
1. Create guidelines per brand
   brand_a_guidelines.json
   brand_b_guidelines.json
   brand_c_guidelines.json

2. Use appropriate file per campaign
3. Track compliance by brand
4. Refine rules based on results
```

---

## Guidelines Schema

```json
{
  "brand_name": "string",
  "logo_required": boolean,
  "logo_min_size_percent": number (0-100),
  "logo_position": "string" | null,
  
  "required_colors": ["#HEXHEX", ...],
  "forbidden_colors": ["#HEXHEX", ...],
  "color_tolerance": number (0-255),
  
  "min_text_size": number (pixels),
  "max_text_length": number (characters),
  "forbidden_words": ["word", ...],
  
  "min_image_quality": number (0-100),
  "required_aspect_ratios": ["W:H", ...],
  
  "compliance_level": "strict" | "standard" | "relaxed"
}
```

---

## Validation Rules

### What Gets Checked:

1. **Colors** (if specified)
   - Required colors present?
   - Forbidden colors absent?

2. **Text** (if provided)
   - Length within limit?
   - No forbidden words?
   - Readable contrast?

3. **Quality**
   - Image quality acceptable?
   - Aspect ratio correct?

### Scoring:
- Each check = 1 point
- Score = (Passed / Total) × 100%
- Compliant if score ≥ 70% AND no critical failures

---

## Support

**Questions?**
- Check `COMPLIANCE_GUIDE.md` for usage
- Review `PHASE4_COMPLETE.md` for features
- See logs in `logs/` directory

**Issues?**
- Verify JSON format is valid
- Check hex colors start with #
- Ensure all required fields present
- Review compliance reports for details

---

**Last Updated:** October 26, 2025  
**Default File:** `examples/brand_guidelines.json` (Relaxed)  
**Recommended:** `examples/brand_guidelines_standard.json` (Standard)