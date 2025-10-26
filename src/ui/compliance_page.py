"""
Brand Compliance Page for Streamlit UI
Adds compliance checking interface to the application.
"""

import streamlit as st
import json
from pathlib import Path
from PIL import Image

from src.models.compliance import BrandGuidelines
from src.compliance.brand_checker import BrandComplianceChecker
from src.compliance.color_analyzer import ColorAnalyzer


def render_compliance_page():
    """Render brand compliance configuration and testing page."""
    st.header("🔍 Brand Compliance")
    
    tab1, tab2, tab3 = st.tabs(["📋 Guidelines", " Test Asset", "📊 Reports"])
    
    with tab1:
        render_guidelines_editor()
    
    with tab2:
        render_asset_tester()
    
    with tab3:
        render_compliance_reports()


def render_guidelines_editor():
    """Render guidelines configuration interface."""
    st.subheader("Brand Guidelines Configuration")
    
    # Load or create guidelines
    guidelines_path = Path("examples/brand_guidelines.json")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Upload guidelines
        uploaded = st.file_uploader(
            "Upload brand guidelines JSON",
            type=['json'],
            help="Upload existing brand guidelines"
        )
        
        if uploaded:
            try:
                data = json.load(uploaded)
                guidelines = BrandGuidelines(**data)
                st.success(f" Loaded guidelines for {guidelines.brand_name}")
                display_guidelines(guidelines)
            except Exception as e:
                st.error(f" Invalid guidelines file: {e}")
        
        elif guidelines_path.exists():
            # Load example
            try:
                with open(guidelines_path, 'r') as f:
                    data = json.load(f)
                guidelines = BrandGuidelines(**data)
                st.info(f"📋 Showing example guidelines for {guidelines.brand_name}")
                display_guidelines(guidelines)
            except Exception as e:
                st.error(f"Error loading example: {e}")
    
    with col2:
        st.write("**Quick Actions**")
        
        if st.button("📄 Create New Guidelines"):
            st.session_state['create_guidelines'] = True
        
        if st.button("💾 Save Current"):
            st.info("Save functionality coming soon")
        
        if st.button("📥 Download Template"):
            template = {
                "brand_name": "Your Brand",
                "required_colors": ["#000000"],
                "forbidden_colors": [],
                "max_text_length": 150,
                "forbidden_words": [],
                "compliance_level": "standard"
            }
            st.download_button(
                "Download",
                json.dumps(template, indent=2),
                "brand_guidelines_template.json",
                "application/json"
            )


