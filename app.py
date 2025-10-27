"""
Social Campaign Generator - Streamlit Application

Complete example with image preview integration
"""

import streamlit as st

from pathlib import Path

import json

from src.services.pipeline import CampaignPipeline

from src.ui.campaign_results import add_image_preview_to_existing_flow

from src.utils.logger import app_logger

# Page configuration

st.set_page_config(
    page_title="Social Campaign Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for light blue buttons and form tools
st.markdown(
    """
    <style>
    /* Button and form tool colors to light blue */
    div.stButton > button {
        background-color: #ADD8E6 !important;
        color: #000000 !important;
    }
    .css-1offfwp.edgvbvh3 {
        background-color: #ADD8E6 !important;
        color: #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    """Main application entry point."""

    # Sidebar
    st.sidebar.title("🎨 Social Campaign Generator")
    st.sidebar.markdown("AI-powered multi-language campaign creation")

    # Main content
    st.title("🎨 Social Campaign Generator")
    st.markdown("Create professional multi-language marketing campaigns with AI")

    # ===== STEP 1: Upload Brief =====

    st.markdown("---")

    st.header("1️⃣ Upload Campaign Brief")

    brief_file = st.file_uploader(
        "Upload Campaign Brief (JSON or YAML)",
        type=['json', 'yaml', 'yml'],
        help="Upload your campaign brief file with product information and messaging"
    )

    # Show brief preview if uploaded
    if brief_file:
        with st.expander("📄 Brief Preview"):
            try:
                brief_content = brief_file.read()
                brief_file.seek(0)  # Reset file pointer
                if brief_file.name.endswith('.json'):
                    brief_data = json.loads(brief_content)
                    st.json(brief_data)
                else:
                    st.code(brief_content.decode('utf-8'), language='yaml')
            except Exception as e:
                st.error(f"Error reading brief: {e}")

    # ===== STEP 2: Configure Options =====

    st.markdown("---")

    st.header("2️⃣ Configure Campaign Options")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📝 Content Options")

        language_map = {
            'en': 'English 🇬🇧',
            'fr': 'French 🇫🇷',
            'es': 'Spanish 🇪🇸',
            'de': 'German 🇩🇪',
            'ja': 'Japanese 🇯🇵',
        }

        selected_languages = st.multiselect(
            "Target Languages",
            options=list(language_map.keys()),
            default=['en'],
            format_func=lambda code: language_map[code],
            help="Select languages for campaign generation"
        )

        # Aspect Ratios
        aspect_ratios = st.multiselect(
            "Aspect Ratios",
            options=[
                ('1x1', '1:1 Square (Instagram) ◻️'),
                ('16x9', '16:9 Landscape (YouTube) ▬'),
                ('9x16', '9:16 Portrait (Stories) ▮'),
            ],
            default=[
                ('1x1', '1:1 Square (Instagram) ◻️'),
                ('16x9', '16:9 Landscape (YouTube) ▬'),
                ('9x16', '9:16 Portrait (Stories) ▮'),
            ],
            format_func=lambda x: x[1],
            help="Select aspect ratios for generated images"
        )

        selected_ratios = [ratio[0] for ratio in aspect_ratios]

    with col2:
        st.subheader("🎨 Style Options")

        font_size = st.slider(
            "Font Size",
            min_value=40,
            max_value=150,
            value=80,
            step=10,
            help="Adjust text overlay font size (pixels)"
        )

        text_position = st.selectbox(
            "Text Position",
            options=['top', 'center', 'bottom'],
            index=2,
            help="Position of text overlay on image"
        )

        # Generate AI image option
        generate_ai_image = st.checkbox(
            "Generate AI Images (DALL-E)",
            value=False,
            help="Use DALL-E to generate product images (requires API credits)"
        )

        # Use existing product images
        if not generate_ai_image:
            product_dir = Path("data/input/assets")
            products = []

            if product_dir.exists():
                products = [f.stem for f in product_dir.glob("*.png")]

            if products:
                selected_product = st.selectbox(
                    "Select Product Image",
                    options=products,
                    help="Choose from existing product images"
                )
            else:
                st.warning("No product images found in data/input/assets/")
                selected_product = None

    # ===== STEP 3: Advanced Options =====
    st.markdown("---")
    st.header("⚙️ Advanced Options")  # Always visible

    col3, col4 = st.columns(2)

    with col3:
        # Brand guidelines
        guidelines_file = st.file_uploader(
            "Brand Guidelines (Optional)",
            type=['json'],
            help="Upload brand guidelines for compliance checking"
        )

        # Output format
        output_format = st.selectbox(
            "Output Format",
            options=['PNG', 'JPEG'],
            help="Image output format"
        )

    with col4:
        # Quality settings
        image_quality = st.slider(
            "Image Quality",
            min_value=60,
            max_value=100,
            value=90,
            help="Image compression quality (higher = better quality, larger files)"
        )

    # Removed Add Watermark option completely

    # ===== STEP 4: Generate Button =====
    st.markdown("---")

    can_generate = brief_file is not None and len(selected_languages) > 0 and len(selected_ratios) > 0

    if not can_generate:
        if not brief_file:
            st.warning("⚠️ Please upload a campaign brief to continue")
        elif len(selected_languages) == 0:
            st.warning("⚠️ Please select at least one language")
        elif len(selected_ratios) == 0:
            st.warning("⚠️ Please select at least one aspect ratio")

    generate_button = st.button(
        "🚀 Generate Campaign",
        type="primary",
        disabled=not can_generate,
        use_container_width=True,
    )

    # ===== STEP 5: Campaign Generation =====
    if generate_button:
        file_extension = brief_file.name.split('.')[-1]
        brief_path = Path(f"data/input/briefs/temp_brief.{file_extension}")
        brief_path.parent.mkdir(parents=True, exist_ok=True)
        with open(brief_path, 'wb') as f:
            f.write(brief_file.getbuffer())

        progress_container = st.container()

        with progress_container:
            progress_bar = st.progress(0, text="Initializing...")
            status_text = st.empty()

            try:
                status_text.info("🔧 Initializing campaign pipeline...")
                progress_bar.progress(10)
                app_logger.info("Initializing pipeline")

                pipeline = CampaignPipeline()

                status_text.info("📄 Processing campaign brief...")
                progress_bar.progress(20)
                app_logger.info(f"Processing brief: {brief_path}")

                status_text.info("⚙️ Configuring campaign settings...")
                progress_bar.progress(30)

                # TODO: Configure pipeline with user selections

                status_text.info("🎨 Generating campaign assets...")
                progress_bar.progress(40)
                app_logger.info("Starting asset generation")

                output_dir = pipeline.run(brief_path=brief_path)

                progress_bar.progress(80)
                status_text.info("✨ Finalizing campaign...")
                progress_bar.progress(90)
                app_logger.info(f"Campaign generated: {output_dir}")

                progress_bar.progress(100)
                status_text.success("✅ Campaign generation complete!")

                import time
                time.sleep(1)

                progress_bar.empty()
                status_text.empty()

                st.balloons()

                # Extract campaign_id from output_dir
                if hasattr(output_dir, 'campaign_id'):
                    campaign_id = output_dir.campaign_id
                elif hasattr(output_dir, 'output_directory'):
                    campaign_id = Path(output_dir.output_directory).name
                elif hasattr(output_dir, 'path'):
                    campaign_id = Path(output_dir.path).name
                elif hasattr(output_dir, 'directory'):
                    campaign_id = Path(output_dir.directory).name
                elif hasattr(output_dir, 'output_path'):
                    campaign_id = Path(output_dir.output_path).name
                elif hasattr(output_dir, 'name'):
                    campaign_id = output_dir.name
                elif isinstance(output_dir, (str, Path)):
                    campaign_id = Path(output_dir).name
                else:
                    output_str = str(output_dir)
                    if "campaign_id='" in output_str:
                        start = output_str.find("campaign_id='") + len("campaign_id='")
                        end = output_str.find("'", start)
                        campaign_id = output_str[start:end]
                    elif "output_directory='" in output_str:
                        start = output_str.find("output_directory='") + len("output_directory='")
                        end = output_str.find("'", start)
                        campaign_id = Path(output_str[start:end]).name
                    else:
                        campaign_id = "campaign"

                # Display generated images in UI
                add_image_preview_to_existing_flow(output_dir=output_dir, campaign_id=campaign_id)

                brief_path.unlink(missing_ok=True)

            except FileNotFoundError as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ File not found: {e}")
                st.info("Please check that all required files are in place")

            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ Error generating campaign: {e}")
                app_logger.error(f"Campaign generation error: {e}", exc_info=True)
                with st.expander("🔍 Show error details"):
                    import traceback
                    st.code(traceback.format_exc())

                st.markdown("### Common Issues:")
                st.markdown("""
                - **Font errors**: Run `python scripts/maintenance/download_fonts.py`
                - **API errors**: Check your OpenAI API key in `.env`
                - **File errors**: Verify product images exist in `data/input/assets/`
                """)

    # ===== Sidebar Info =====
    st.sidebar.markdown("---")
    st.sidebar.subheader("ℹ️ About")
    st.sidebar.info(
        """
        **Social Campaign Generator** uses AI to create
        multi-language marketing campaigns with:

        - 🌍 Multi-language support (5 languages)
        - 🎨 AI image generation (DALL-E 3)
        - 📐 Multiple aspect ratios
        - ✅ Brand compliance checking
        - 📦 Batch processing

        **Version**: 1.0.0
        """
    )

    output_dir = Path("data/output")

    if output_dir.exists():
        campaigns = [d for d in output_dir.iterdir() if d.is_dir() and d.name.startswith('CAMP_')]
        if campaigns:
            st.sidebar.markdown("---")
            st.sidebar.subheader("📊 Statistics")
            st.sidebar.metric("Total Campaigns", len(campaigns))
            recent = sorted(campaigns, key=lambda x: x.stat().st_mtime, reverse=True)[0]
            images = len(list(recent.rglob("*.png")))
            st.sidebar.metric("Last Campaign Images", images)

if __name__ == "__main__":
    main()
