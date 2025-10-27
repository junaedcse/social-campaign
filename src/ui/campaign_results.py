"""
Enhanced Campaign Generation UI with Image Preview

This module adds image preview functionality to display generated
campaign images in the UI before downloading.
"""

import streamlit as st
from pathlib import Path
from typing import List, Dict
import json
from PIL import Image
from pathlib import Path

def display_campaign_results(output_dir, metadata: Dict = None):
    """
    Display generated campaign images with organized layout.
    
    Args:
        output_dir: Path to campaign output directory (can be Path, str, or CampaignOutput object)
        metadata: Campaign metadata dictionary
    """
    st.markdown("---")
    st.header("🎨 Generated Campaign Assets")
    
    if metadata:
        # Display campaign info
        st.subheader("📋 Campaign Information")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Campaign ID", metadata.get('campaign_id', 'N/A'))
        with col2:
            st.metric("Total Assets", metadata.get('total_assets', 0))
        with col3:
            st.metric("Languages", len(metadata.get('languages', [])))
        
        st.markdown("---")
    
    # Convert output_dir to Path object
    # Handle CampaignOutput object or similar custom types
    if hasattr(output_dir, 'output_directory'):
        output_path = Path(output_dir.output_directory)
    elif hasattr(output_dir, 'path'):
        output_path = Path(output_dir.path)
    elif hasattr(output_dir, 'directory'):
        output_path = Path(output_dir.directory)
    elif hasattr(output_dir, 'output_path'):
        output_path = Path(output_dir.output_path)
    elif isinstance(output_dir, (str, Path)):
        output_path = Path(output_dir)
    else:
        # Last resort: try to extract from string representation
        output_str = str(output_dir)
        if "output_directory='" in output_str:
            # Extract path from string like "output_directory='data/output/...'"
            start = output_str.find("output_directory='") + len("output_directory='")
            end = output_str.find("'", start)
            output_path = Path(output_str[start:end])
        else:
            raise ValueError(f"Cannot extract path from output_dir: {type(output_dir)}")
    
    # Get all product directories
    product_dirs = [d for d in output_path.iterdir() if d.is_dir()]
    
    if not product_dirs:
        st.warning("No products found in output directory")
        return
    
    # Create tabs for each product
    if len(product_dirs) > 1:
        tabs = st.tabs([d.name for d in product_dirs])
    else:
        tabs = [st.container()]
    
    # Display each product
    for idx, product_dir in enumerate(product_dirs):
        with tabs[idx]:
            display_product_images(product_dir)


def display_product_images(product_dir: Path):
    """
    Display all images for a single product organized by aspect ratio.
    
    Args:
        product_dir: Path to product directory
    """
    st.subheader(f"📦 {product_dir.name}")
    
    # Get all image files
    image_files = sorted(product_dir.glob("*.png"))
    
    if not image_files:
        st.warning(f"No images found for {product_dir.name}")
        return
    
    # Organize images by aspect ratio
    images_by_ratio = {}
    for img_file in image_files:
        # Extract aspect ratio from filename (e.g., "1x1.png", "16x9_en.png")
        parts = img_file.stem.split('_')
        ratio = parts[0] if parts[0] in ['1x1', '16x9', '9x16'] else 'other'
        
        if ratio not in images_by_ratio:
            images_by_ratio[ratio] = []
        images_by_ratio[ratio].append(img_file)
    
    # Display images organized by aspect ratio
    aspect_ratios = ['1x1', '16x9', '9x16', 'other']
    
    for ratio in aspect_ratios:
        if ratio not in images_by_ratio:
            continue
        
        images = images_by_ratio[ratio]
        
        # Aspect ratio header with emoji
        ratio_emoji = {
            '1x1': '◻️',
            '16x9': '▬',
            '9x16': '▮',
            'other': '🖼️'
        }
        
        ratio_name = {
            '1x1': '1:1 Square',
            '16x9': '16:9 Landscape',
            '9x16': '9:16 Portrait',
            'other': 'Other'
        }
        
        st.markdown(f"### {ratio_emoji.get(ratio, '🖼️')} {ratio_name.get(ratio, ratio.upper())}")
        
        # Display images in columns
        cols_per_row = 3 if ratio == '1x1' else 2
        
        for i in range(0, len(images), cols_per_row):
            cols = st.columns(cols_per_row)
            
            for col_idx, img_path in enumerate(images[i:i + cols_per_row]):
                with cols[col_idx]:
                    display_single_image(img_path)
        
        st.markdown("---")


