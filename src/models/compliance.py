"""
Brand Compliance Models
Data models for brand guidelines and compliance validation.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from pathlib import Path


class BrandGuidelines(BaseModel):
    """Brand guidelines and compliance rules."""
    
    brand_name: str = Field(..., description="Brand name")
    
    # Logo requirements
    logo_required: bool = Field(default=False, description="Whether logo must be present")
    logo_min_size_percent: float = Field(default=5.0, description="Minimum logo size as % of image")
    logo_position: Optional[str] = Field(None, description="Preferred logo position")
    
    # Color requirements
    required_colors: List[str] = Field(default_factory=list, description="Required brand colors (hex)")
    forbidden_colors: List[str] = Field(default_factory=list, description="Forbidden colors (hex)")
    color_tolerance: int = Field(default=30, description="Color matching tolerance (0-255)")
    
    # Text requirements
    min_text_size: int = Field(default=24, description="Minimum text size in pixels")
    max_text_length: int = Field(default=150, description="Maximum text length")
    forbidden_words: List[str] = Field(default_factory=list, description="Forbidden words")
    
    # Content requirements
    min_image_quality: int = Field(default=70, description="Minimum image quality (0-100)")
    required_aspect_ratios: Optional[List[str]] = Field(None, description="Required aspect ratios")
    
    # Metadata
    compliance_level: str = Field(default="standard", description="strict, standard, or relaxed")
    
    class Config:
        """Pydantic config."""
        validate_assignment = True


class ComplianceResult(BaseModel):
    """Result of compliance validation."""
    
    is_compliant: bool = Field(..., description="Overall compliance status")
    compliance_score: float = Field(..., description="Compliance score (0-100)")
    
    passed_checks: List[str] = Field(default_factory=list, description="Checks that passed")
    failed_checks: List[str] = Field(default_factory=list, description="Checks that failed")
    warnings: List[str] = Field(default_factory=list, description="Non-critical warnings")
    
    details: Dict[str, Any] = Field(default_factory=dict, description="Detailed check results")
    
    def add_passed(self, check_name: str, detail: Optional[str] = None):
        """Add a passed check."""
        self.passed_checks.append(check_name)
        if detail:
            self.details[check_name] = {"status": "passed", "detail": detail}
    
    def add_failed(self, check_name: str, reason: str):
        """Add a failed check."""
        self.failed_checks.append(check_name)
        self.details[check_name] = {"status": "failed", "reason": reason}
    
    def add_warning(self, check_name: str, message: str):
        """Add a warning."""
        self.warnings.append(message)
        self.details[check_name] = {"status": "warning", "message": message}
    
    def calculate_score(self):
        """Calculate overall compliance score."""
        total_checks = len(self.passed_checks) + len(self.failed_checks)
        if total_checks == 0:
            self.compliance_score = 100.0
        else:
            self.compliance_score = (len(self.passed_checks) / total_checks) * 100.0
        
        self.is_compliant = self.compliance_score >= 70.0 and len(self.failed_checks) == 0


class AssetMetadata(BaseModel):
    """Metadata for generated assets."""
    
    asset_id: str
    product_name: str
    campaign_id: str
    aspect_ratio: str
    
    # Image properties
    width: int
    height: int
    file_size: int
    format: str
    
    # Content properties
    has_text: bool = False
    text_content: Optional[str] = None
    dominant_colors: List[str] = Field(default_factory=list)
    
    # Compliance
    compliance_result: Optional[ComplianceResult] = None
    
    # Timestamps
    created_at: str
    validated_at: Optional[str] = None