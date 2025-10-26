"""
Creative Automation Pipeline - Streamlit UI
Interactive web interface for campaign asset generation.
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.services.pipeline import CampaignPipeline
from src.services.pipeline_enhanced import EnhancedCampaignPipeline
from src.services.brief_parser import BriefParser
from src.services.asset_manager import AssetManager
from src.config import settings
from src.utils.logger import app_logger
from src.models.compliance import BrandGuidelines
from src.compliance.brand_checker import BrandComplianceChecker
import json
import yaml
from datetime import datetime
from PIL import Image
import io


# Page configuration
st.set_page_config(
    page_title="Creative Automation Pipeline",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4285F4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4285F4;
        color: white;
        font-weight: bold;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
    </style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if 'pipeline_run' not in st.session_state:
        st.session_state.pipeline_run = False
    if 'output_data' not in st.session_state:
        st.session_state.output_data = None
    if 'brief_uploaded' not in st.session_state:
        st.session_state.brief_uploaded = False


def render_header():
    """Render page header."""
    st.markdown('<div class="main-header">🎨 Creative Automation Pipeline</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Campaign Asset Generation</div>', unsafe_allow_html=True)


def render_sidebar():
    """Render sidebar with configuration."""
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Use API key from config/environment
        api_key = settings.openai_api_key
        
        # Compliance Settings
        st.subheader("🔍 Compliance")
        enable_compliance = st.checkbox(
            "Enable Brand Compliance",
            value=False,
            help="Validate assets against brand guidelines"
        )
        
        guidelines_file = None
        if enable_compliance:
            uploaded_guidelines = st.file_uploader(
                "Brand Guidelines (JSON)",
                type=['json'],
                help="Upload brand guidelines file"
            )
            
            if uploaded_guidelines:
                guidelines_file = uploaded_guidelines
                st.success(" Guidelines loaded")
            else:
                # Check for example guidelines
                example_path = Path("examples/brand_guidelines.json")
                if example_path.exists():
                    st.info("📋 Using example guidelines")
                    guidelines_file = example_path
                else:
                    st.warning("⚠️ No guidelines file")
        
        st.divider()
        
        # System info
        st.subheader("📊 System Info")
        st.write(f"**Supported Languages:** {', '.join(settings.supported_languages_list)}")
        st.write(f"**Aspect Ratios:** {', '.join(settings.aspect_ratios)}")
        
        # Asset stats
        asset_manager = AssetManager()
        assets = asset_manager.list_assets()
        st.write(f"**Available Assets:** {len(assets)}")
        
        st.divider()
        
        # Help
        st.subheader("❓ Help")
        with st.expander("How to use"):
            st.markdown("""
            1. **Upload Campaign Brief** (JSON or YAML)
            2. **Upload Product Images** (optional)
            3. **Enable Compliance** (optional)
            4. **Click Generate** to create assets
            5. **Download** generated campaign assets
            """)
        
        return api_key, enable_compliance, guidelines_file


def render_brief_upload():
    """Render brief upload section."""
    st.header("📄 Campaign Brief")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_brief = st.file_uploader(
            "Upload campaign brief (JSON or YAML)",
            type=['json', 'yaml', 'yml'],
            help="Upload your campaign brief file"
        )
    
    with col2:
        st.write("**Example Briefs:**")
        example_files = list(Path("examples").glob("*.json")) + list(Path("examples").glob("*.yaml"))
        if example_files:
            selected_example = st.selectbox(
                "Or select example",
                [""] + [f.name for f in example_files]
            )
            if selected_example:
                return Path("examples") / selected_example
    
    if uploaded_brief:
        # Save uploaded brief temporarily
        temp_path = Path("data/input/briefs") / uploaded_brief.name
        temp_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path.write_bytes(uploaded_brief.getvalue())
        return temp_path
    
    return None


def render_brief_preview(brief_path):
    """Render brief preview."""
    if not brief_path:
        return None
    
    try:
        parser = BriefParser()
        brief = parser.parse_file(brief_path)
        
        st.success(f" Brief loaded: **{brief.campaign_name}**")
        
        with st.expander("📋 Brief Details", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Campaign ID:** {brief.campaign_id}")
                st.write(f"**Target Market:** {brief.target_market}")
                st.write(f"**Language:** {brief.language.upper()}")
            
            with col2:
                st.write(f"**Products:** {len(brief.products)}")
                st.write(f"**Aspect Ratios:** {len(brief.aspect_ratios)}")
                st.write(f"**Target Audience:** {brief.target_audience}")
            
            with col3:
                st.write(f"**Message:** {brief.campaign_message[:50]}...")
                if brief.campaign_tagline:
                    st.write(f"**Tagline:** {brief.campaign_tagline}")
            
            # Products table
            st.subheader("Products")
            for i, product in enumerate(brief.products, 1):
                st.write(f"{i}. **{product.product_name}** - {product.description[:60]}...")
                if product.existing_image:
                    st.write(f"   📷 Image: {product.existing_image}")
                elif product.generate_image:
                    st.write(f"   🎨 Will generate via AI")
        
        return brief
        
    except Exception as e:
        st.error(f" Failed to parse brief: {e}")
        return None


def render_asset_upload():
    """Render asset upload section."""
    st.header("📷 Product Images")
    
    uploaded_assets = st.file_uploader(
        "Upload product images (optional)",
        type=['png', 'jpg', 'jpeg', 'webp'],
        accept_multiple_files=True,
        help="Upload images for products that don't have them yet"
    )
    
    if uploaded_assets:
        asset_manager = AssetManager()
        
        for uploaded_file in uploaded_assets:
            # Save to assets directory
            image = Image.open(uploaded_file)
            asset_manager.save_image(image, uploaded_file.name)
            st.success(f" Uploaded: {uploaded_file.name}")
    
    # Show existing assets
    asset_manager = AssetManager()
    existing_assets = asset_manager.list_assets()
    
    if existing_assets:
        with st.expander(f"📂 Available Assets ({len(existing_assets)})", expanded=False):
            cols = st.columns(4)
            for i, asset in enumerate(existing_assets):
                with cols[i % 4]:
                    img = asset_manager.load_image(asset)
                    if img:
                        st.image(img, caption=asset, use_column_width=True)


def run_pipeline(brief_path, api_key, enable_compliance=False, guidelines_file=None):
    """Run the campaign pipeline."""
    try:
        # Determine which pipeline to use
        if enable_compliance and guidelines_file:
            # Load guidelines
            guidelines_path = None
            
            if isinstance(guidelines_file, Path):
                guidelines_path = guidelines_file
            else:
                # Save uploaded file temporarily
                temp_guidelines = Path("data/input/briefs/temp_guidelines.json")
                temp_guidelines.parent.mkdir(parents=True, exist_ok=True)
                temp_guidelines.write_bytes(guidelines_file.getvalue())
                guidelines_path = temp_guidelines
            
            # Initialize enhanced pipeline
            pipeline = EnhancedCampaignPipeline(
                api_key=api_key,
                guidelines_path=guidelines_path
            )
            
            st.info("🔍 Running with brand compliance validation...")
        else:
            # Initialize standard pipeline
            pipeline = CampaignPipeline(api_key=api_key)
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text(" Starting pipeline...")
        progress_bar.progress(10)
        
        # Run pipeline
        status_text.text("⚙️ Processing campaign...")
        progress_bar.progress(30)
        
        if enable_compliance and isinstance(pipeline, EnhancedCampaignPipeline):
            output = pipeline.run(brief_path, enable_compliance=True)
        else:
            output = pipeline.run(brief_path)
        
        progress_bar.progress(100)
        status_text.text(" Pipeline complete!")
        
        return output
        
    except Exception as e:
        st.error(f" Pipeline failed: {e}")
        app_logger.error(f"Pipeline error: {e}")
        import traceback
        app_logger.error(traceback.format_exc())
        return None


def render_output(output):
    """Render pipeline output and results."""
    if not output:
        return
    
    st.header("📊 Generation Results")
    
    # Check for compliance report
    output_dir = Path(output.output_directory)
    compliance_report_path = output_dir / "compliance_report.json"
    has_compliance = compliance_report_path.exists()
    
    # Summary metrics
    if has_compliance:
        col1, col2, col3, col4, col5 = st.columns(5)
    else:
        col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Campaign", output.campaign_name)
    
    with col2:
        st.metric("Language", output.language.upper())
    
    with col3:
        st.metric("Assets Generated", output.success_count())
    
    with col4:
        error_count = len(output.errors) if output.errors else 0
        st.metric("Errors", error_count)
    
    # Show compliance metrics if available
    if has_compliance:
        with col5:
            try:
                with open(compliance_report_path, 'r') as f:
                    compliance_data = json.load(f)
                compliance_rate = compliance_data.get('compliance_rate', 0)
                st.metric("Compliance", f"{compliance_rate:.0f}%")
            except:
                pass
    
    # Show compliance report if available
    if has_compliance:
        with st.expander("🔍 Compliance Report", expanded=False):
            try:
                with open(compliance_report_path, 'r') as f:
                    compliance_data = json.load(f)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Assets", compliance_data.get('total_assets', 0))
                with col2:
                    st.metric("Compliant", compliance_data.get('compliant_assets', 0))
                with col3:
                    avg_score = compliance_data.get('average_score', 0)
                    st.metric("Avg Score", f"{avg_score:.0f}%")
                
                if 'common_failures' in compliance_data and compliance_data['common_failures']:
                    st.write("**Most Common Issues:**")
                    for check, count in compliance_data['common_failures']:
                        st.write(f"- {check}: {count} occurrence(s)")
            except Exception as e:
                st.error(f"Could not load compliance report: {e}")
    
    # Show errors if any
    if output.has_errors():
        st.error("⚠️ Some errors occurred during generation:")
        for error in output.errors:
            st.write(f"- {error}")
    
    # Display generated assets
    if output.success_count() > 0:
        st.success(f" Successfully generated {output.success_count()} assets!")
        
        # Group assets by product
        products = {}
        for asset_info in output.generated_assets:
            product_name = asset_info['product_name']
            if product_name not in products:
                products[product_name] = []
            products[product_name].append(asset_info)
        
        # Display each product's assets
        for product_name, assets in products.items():
            st.subheader(f"📦 {product_name}")
            
            cols = st.columns(len(assets))
            for i, asset_info in enumerate(assets):
                with cols[i]:
                    asset_path = output_dir / asset_info['filepath']
                    if asset_path.exists():
                        img = Image.open(asset_path)
                        st.image(img, caption=f"{asset_info['aspect_ratio']}", use_column_width=True)
                        
                        # Download button
                        with open(asset_path, 'rb') as f:
                            st.download_button(
                                label=f"⬇️ Download",
                                data=f,
                                file_name=asset_path.name,
                                mime="image/png",
                                key=f"download_{product_name}_{asset_info['aspect_ratio']}"
                            )
        
        # Download all as ZIP
        st.divider()
        if st.button("📦 Download All Assets as ZIP"):
            zip_path = create_zip_archive(output_dir)
            if zip_path and zip_path.exists():
                with open(zip_path, 'rb') as f:
                    st.download_button(
                        label="⬇️ Download ZIP",
                        data=f,
                        file_name=f"{output.campaign_id}_assets.zip",
                        mime="application/zip"
                    )


def create_zip_archive(output_dir):
    """Create ZIP archive of all generated assets."""
    try:
        import zipfile
        
        zip_path = output_dir / "campaign_assets.zip"
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in output_dir.rglob('*.png'):
                zipf.write(file, file.relative_to(output_dir))
        
        return zip_path
        
    except Exception as e:
        app_logger.error(f"Failed to create ZIP: {e}")
        return None


def main():
    """Main application."""
    init_session_state()
    render_header()
    
    # Sidebar
    api_key, enable_compliance, guidelines_file = render_sidebar()
    
    # Main content
    tab1, tab2, tab3 = st.tabs([" Generate Campaign", "📚 Examples", "ℹ️ About"])
    
    with tab1:
        # Brief upload
        brief_path = render_brief_upload()
        
        # Brief preview
        brief = render_brief_preview(brief_path) if brief_path else None
        
        st.divider()
        
        # Asset upload
        render_asset_upload()
        
        st.divider()
        
        # Generate button
        if brief_path and brief:
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button(" Generate Campaign Assets", type="primary", use_container_width=True):
                    with st.spinner("Generating assets..."):
                        output = run_pipeline(
                            brief_path,
                            api_key,
                            enable_compliance=enable_compliance,
                            guidelines_file=guidelines_file
                        )
                        if output:
                            st.session_state.output_data = output
                            st.session_state.pipeline_run = True
                            st.rerun()
        else:
            st.info("👆 Please upload or select a campaign brief to continue")
        
        # Show results if available
        if st.session_state.pipeline_run and st.session_state.output_data:
            st.divider()
            render_output(st.session_state.output_data)
    
    with tab2:
        st.header("📚 Example Campaign Briefs")
        
        example_dir = Path("examples")
        if example_dir.exists():
            for example_file in sorted(example_dir.glob("*.json")) + sorted(example_dir.glob("*.yaml")):
                with st.expander(f"📄 {example_file.name}"):
                    content = example_file.read_text()
                    
                    if example_file.suffix == '.json':
                        data = json.loads(content)
                        st.json(data)
                    else:
                        st.code(content, language='yaml')
                    
                    st.download_button(
                        label="⬇️ Download Example",
                        data=content,
                        file_name=example_file.name,
                        key=f"download_example_{example_file.name}"
                    )
    
    with tab3:
        st.header("ℹ️ About Creative Automation Pipeline")
        
        st.markdown("""
        ### 🎨 What is this?
        
        An AI-powered creative automation pipeline that generates localized social media 
        campaign assets at scale using OpenAI's DALL-E 3 and GPT-4.
        
        ### ✨ Features
        
        - **Multi-format support**: JSON and YAML campaign briefs
        - **Smart asset management**: Reuse existing images or generate new ones
        - **Multiple aspect ratios**: 1:1, 9:16, 16:9 (Instagram, Stories, YouTube)
        - **Text overlays**: Automatic campaign message placement
        - **Multi-language**: Support for 5 languages (en, es, fr, de, ja)
        - **Organized output**: Assets organized by product and aspect ratio
        
        ###  How It Works
        
        1. Upload a campaign brief with product details
        2. Upload product images (or let AI generate them)
        3. Pipeline processes and generates assets for all aspect ratios
        4. Download individual assets or entire campaign as ZIP
        
        ### 🛠️ Technology Stack
        
        - **Streamlit**: Web interface
        - **OpenAI DALL-E 3**: Image generation
        - **OpenAI GPT-4**: Translation
        - **Pillow**: Image processing
        - **Pydantic**: Data validation
        
        ### 📊 System Configuration
        
        - **Languages**: {lang}
        - **Aspect Ratios**: {ratios}
        - **Max Image Size**: {size}px
        
        ### 📝 Brief Format
        
        Campaign briefs should include:
        - Campaign metadata (ID, name, target market)
        - Product information (name, description, images)
        - Campaign message and tagline
        - Brand colors and call-to-action
        
        See the Examples tab for sample briefs.
        """.format(
            lang=", ".join(settings.supported_languages_list),
            ratios=", ".join(settings.aspect_ratios),
            size=settings.max_image_size
        ))


if __name__ == "__main__":
    main()