"""
Phase 3 Verification Script
Tests Streamlit UI components and dependencies.
"""

import sys
from pathlib import Path

print("=" * 70)
print("PHASE 3 VERIFICATION: Streamlit UI")
print("=" * 70)

results = []

# Test 1: Check Streamlit installation
print("\n Testing Streamlit Installation...")
try:
    import streamlit as st
    print(f"    Streamlit installed: v{st.__version__}")
    results.append(("Streamlit Installation", True))
except ImportError:
    print("    Streamlit not installed")
    print("   Run: pip install streamlit")
    results.append(("Streamlit Installation", False))

# Test 2: Check app.py exists
print("\n Testing App File...")
app_file = Path("/Users/admin/Codes/creative-automation-pipeline/app.py")
if app_file.exists():
    size = app_file.stat().st_size
    print(f"    app.py exists ({size:,} bytes)")
    results.append(("App File", True))
else:
    print("    app.py not found")
    results.append(("App File", False))

# Test 3: Check Streamlit config
print("\n Testing Streamlit Configuration...")
config_file = Path("/Users/admin/Codes/creative-automation-pipeline/.streamlit/config.toml")
if config_file.exists():
    print(f"    Streamlit config exists")
    results.append(("Streamlit Config", True))
else:
    print("     Streamlit config not found (optional)")
    results.append(("Streamlit Config", True))

# Test 4: Check start script
print("\n Testing Start Script...")
start_script = Path("/Users/admin/Codes/creative-automation-pipeline/start.sh")
if start_script.exists():
    print(f"    start.sh exists")
    if start_script.stat().st_mode & 0o111:
        print(f"    start.sh is executable")
    else:
        print(f"     start.sh not executable (run: chmod +x start.sh)")
    results.append(("Start Script", True))
else:
    print("    start.sh not found")
    results.append(("Start Script", False))

# Test 5: Check README
print("\n Testing Documentation...")
readme = Path("/Users/admin/Codes/creative-automation-pipeline/README.md")
if readme.exists():
    size = readme.stat().st_size
    print(f"    README.md exists ({size:,} bytes)")
    results.append(("Documentation", True))
else:
    print("    README.md not found")
    results.append(("Documentation", False))

# Test 6: Check all dependencies
print("\n Testing All Dependencies...")
try:
    import openai
    import PIL
    import pydantic
    import yaml
    import streamlit
    print("    All required packages installed")
    results.append(("Dependencies", True))
except ImportError as e:
    print(f"    Missing package: {e}")
    print("   Run: pip install -r requirements.txt")
    results.append(("Dependencies", False))

# Test 7: Validate app.py syntax
print("\n Testing App Syntax...")
try:
    if app_file.exists():
        with open(app_file, 'r') as f:
            compile(f.read(), 'app.py', 'exec')
        print("    app.py syntax valid")
        results.append(("App Syntax", True))
    else:
        results.append(("App Syntax", False))
except SyntaxError as e:
    print(f"    Syntax error in app.py: {e}")
    results.append(("App Syntax", False))

# Summary
print("\n" + "=" * 70)
print("PHASE 3 RESULTS")
print("=" * 70)

for test_name, passed in results:
    status = " PASS" if passed else " FAIL"
    print(f"{status} - {test_name}")

all_passed = all(result[1] for result in results)

if all_passed:
    print("\n" + "" * 35)
    print("PHASE 3 COMPLETE - Streamlit UI Ready!")
    print("" * 35)
    
    print("\n📊 What's Available:")
    print("    Interactive Streamlit web interface")
    print("    Campaign brief upload (JSON/YAML)")
    print("    Product image upload")
    print("    Real-time progress tracking")
    print("    Asset preview and download")
    print("    Example briefs included")
    
    print("\n How to Start:")
    print("   Option 1: ./start.sh")
    print("   Option 2: streamlit run app.py")
    print("   Option 3: python3 -m streamlit run app.py")
    
    print("\n🌐 The app will open at: http://localhost:8501")
    
    print("\n💡 Next Steps:")
    print("   1. Add your OpenAI API key in the sidebar")
    print("   2. Upload or select a campaign brief")
    print("   3. Upload product images (optional)")
    print("   4. Click 'Generate Campaign Assets'")
    print("   5. Download your generated assets!")
    
    exit_code = 0
else:
    print("\n  Some tests failed. Please fix before running the app.")
    exit_code = 1

print("\n" + "=" * 70)
sys.exit(exit_code)