def display_guidelines(guidelines: BrandGuidelines):
    """Display guidelines in a readable format."""
    with st.expander("📋 View Guidelines Details", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Brand Information**")
            st.write(f"Name: {guidelines.brand_name}")
            st.write(f"Compliance Level: {guidelines.compliance_level}")
            
            st.write("\n**Color Requirements**")
            if guidelines.required_colors:
                st.write("Required Colors:")
                for color in guidelines.required_colors:
                    st.color_picker(color, color, key=f"req_{color}", disabled=True)
            
            if guidelines.forbidden_colors:
                st.write("Forbidden Colors:")
                for color in guidelines.forbidden_colors:
                    st.color_picker(color, color, key=f"forb_{color}", disabled=True)
        
        with col2:
            st.write("**Text Requirements**")
            st.write(f"Max Length: {guidelines.max_text_length} chars")
            st.write(f"Min Size: {guidelines.min_text_size}px")
            
            if guidelines.forbidden_words:
                st.write(f"Forbidden Words: {', '.join(guidelines.forbidden_words)}")
            
            st.write("\n**Quality Requirements**")
            st.write(f"Min Quality: {guidelines.min_image_quality}%")
            
            if guidelines.required_aspect_ratios:
                st.write(f"Aspect Ratios: {', '.join(guidelines.required_aspect_ratios)}")


def render_asset_tester():
    """Render interface for testing individual assets."""
    st.subheader("Test Individual Asset")
    
    # Load guidelines
    guidelines_path = Path("examples/brand_guidelines.json")
    guidelines = None
    
    if guidelines_path.exists():
        try:
            with open(guidelines_path, 'r') as f:
                data = json.load(f)
            guidelines = BrandGuidelines(**data)
        except Exception as e:
            st.error(f"Error loading guidelines: {e}")
            return
    else:
        st.warning(" No guidelines file found. Please create one first.")
        return
    
    # Upload image to test
    uploaded_image = st.file_uploader(
        "Upload image to test",
        type=['png', 'jpg', 'jpeg', 'webp'],
        help="Upload an asset to validate against guidelines"
    )
    
    if uploaded_image:
        # Display image
        image = Image.open(uploaded_image)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(image, caption="Asset to test", use_column_width=True)
        
        with col2:
            # Text content input
            text_content = st.text_area(
                "Text content in image (optional)",
                help="Enter any text that appears in the image"
            )
            
            if st.button("🔍 Run Compliance Check", type="primary"):
                # Run compliance check
                checker = BrandComplianceChecker(guidelines)
                
                with st.spinner("Analyzing asset..."):
                    result = checker.validate_asset(image, text_content)
                
                # Display results
                st.divider()
                display_compliance_results(result)


def display_compliance_results(result):
    """Display compliance check results."""
    # Overall status
    if result.is_compliant:
        st.success(f" Asset is compliant ({result.compliance_score:.1f}%)")
    else:
        st.error(f" Asset is not compliant ({result.compliance_score:.1f}%)")
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Compliance Score", f"{result.compliance_score:.0f}%")
    
    with col2:
        st.metric("Passed Checks", len(result.passed_checks))
    
    with col3:
        st.metric("Failed Checks", len(result.failed_checks))
    
    # Detailed results
    if result.passed_checks:
        with st.expander(" Passed Checks", expanded=False):
            for check in result.passed_checks:
                detail = result.details.get(check, {})
                st.write(f"✓ **{check}**: {detail.get('detail', 'Passed')}")
    
    if result.failed_checks:
        with st.expander(" Failed Checks", expanded=True):
            for check in result.failed_checks:
                detail = result.details.get(check, {})
                st.write(f"✗ **{check}**: {detail.get('reason', 'Failed')}")
    
    if result.warnings:
        with st.expander(" Warnings", expanded=False):
            for warning in result.warnings:
                st.write(f"⚠ {warning}")


def render_compliance_reports():
    """Render compliance reports from past campaigns."""
    st.subheader("Campaign Compliance Reports")
    
    # Look for compliance reports in output directory
    output_dir = Path("data/output")
    
    if not output_dir.exists():
        st.info("No campaign outputs found yet.")
        return
    
    # Find all compliance reports
    reports = list(output_dir.rglob("compliance_report.json"))
    
    if not reports:
        st.info("No compliance reports found. Generate a campaign with compliance enabled.")
        return
    
    # Display reports
    for report_path in sorted(reports, reverse=True):
        campaign_name = report_path.parent.name
        
        with st.expander(f"📊 {campaign_name}"):
            try:
                with open(report_path, 'r') as f:
                    report_data = json.load(f)
                
                # Display summary
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Assets", report_data.get('total_assets', 0))
                
                with col2:
                    st.metric("Compliant", report_data.get('compliant_assets', 0))
                
                with col3:
                    compliance_rate = report_data.get('compliance_rate', 0)
                    st.metric("Compliance Rate", f"{compliance_rate:.0f}%")
                
                # Common failures
                if 'common_failures' in report_data and report_data['common_failures']:
                    st.write("**Most Common Issues:**")
                    for check, count in report_data['common_failures']:
                        st.write(f"- {check}: {count} occurrences")
                
            except Exception as e:
                st.error(f"Error loading report: {e}")


# Add to main app.py by importing and calling in a new tab
if __name__ == "__main__":
    render_compliance_page()