def display_single_image(img_path: Path):
    """
    Display a single image with metadata.
    
    Args:
        img_path: Path to image file
    """
    try:
        # Load image
        image = Image.open(img_path)
        
        # Display image (use_column_width for older Streamlit, use_container_width for newer)
        try:
            st.image(image, use_container_width=True)
        except TypeError:
            # Fallback for older Streamlit versions
            st.image(image, use_column_width=True)
        
        # Image metadata
        st.caption(f"📄 **{img_path.name}**")
        st.caption(f"📐 Size: {image.width}×{image.height}px")
        
        # File size
        file_size_kb = img_path.stat().st_size / 1024
        if file_size_kb > 1024:
            st.caption(f"💾 {file_size_kb/1024:.2f} MB")
        else:
            st.caption(f"💾 {file_size_kb:.1f} KB")
        
        # Download button for individual image
        with open(img_path, 'rb') as f:
            st.download_button(
                label="⬇️ Download",
                data=f.read(),
                file_name=img_path.name,
                mime="image/png",
                key=f"download_{img_path.stem}_{hash(img_path)}",
                use_container_width=True
            )
        
    except Exception as e:
        st.error(f"Error loading image: {e}")


def create_download_zip_button(output_dir, campaign_id: str):
    """
    Create a download button for zipped campaign assets.
    
    Args:
        output_dir: Path to campaign output directory (can be Path, str, or CampaignOutput object)
        campaign_id: Campaign identifier
    """
    import zipfile
    import io
    
    st.markdown("---")
    st.header("📦 Download All Assets")
    
    # Convert output_dir to Path object
    if hasattr(output_dir, 'output_directory'):
        output_path = Path(output_dir.output_directory)
    elif hasattr(output_dir, 'path'):
        output_path = Path(output_dir.path)
    elif hasattr(output_dir, 'directory'):
        output_path = Path(output_dir.directory)
    elif hasattr(output_dir, 'output_path'):
        output_path = Path(output_dir.output_path)
    elif isinstance(output_dir, (str, Path)):
        output_path = Path(output_dir)
    else:
        # Last resort: try to extract from string representation
        output_str = str(output_dir)
        if "output_directory='" in output_str:
            start = output_str.find("output_directory='") + len("output_directory='")
            end = output_str.find("'", start)
            output_path = Path(output_str[start:end])
        else:
            raise ValueError(f"Cannot extract path from output_dir: {type(output_dir)}")
    
    try:
        # Create zip in memory
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add all files from output directory
            for file_path in output_path.rglob('*'):
                if file_path.is_file():
                    # Get relative path for zip
                    arcname = file_path.relative_to(output_path.parent)
                    zip_file.write(file_path, arcname=str(arcname))
        
        # Reset buffer position
        zip_buffer.seek(0)
        
        # Display download button
        st.download_button(
            label="⬇️ Download All Assets (ZIP)",
            data=zip_buffer.read(),
            file_name=f"{campaign_id}_assets.zip",
            mime="application/zip",
            type="primary",
            use_container_width=True
        )
        
        st.success(f"✅ Campaign generated successfully! Assets ready for download.")
        
    except Exception as e:
        st.error(f"Error creating zip file: {e}")


def display_campaign_summary(output_dir):
    """
    Display summary statistics about generated campaign.
    
    Args:
        output_dir: Path to campaign output directory (can be Path, str, or CampaignOutput object)
    """
    st.markdown("---")
    st.subheader("📊 Campaign Summary")
    
    # Convert output_dir to Path object
    if hasattr(output_dir, 'output_directory'):
        output_path = Path(output_dir.output_directory)
    elif hasattr(output_dir, 'path'):
        output_path = Path(output_dir.path)
    elif hasattr(output_dir, 'directory'):
        output_path = Path(output_dir.directory)
    elif hasattr(output_dir, 'output_path'):
        output_path = Path(output_dir.output_path)
    elif isinstance(output_dir, (str, Path)):
        output_path = Path(output_dir)
    else:
        # Last resort: try to extract from string representation
        output_str = str(output_dir)
        if "output_directory='" in output_str:
            start = output_str.find("output_directory='") + len("output_directory='")
            end = output_str.find("'", start)
            output_path = Path(output_str[start:end])
        else:
            raise ValueError(f"Cannot extract path from output_dir: {type(output_dir)}")
    
    # Count files
    total_images = len(list(output_path.rglob("*.png")))
    total_products = len([d for d in output_path.iterdir() if d.is_dir()])
    
    # Calculate total size
    total_size = sum(f.stat().st_size for f in output_path.rglob("*") if f.is_file())
    total_size_mb = total_size / (1024 * 1024)
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Images", total_images)
    with col2:
        st.metric("Products", total_products)
    with col3:
        st.metric("Total Size", f"{total_size_mb:.2f} MB")


