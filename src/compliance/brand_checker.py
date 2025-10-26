"""
Brand Compliance Checker
Main service for validating campaign assets against brand guidelines.
"""

from pathlib import Path
from typing import Optional
from PIL import Image
from datetime import datetime

from src.models.compliance import BrandGuidelines, ComplianceResult, AssetMetadata
from src.compliance.color_analyzer import ColorAnalyzer
from src.compliance.content_validator import ContentValidator
from src.utils.logger import app_logger


class BrandComplianceChecker:
    """Main brand compliance validation service."""
    
    def __init__(self, guidelines: Optional[BrandGuidelines] = None):
        """
        Initialize compliance checker.
        
        Args:
            guidelines: Brand guidelines to validate against
        """
        self.guidelines = guidelines
        self.color_analyzer = ColorAnalyzer()
        self.content_validator = ContentValidator()
        
        app_logger.info("BrandComplianceChecker initialized")
    
    def validate_asset(
        self,
        image: Image.Image,
        text_content: Optional[str] = None,
        asset_metadata: Optional[dict] = None
    ) -> ComplianceResult:
        """
        Validate an asset against brand guidelines.
        
        Args:
            image: PIL Image to validate
            text_content: Text content in the image (optional)
            asset_metadata: Additional metadata (optional)
            
        Returns:
            ComplianceResult with validation details
        """
        result = ComplianceResult(
            is_compliant=True,
            compliance_score=0.0
        )
        
        if not self.guidelines:
            app_logger.warning("No guidelines provided, skipping validation")
            result.add_warning("no_guidelines", "No brand guidelines configured")
            result.calculate_score()
            return result
        
        app_logger.info(f"🔍 Validating asset against {self.guidelines.brand_name} guidelines")
        
        # Color validation
        self._validate_colors(image, result)
        
        # Content validation
        if text_content:
            self._validate_text_content(text_content, result)
        
        # Image quality validation
        self._validate_image_quality(image, result)
        
        # Aspect ratio validation
        if asset_metadata and 'aspect_ratio' in asset_metadata:
            self._validate_aspect_ratio(image, asset_metadata['aspect_ratio'], result)
        
        # Calculate final score
        result.calculate_score()
        
        app_logger.info(
            f" Validation complete: {result.compliance_score:.1f}% "
            f"({len(result.passed_checks)} passed, {len(result.failed_checks)} failed)"
        )
        
        return result
    
    def _validate_colors(self, image: Image.Image, result: ComplianceResult):
        """Validate color compliance."""
        # Check required colors
        if self.guidelines.required_colors:
            all_present, missing = self.color_analyzer.validate_brand_colors(
                image,
                self.guidelines.required_colors,
                self.guidelines.color_tolerance
            )
            
            if all_present:
                result.add_passed(
                    "required_colors",
                    f"All {len(self.guidelines.required_colors)} brand colors present"
                )
            else:
                result.add_failed(
                    "required_colors",
                    f"Missing brand colors: {', '.join(missing)}"
                )
        
        # Check forbidden colors
        if self.guidelines.forbidden_colors:
            forbidden_found = self.color_analyzer.check_forbidden_colors(
                image,
                self.guidelines.forbidden_colors,
                self.guidelines.color_tolerance
            )
            
            if not forbidden_found:
                result.add_passed(
                    "forbidden_colors",
                    "No forbidden colors detected"
                )
            else:
                colors_str = ", ".join([f"{c} ({p:.1f}%)" for c, p in forbidden_found])
                result.add_failed(
                    "forbidden_colors",
                    f"Forbidden colors found: {colors_str}"
                )
    
    def _validate_text_content(self, text: str, result: ComplianceResult):
        """Validate text content."""
        # Check text length
        is_valid, message = self.content_validator.check_text_length(
            text,
            self.guidelines.max_text_length
        )
        
        if is_valid:
            result.add_passed("text_length", message)
        else:
            result.add_failed("text_length", message)
        
        # Check forbidden words
        if self.guidelines.forbidden_words:
            is_valid, found_words = self.content_validator.check_forbidden_words(
                text,
                self.guidelines.forbidden_words
            )
            
            if is_valid:
                result.add_passed("forbidden_words", "No forbidden words detected")
            else:
                result.add_failed(
                    "forbidden_words",
                    f"Forbidden words found: {', '.join(found_words)}"
                )
        
        # Check readability
        is_readable, ratio = self.content_validator.check_text_readability(text)
        
        if is_readable:
            result.add_passed("text_readability", f"Text is readable (ratio: {ratio:.1f})")
        else:
            result.add_warning(
                "text_readability",
                f"Text may be hard to read (ratio: {ratio:.1f})"
            )
    
    def _validate_image_quality(self, image: Image.Image, result: ComplianceResult):
        """Validate image quality."""
        is_acceptable, quality = self.content_validator.check_image_quality(
            image,
            self.guidelines.min_image_quality
        )
        
        if is_acceptable:
            result.add_passed("image_quality", f"Quality acceptable ({quality})")
        else:
            result.add_failed(
                "image_quality",
                f"Quality too low ({quality} < {self.guidelines.min_image_quality})"
            )
    
    def _validate_aspect_ratio(
        self,
        image: Image.Image,
        aspect_ratio: str,
        result: ComplianceResult
    ):
        """Validate aspect ratio."""
        if not self.guidelines.required_aspect_ratios:
            return
        
        if aspect_ratio in self.guidelines.required_aspect_ratios:
            result.add_passed(
                "aspect_ratio",
                f"Aspect ratio {aspect_ratio} is allowed"
            )
        else:
            result.add_failed(
                "aspect_ratio",
                f"Aspect ratio {aspect_ratio} not in allowed list: "
                f"{', '.join(self.guidelines.required_aspect_ratios)}"
            )
    
    def create_asset_metadata(
        self,
        image: Image.Image,
        filepath: Path,
        product_name: str,
        campaign_id: str,
        aspect_ratio: str,
        text_content: Optional[str] = None
    ) -> AssetMetadata:
        """
        Create comprehensive metadata for an asset.
        
        Args:
            image: PIL Image
            filepath: Path to saved file
            product_name: Product name
            campaign_id: Campaign ID
            aspect_ratio: Aspect ratio
            text_content: Text overlay content (optional)
            
        Returns:
            AssetMetadata object
        """
        # Extract dominant colors
        dominant_colors = self.color_analyzer.get_dominant_colors(image)
        
        # Create metadata
        metadata = AssetMetadata(
            asset_id=f"{campaign_id}_{product_name}_{aspect_ratio}",
            product_name=product_name,
            campaign_id=campaign_id,
            aspect_ratio=aspect_ratio,
            width=image.size[0],
            height=image.size[1],
            file_size=filepath.stat().st_size if filepath.exists() else 0,
            format=image.format or 'PNG',
            has_text=text_content is not None,
            text_content=text_content,
            dominant_colors=dominant_colors,
            created_at=datetime.now().isoformat()
        )
        
        # Run compliance check
        compliance = self.validate_asset(image, text_content)
        metadata.compliance_result = compliance
        metadata.validated_at = datetime.now().isoformat()
        
        return metadata
    
    def generate_compliance_report(self, results: list[ComplianceResult]) -> dict:
        """
        Generate summary report from multiple compliance results.
        
        Args:
            results: List of ComplianceResult objects
            
        Returns:
            Dictionary with summary statistics
        """
        if not results:
            return {"error": "No results to analyze"}
        
        total = len(results)
        compliant = sum(1 for r in results if r.is_compliant)
        avg_score = sum(r.compliance_score for r in results) / total
        
        # Collect all failed checks
        all_failed = {}
        for result in results:
            for check in result.failed_checks:
                all_failed[check] = all_failed.get(check, 0) + 1
        
        report = {
            "total_assets": total,
            "compliant_assets": compliant,
            "non_compliant_assets": total - compliant,
            "compliance_rate": (compliant / total) * 100,
            "average_score": avg_score,
            "common_failures": sorted(
                all_failed.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
        }
        
        app_logger.info(f"📊 Compliance Report: {report['compliance_rate']:.1f}% compliant")
        
        return report