#!/bin/bash
# Quick start script for Creative Automation Pipeline

echo " Starting Creative Automation Pipeline..."
echo ""

# Check if in correct directory
if [ ! -f "app.py" ]; then
    echo " Error: app.py not found"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "  Streamlit not found. Installing..."
    pip install streamlit
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "import openai, PIL, pydantic, yaml" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "  Some dependencies missing. Installing..."
    pip install -r requirements.txt
fi

echo ""
echo " All dependencies ready"
echo ""
echo "🌐 Starting Streamlit app..."
echo "   Open your browser to: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start Streamlit
streamlit run app.py