# Enhanced main UI function
def render_campaign_generation_ui():
    """
    Enhanced campaign generation UI with image preview.
    
    This replaces or enhances your existing campaign generation page.
    """
    st.header("🎨 Campaign Generation")
    
    # Brief upload section
    st.subheader("1️⃣ Upload Campaign Brief")
    brief_file = st.file_uploader(
        "Upload Campaign Brief",
        type=['json', 'yaml', 'yml'],
        help="Upload your campaign brief file (JSON or YAML format)"
    )
    
    # Configuration section
    st.subheader("2️⃣ Configure Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Language selection
        languages = st.multiselect(
            "Target Languages",
            options=['en', 'fr', 'es', 'de', 'ja', 'zh', 'ko'],
            default=['en'],
            help="Select languages for campaign generation"
        )
        
        # Aspect ratios
        aspect_ratios = st.multiselect(
            "Aspect Ratios",
            options=['1x1', '16x9', '9x16'],
            default=['1x1', '16x9', '9x16'],
            help="Select aspect ratios for generated images"
        )
    
    with col2:
        # Font size
        font_size = st.slider(
            "Font Size",
            min_value=40,
            max_value=150,
            value=80,
            step=10,
            help="Adjust text overlay font size"
        )
        
        # Product selection
        product_dir = Path("data/input/assets")
        products = [f.stem for f in product_dir.glob("*.png")] if product_dir.exists() else []
        
        selected_product = st.selectbox(
            "Product",
            options=products,
            help="Select product image"
        ) if products else None
    
    # Generate button
    st.markdown("---")
    
    if st.button("🚀 Generate Campaign", type="primary", use_container_width=True):
        if not brief_file:
            st.error("Please upload a campaign brief first")
            return
        
        # Show progress
        with st.spinner("Generating campaign assets..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Import your pipeline
                from src.services.pipeline import CampaignPipeline
                
                # Initialize pipeline
                status_text.text("Initializing pipeline...")
                progress_bar.progress(10)
                
                pipeline = CampaignPipeline()
                
                # Process brief
                status_text.text("Processing campaign brief...")
                progress_bar.progress(20)
                
                # TODO: Parse brief file and configure pipeline
                # This depends on your existing implementation
                
                # Generate assets
                status_text.text("Generating images...")
                progress_bar.progress(40)
                
                # TODO: Call your pipeline.run() method
                # output_dir = pipeline.run(brief_path=brief_file)
                
                # For demonstration, assuming output directory exists
                output_dir = Path("data/output/CAMP_2025_001_20251027_120000")
                
                progress_bar.progress(80)
                status_text.text("Finalizing...")
                
                # Convert output_dir to Path object
                if hasattr(output_dir, 'path'):
                    actual_output_dir = Path(output_dir.path)
                elif hasattr(output_dir, 'directory'):
                    actual_output_dir = Path(output_dir.directory)
                elif hasattr(output_dir, 'output_path'):
                    actual_output_dir = Path(output_dir.output_path)
                else:
                    actual_output_dir = Path(str(output_dir))
                
                # Load metadata
                metadata_path = actual_output_dir / "metadata.json"


                metadata = None
                if metadata_path.exists():
                    with open(metadata_path) as f:
                        metadata = json.load(f)
                
                progress_bar.progress(100)
                status_text.text("Complete!")
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                # Display results
                st.success("✅ Campaign generated successfully!")
                
                # Display images in UI
                display_campaign_results(output_dir, metadata)
                
                # Display summary
                display_campaign_summary(output_dir)
                
                # Download button
                campaign_id = output_dir.name
                create_download_zip_button(output_dir, campaign_id)
                
            except Exception as e:
                st.error(f"Error generating campaign: {e}")
                import traceback
                with st.expander("Show error details"):
                    st.code(traceback.format_exc())


# Alternative: Add to existing campaign generation flow
def add_image_preview_to_existing_flow(output_dir, campaign_id: str):
    """
    Add image preview to your existing campaign generation flow.
    
    Call this function after your pipeline completes successfully.
    
    Usage:
        output_dir = pipeline.run(brief_path)
        add_image_preview_to_existing_flow(output_dir, campaign_id)
    
    Args:
        output_dir: Path to campaign output directory (can be Path, str, or CampaignOutput object)
        campaign_id: Campaign identifier
    """
    # Convert output_dir to Path object
    if hasattr(output_dir, 'output_directory'):
        output_path = Path(output_dir.output_directory)
    elif hasattr(output_dir, 'path'):
        output_path = Path(output_dir.path)
    elif hasattr(output_dir, 'directory'):
        output_path = Path(output_dir.directory)
    elif hasattr(output_dir, 'output_path'):
        output_path = Path(output_dir.output_path)
    elif isinstance(output_dir, (str, Path)):
        output_path = Path(output_dir)
    else:
        # Last resort: try to extract from string representation
        output_str = str(output_dir)
        if "output_directory='" in output_str:
            start = output_str.find("output_directory='") + len("output_directory='")
            end = output_str.find("'", start)
            output_path = Path(output_str[start:end])
        else:
            raise ValueError(f"Cannot extract path from output_dir: {type(output_dir)}")
    
    # Load metadata if exists
    metadata_path = output_path / "metadata.json"
    metadata = None
    if metadata_path.exists():
        with open(metadata_path) as f:
            metadata = json.load(f)
    
    # Display results
    st.success("✅ Campaign generated successfully!")
    
    # Show images
    display_campaign_results(output_dir, metadata)
    
    # Show summary
    display_campaign_summary(output_dir)
    
    # Download button
    create_download_zip_button(output_dir, campaign_id)


# Compact version for smaller screens
def display_campaign_results_compact(output_dir):
    """
    Compact version of results display for smaller screens.
    
    Args:
        output_dir: Path to campaign output directory (can be Path, str, or CampaignOutput object)
    """
    st.markdown("---")
    st.header("🎨 Generated Assets")
    
    # Convert output_dir to Path object
    if hasattr(output_dir, 'output_directory'):
        output_path = Path(output_dir.output_directory)
    elif hasattr(output_dir, 'path'):
        output_path = Path(output_dir.path)
    elif hasattr(output_dir, 'directory'):
        output_path = Path(output_dir.directory)
    elif hasattr(output_dir, 'output_path'):
        output_path = Path(output_dir.output_path)
    elif isinstance(output_dir, (str, Path)):
        output_path = Path(output_dir)
    else:
        # Last resort: try to extract from string representation
        output_str = str(output_dir)
        if "output_directory='" in output_str:
            start = output_str.find("output_directory='") + len("output_directory='")
            end = output_str.find("'", start)
            output_path = Path(output_str[start:end])
        else:
            raise ValueError(f"Cannot extract path from output_dir: {type(output_dir)}")
    
    # Get all images
    image_files = sorted(output_path.rglob("*.png"))
    
    if not image_files:
        st.warning("No images generated")
        return
    
    # Simple gallery view
    for img_path in image_files:
        with st.expander(f"📷 {img_path.parent.name} - {img_path.name}"):
            try:
                image = Image.open(img_path)
                # Handle Streamlit version compatibility
                try:
                    st.image(image, use_container_width=True)
                except TypeError:
                    st.image(image, use_column_width=True)
                
                # Download button
                with open(img_path, 'rb') as f:
                    st.download_button(
                        label="⬇️ Download",
                        data=f.read(),
                        file_name=img_path.name,
                        mime="image/png",
                        key=f"dl_{img_path.stem}"
                    )
            except Exception as e:
                st.error(f"Error: {e}")


# Example integration with existing app.py
"""
# In your app.py, after pipeline completes:

if st.button("Generate Campaign"):
    with st.spinner("Generating..."):
        # Your existing pipeline code
        from src.services.pipeline import CampaignPipeline
        
        pipeline = CampaignPipeline()
        output_dir = pipeline.run(brief_path=brief_file)
        
        # NEW: Add image preview
        from src.ui.campaign_results import add_image_preview_to_existing_flow
        
        add_image_preview_to_existing_flow(
            output_dir=output_dir,
            campaign_id=output_dir.name
        )
"""


if __name__ == "__main__":
    """Test the UI components."""
    st.set_page_config(page_title="Campaign Results", layout="wide")
    
    # Test with existing output
    test_output = Path("data/output/CAMP_2025_002_20251026_144502")
    
    if test_output.exists():
        st.title("🎨 Campaign Generator - Test View")
        display_campaign_results(test_output)
        create_download_zip_button(test_output, test_output.name)
    else:
        st.warning(f"Test output directory not found: {test_output}")
        st.info("Generate a campaign first to see results")