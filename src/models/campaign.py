"""
Data models for campaign briefs.
Defines the structure and validation for campaign data using Pydantic.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class Product(BaseModel):
    """Product information within a campaign."""
    
    product_id: str = Field(..., description="Unique product identifier")
    product_name: str = Field(..., description="Product name")
    description: str = Field(..., description="Product description")
    existing_image: Optional[str] = Field(None, description="Filename of existing image")
    generate_image: Optional[bool] = Field(False, description="Whether to generate image via AI")
    image_prompt: Optional[str] = Field(None, description="Prompt for AI image generation")
    
    @field_validator('product_name')
    @classmethod
    def validate_product_name(cls, v):
        """Ensure product name is not empty."""
        if not v or not v.strip():
            raise ValueError("Product name cannot be empty")
        return v.strip()
    
    def needs_generation(self) -> bool:
        """Check if this product needs AI image generation."""
        return self.generate_image or (not self.existing_image)


class CampaignBrief(BaseModel):
    """Complete campaign brief data model."""
    
    campaign_id: str = Field(..., description="Unique campaign identifier")
    campaign_name: str = Field(..., description="Campaign name")
    target_market: str = Field(..., description="Target market/country")
    language: str = Field(..., description="Language code (e.g., 'en', 'es')")
    target_audience: str = Field(..., description="Target audience description")
    
    products: List[Product] = Field(..., min_length=1, description="List of products in campaign")
    
    campaign_message: str = Field(..., description="Main campaign message")
    campaign_tagline: Optional[str] = Field(None, description="Campaign tagline")
    brand_colors: List[str] = Field(default_factory=list, description="Brand color hex codes")
    call_to_action: Optional[str] = Field("Learn More", description="Call to action text")
    aspect_ratios: List[str] = Field(
        default=["1:1", "9:16", "16:9"],
        description="Target aspect ratios"
    )
    notes: Optional[str] = Field(None, description="Additional notes")
    
    @field_validator('language')
    @classmethod
    def validate_language(cls, v):
        """Ensure language code is lowercase."""
        return v.lower().strip()
    
    @field_validator('products')
    @classmethod
    def validate_products(cls, v):
        """Ensure at least one product exists."""
        if not v:
            raise ValueError("Campaign must have at least one product")
        return v
    
    @field_validator('aspect_ratios')
    @classmethod
    def validate_aspect_ratios(cls, v):
        """Validate aspect ratio format."""
        for ratio in v:
            parts = ratio.split(':')
            if len(parts) != 2:
                raise ValueError(f"Invalid aspect ratio format: {ratio}")
            try:
                int(parts[0])
                int(parts[1])
            except ValueError:
                raise ValueError(f"Aspect ratio must be integers: {ratio}")
        return v
    
    def get_primary_color(self) -> str:
        """Get the primary brand color or default."""
        return self.brand_colors[0] if self.brand_colors else "#4285F4"
    
    def products_needing_generation(self) -> List[Product]:
        """Get list of products that need AI image generation."""
        return [p for p in self.products if p.needs_generation()]


class CampaignOutput(BaseModel):
    """Output metadata for generated campaign assets."""
    
    campaign_id: str
    campaign_name: str
    language: str
    generated_at: str
    output_directory: str
    generated_assets: List[dict] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    
    def add_asset(self, product_name: str, aspect_ratio: str, filepath: str):
        """Add a generated asset to the output record."""
        self.generated_assets.append({
            "product_name": product_name,
            "aspect_ratio": aspect_ratio,
            "filepath": filepath
        })
    
    def add_error(self, error_message: str):
        """Add an error to the output record."""
        self.errors.append(error_message)
    
    def success_count(self) -> int:
        """Get count of successfully generated assets."""
        return len(self.generated_assets)
    
    def has_errors(self) -> bool:
        """Check if any errors occurred."""
        return len(self.errors) > 0