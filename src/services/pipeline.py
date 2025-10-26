"""
Campaign Pipeline Orchestrator
Main pipeline that coordinates all services to generate campaign assets.
"""

from pathlib import Path
from datetime import datetime
from typing import Optional
from src.models.campaign import CampaignBrief, CampaignOutput
from src.services.brief_parser import BriefParser
from src.services.asset_manager import AssetManager
from src.services.image_generator import ImageGenerator
from src.services.image_processor import ImageProcessor
from src.services.translator import TranslationService
from src.services.output_manager import OutputManager
from src.utils.logger import app_logger
from src.config import settings


class CampaignPipeline:
    """Main pipeline for campaign asset generation."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize pipeline with all services.
        
        Args:
            api_key: OpenAI API key (optional, uses config if not provided)
        """
        self.brief_parser = BriefParser()
        self.asset_manager = AssetManager()
        self.image_generator = ImageGenerator(api_key=api_key)
        self.image_processor = ImageProcessor()
        self.translator = TranslationService(api_key=api_key)
        self.output_manager = OutputManager()
        
        app_logger.info(" Campaign Pipeline initialized")
    
    def run(self, brief_path: Path) -> CampaignOutput:
        """
        Run complete pipeline for a campaign brief.
        
        Args:
            brief_path: Path to campaign brief file
            
        Returns:
            CampaignOutput with results and metadata
        """
        app_logger.info("=" * 70)
        app_logger.info(f" Starting Campaign Pipeline")
        app_logger.info(f"📄 Brief: {brief_path.name}")
        app_logger.info("=" * 70)
        
        # Step 1: Parse brief
        try:
            brief = self.brief_parser.parse_file(brief_path)
            app_logger.info(f" Parsed brief: {brief.campaign_name}")
        except Exception as e:
            app_logger.error(f" Failed to parse brief: {e}")
            raise
        
        # Create output tracking
        output = CampaignOutput(
            campaign_id=brief.campaign_id,
            campaign_name=brief.campaign_name,
            language=brief.language,
            generated_at=datetime.now().isoformat(),
            output_directory=""
        )
        
        # Step 2: Create output directory
        campaign_dir = self.output_manager.create_campaign_directory(brief.campaign_id)
        output.output_directory = str(campaign_dir)
        
        # Step 3: Process each product
        for product in brief.products:
            app_logger.info(f"\n📦 Processing product: {product.product_name}")
            
            try:
                # Get or generate base image
                base_image = self._get_or_generate_image(product)
                
                if not base_image:
                    error_msg = f"Could not obtain image for {product.product_name}"
                    app_logger.error(f" {error_msg}")
                    output.add_error(error_msg)
                    continue
                
                # Translate campaign message if needed
                message = self._translate_message(brief)
                
                # Generate assets for each aspect ratio
                for aspect_ratio in brief.aspect_ratios:
                    app_logger.info(f"  📐 Creating {aspect_ratio} asset...")
                    
                    try:
                        # Resize to aspect ratio
                        resized = self.image_processor.resize_to_aspect_ratio(
                            base_image,
                            aspect_ratio
                        )
                        
                        # Add text overlay
                        final_image = self.image_processor.add_text_overlay(
                            resized,
                            message,
                            position="bottom"
                        )
                        
                        # Save asset
                        saved_path = self.output_manager.save_asset(
                            final_image,
                            campaign_dir,
                            product.product_name,
                            aspect_ratio
                        )
                        
                        if saved_path:
                            output.add_asset(
                                product.product_name,
                                aspect_ratio,
                                self.output_manager.get_relative_path(saved_path)
                            )
                            app_logger.info(f"   Created {aspect_ratio} asset")
                        
                    except Exception as e:
                        error_msg = f"Failed to create {aspect_ratio} for {product.product_name}: {e}"
                        app_logger.error(f"   {error_msg}")
                        output.add_error(error_msg)
                
            except Exception as e:
                error_msg = f"Failed to process {product.product_name}: {e}"
                app_logger.error(f" {error_msg}")
                output.add_error(error_msg)
        
        # Step 4: Save metadata
        self.output_manager.save_metadata(campaign_dir, output)
        
        # Step 5: Summary
        self._print_summary(output)
        
        return output
    
    def _get_or_generate_image(self, product):
        """Get existing image or generate new one."""
        # Try to load existing image
        if product.existing_image:
            image = self.asset_manager.load_image(product.existing_image)
            if image:
                app_logger.info(f"   Loaded existing image: {product.existing_image}")
                return image
        
        # Generate new image if needed
        if product.needs_generation():
            if not self.image_generator.is_available():
                app_logger.warning("    Image generation not available (no API key)")
                return None
            
            app_logger.info(f"   Generating image via DALL-E...")
            
            image = self.image_generator.generate_product_image(
                product.product_name,
                product.description,
                prompt=product.image_prompt
            )
            
            if image:
                # Save generated image to assets
                filename = f"{product.product_name.lower().replace(' ', '_')}_generated.png"
                self.asset_manager.save_image(image, filename)
                app_logger.info(f"   Generated and saved: {filename}")
            
            return image
        
        return None
    
    def _translate_message(self, brief: CampaignBrief) -> str:
        """Translate campaign message if needed."""
        if brief.language.lower() == 'en':
            return brief.campaign_message
        
        if not self.translator.is_available():
            app_logger.warning("    Translation not available, using original message")
            return brief.campaign_message
        
        translated = self.translator.translate_campaign_message(
            brief.campaign_message,
            brief.language
        )
        
        return translated
    
    def _print_summary(self, output: CampaignOutput):
        """Print pipeline execution summary."""
        app_logger.info("\n" + "=" * 70)
        app_logger.info("📊 PIPELINE SUMMARY")
        app_logger.info("=" * 70)
        app_logger.info(f"Campaign: {output.campaign_name}")
        app_logger.info(f"Language: {output.language}")
        app_logger.info(f"Output: {output.output_directory}")
        app_logger.info(f"Assets Generated: {output.success_count()}")
        
        if output.has_errors():
            app_logger.warning(f"Errors: {len(output.errors)}")
            for error in output.errors:
                app_logger.warning(f"  - {error}")
        else:
            app_logger.info(" All assets generated successfully!")
        
        app_logger.info("=" * 70)