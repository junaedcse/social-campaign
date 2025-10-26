"""
Enhanced Campaign Pipeline with Brand Compliance
Pipeline with integrated brand guidelines validation.
"""

from pathlib import Path
from datetime import datetime
from typing import Optional
import json

from src.models.campaign import CampaignBrief, CampaignOutput
from src.models.compliance import BrandGuidelines
from src.services.brief_parser import BriefParser
from src.services.asset_manager import AssetManager
from src.services.image_generator import ImageGenerator
from src.services.image_processor import ImageProcessor
from src.services.translator import TranslationService
from src.services.output_manager import OutputManager
from src.compliance.brand_checker import BrandComplianceChecker
from src.utils.logger import app_logger
from src.config import settings


class EnhancedCampaignPipeline:
    """Enhanced campaign pipeline with brand compliance."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        guidelines_path: Optional[Path] = None
    ):
        """
        Initialize enhanced pipeline.
        
        Args:
            api_key: OpenAI API key (optional)
            guidelines_path: Path to brand guidelines JSON (optional)
        """
        # Core services
        self.brief_parser = BriefParser()
        self.asset_manager = AssetManager()
        self.image_generator = ImageGenerator(api_key=api_key)
        self.image_processor = ImageProcessor()
        self.translator = TranslationService(api_key=api_key)
        self.output_manager = OutputManager()
        
        # Compliance
        self.guidelines = self._load_guidelines(guidelines_path)
        self.compliance_checker = BrandComplianceChecker(self.guidelines)
        
        app_logger.info(" Enhanced Campaign Pipeline initialized")
        if self.guidelines:
            app_logger.info(f"   📋 Brand: {self.guidelines.brand_name}")
    
    def _load_guidelines(self, path: Optional[Path]) -> Optional[BrandGuidelines]:
        """Load brand guidelines from file."""
        if not path:
            return None
        
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            guidelines = BrandGuidelines(**data)
            app_logger.info(f" Loaded guidelines for {guidelines.brand_name}")
            return guidelines
        except Exception as e:
            app_logger.warning(f"Could not load guidelines: {e}")
            return None
    
    def run(
        self,
        brief_path: Path,
        enable_compliance: bool = True
    ) -> CampaignOutput:
        """
        Run enhanced pipeline with compliance checking.
        
        Args:
            brief_path: Path to campaign brief
            enable_compliance: Whether to run compliance checks
            
        Returns:
            CampaignOutput with results and compliance data
        """
        app_logger.info("=" * 70)
        app_logger.info(f" Starting Enhanced Pipeline")
        app_logger.info(f"📄 Brief: {brief_path.name}")
        app_logger.info(f"🔍 Compliance: {'Enabled' if enable_compliance else 'Disabled'}")
        app_logger.info("=" * 70)
        
        # Parse brief
        try:
            brief = self.brief_parser.parse_file(brief_path)
            app_logger.info(f" Parsed: {brief.campaign_name}")
        except Exception as e:
            app_logger.error(f" Failed to parse: {e}")
            raise
        
        # Create output tracking
        output = CampaignOutput(
            campaign_id=brief.campaign_id,
            campaign_name=brief.campaign_name,
            language=brief.language,
            generated_at=datetime.now().isoformat(),
            output_directory=""
        )
        
        campaign_dir = self.output_manager.create_campaign_directory(brief.campaign_id)
        output.output_directory = str(campaign_dir)
        
        # Track compliance results
        compliance_results = []
        
        # Process each product
        for product in brief.products:
            app_logger.info(f"\n📦 Processing: {product.product_name}")
            
            try:
                # Get or generate base image
                base_image = self._get_or_generate_image(product)
                
                if not base_image:
                    error = f"Could not obtain image for {product.product_name}"
                    app_logger.error(f" {error}")
                    output.add_error(error)
                    continue
                
                # Translate message
                message = self._translate_message(brief)
                
                # Generate assets for each aspect ratio
                for aspect_ratio in brief.aspect_ratios:
                    app_logger.info(f"  📐 Creating {aspect_ratio}...")
                    
                    try:
                        # Resize
                        resized = self.image_processor.resize_to_aspect_ratio(
                            base_image, aspect_ratio
                        )
                        
                        # Add text
                        final = self.image_processor.add_text_overlay(
                            resized, message, position="bottom"
                        )
                        
                        # Save asset
                        saved_path = self.output_manager.save_asset(
                            final, campaign_dir, product.product_name, aspect_ratio
                        )
                        
                        if saved_path:
                            # Add to output
                            output.add_asset(
                                product.product_name,
                                aspect_ratio,
                                self.output_manager.get_relative_path(saved_path)
                            )
                            
                            # Run compliance check
                            if enable_compliance and self.guidelines:
                                compliance = self.compliance_checker.validate_asset(
                                    final,
                                    text_content=message,
                                    asset_metadata={
                                        'aspect_ratio': aspect_ratio,
                                        'product': product.product_name
                                    }
                                )
                                compliance_results.append(compliance)
                                
                                if compliance.is_compliant:
                                    app_logger.info(
                                        f"   Compliance: {compliance.compliance_score:.0f}%"
                                    )
                                else:
                                    app_logger.warning(
                                        f"    Compliance: {compliance.compliance_score:.0f}% "
                                        f"({len(compliance.failed_checks)} issues)"
                                    )
                            
                            app_logger.info(f"   Created {aspect_ratio}")
                    
                    except Exception as e:
                        error = f"Failed {aspect_ratio} for {product.product_name}: {e}"
                        app_logger.error(f"   {error}")
                        output.add_error(error)
            
            except Exception as e:
                error = f"Failed to process {product.product_name}: {e}"
                app_logger.error(f" {error}")
                output.add_error(error)
        
        # Save metadata and compliance report
        self.output_manager.save_metadata(campaign_dir, output)
        
        if compliance_results and enable_compliance:
            self._save_compliance_report(campaign_dir, compliance_results)
        
        # Print summary
        self._print_summary(output, compliance_results if enable_compliance else None)
        
        return output
    
    def _get_or_generate_image(self, product):
        """Get existing or generate new image."""
        if product.existing_image:
            image = self.asset_manager.load_image(product.existing_image)
            if image:
                app_logger.info(f"   Loaded: {product.existing_image}")
                return image
        
        if product.needs_generation():
            if not self.image_generator.is_available():
                app_logger.warning("    Generation unavailable")
                return None
            
            app_logger.info(f"   Generating via DALL-E...")
            image = self.image_generator.generate_product_image(
                product.product_name,
                product.description,
                prompt=product.image_prompt
            )
            
            if image:
                filename = f"{product.product_name.lower().replace(' ', '_')}_gen.png"
                self.asset_manager.save_image(image, filename)
            
            return image
        
        return None
    
    def _translate_message(self, brief):
        """Translate campaign message."""
        if brief.language.lower() == 'en':
            return brief.campaign_message
        
        if not self.translator.is_available():
            app_logger.warning("    Translation unavailable")
            return brief.campaign_message
        
        return self.translator.translate_campaign_message(
            brief.campaign_message, brief.language
        )
    
    def _save_compliance_report(self, campaign_dir: Path, results: list):
        """Save compliance report."""
        try:
            report = self.compliance_checker.generate_compliance_report(results)
            
            report_path = campaign_dir / "compliance_report.json"
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)
            
            app_logger.info(f"📊 Saved compliance report")
        except Exception as e:
            app_logger.error(f"Failed to save compliance report: {e}")
    
    def _print_summary(self, output, compliance_results=None):
        """Print pipeline summary."""
        app_logger.info("\n" + "=" * 70)
        app_logger.info("📊 PIPELINE SUMMARY")
        app_logger.info("=" * 70)
        app_logger.info(f"Campaign: {output.campaign_name}")
        app_logger.info(f"Language: {output.language}")
        app_logger.info(f"Output: {output.output_directory}")
        app_logger.info(f"Assets: {output.success_count()}")
        
        if compliance_results:
            compliant = sum(1 for r in compliance_results if r.is_compliant)
            total = len(compliance_results)
            avg_score = sum(r.compliance_score for r in compliance_results) / total
            
            app_logger.info(f"Compliance: {compliant}/{total} assets ({avg_score:.0f}% avg)")
        
        if output.has_errors():
            app_logger.warning(f"Errors: {len(output.errors)}")
        else:
            app_logger.info(" All successful!")
        
        app_logger.info("=" * 70)