#  Quick Start - Brand Compliance

## Run the App

```bash
streamlit run app.py
```

---

## Enable Compliance (3 Steps)

### 1. In Sidebar
```
☑ Enable Brand Compliance
```

### 2. Upload Guidelines (Optional)
```
Choose file: brand_guidelines.json
```
**Or skip - uses default automatically!**

### 3. Generate Campaign
```
 Generate Campaign Assets
```

---

## Guideline Levels

| Level | File | Pass Rate | Use For |
|-------|------|-----------|---------|
| **Relaxed** | `brand_guidelines.json` | ~100% | Testing, Development |
| **Standard** | `brand_guidelines_standard.json` | ~90% | Production |
| **Strict** | `brand_guidelines_strict.json` | ~75% | Premium |

**Default:** Relaxed (automatic)

---

## View Results

### Metrics Row
```
Campaign | Language | Assets | Errors | Compliance
---------|----------|--------|--------|------------
My Camp  |    EN    |   12   |   0    |    92%
```

### Compliance Report (Click to Expand)
```
🔍 Compliance Report

Total Assets: 12
Compliant: 11
Avg Score: 91%

Most Common Issues:
- text_length: 1 occurrence(s)
```

---

## Customization

### Basic Template
```json
{
  "brand_name": "Your Brand",
  "required_colors": [],
  "forbidden_colors": [],
  "max_text_length": 200,
  "min_image_quality": 60,
  "compliance_level": "relaxed"
}
```

### Add Restrictions
```json
{
  "required_colors": ["#YOUR_COLOR"],
  "forbidden_colors": ["#RED"],
  "forbidden_words": ["cheap", "fake"],
  "max_text_length": 150
}
```

---

## Troubleshooting

### Assets Failing?
1. Use relaxed guidelines
2. Increase `color_tolerance` to 60+
3. Increase `max_text_length` to 200+
4. Remove `required_colors`

### No Compliance Showing?
1. Check ☑ "Enable Brand Compliance"
2. Ensure guidelines file uploaded
3. Check logs in `logs/` directory

---

## Files

```
examples/
├── brand_guidelines.json          ← Relaxed (default)
├── brand_guidelines_standard.json ← Standard
└── brand_guidelines_strict.json   ← Strict
```

---

## Documentation

- `COMPLIANCE_GUIDE.md` - Full user guide
- `GUIDELINES_COMPARISON.md` - Compare levels
- `FINAL_STATUS.md` - Complete status

---

**That's it! Simple. **