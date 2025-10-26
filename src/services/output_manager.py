"""
Output Manager Service
Manages organization and storage of generated campaign assets.
"""

from pathlib import Path
from datetime import datetime
from typing import Optional
from PIL import Image
from src.config import settings
from src.utils.logger import app_logger
from src.models.campaign import CampaignOutput


class OutputManager:
    """Manages output directory structure and file saving."""
    
    def __init__(self, base_output_dir: Optional[Path] = None):
        """
        Initialize OutputManager.
        
        Args:
            base_output_dir: Base directory for outputs (defaults to config)
        """
        self.base_output_dir = base_output_dir or settings.output_base_dir
        self.base_output_dir = Path(self.base_output_dir)
        self.base_output_dir.mkdir(parents=True, exist_ok=True)
        
        app_logger.info(f"OutputManager initialized: {self.base_output_dir}")
    
    def create_campaign_directory(
        self,
        campaign_id: str,
        timestamp: Optional[datetime] = None
    ) -> Path:
        """
        Create directory structure for a campaign.
        
        Args:
            campaign_id: Campaign identifier
            timestamp: Optional timestamp (defaults to now)
            
        Returns:
            Path to campaign directory
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        # Create directory name: campaign_YYYYMMDD_HHMMSS
        dir_name = f"{campaign_id}_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        campaign_dir = self.base_output_dir / dir_name
        
        campaign_dir.mkdir(parents=True, exist_ok=True)
        
        app_logger.info(f"📁 Created campaign directory: {campaign_dir.name}")
        
        return campaign_dir
    
    def create_product_directory(
        self,
        campaign_dir: Path,
        product_name: str
    ) -> Path:
        """
        Create directory for a product within campaign.
        
        Args:
            campaign_dir: Campaign directory path
            product_name: Product name
            
        Returns:
            Path to product directory
        """
        # Sanitize product name for filesystem
        safe_name = self._sanitize_filename(product_name)
        product_dir = campaign_dir / safe_name
        
        product_dir.mkdir(parents=True, exist_ok=True)
        
        app_logger.debug(f"Created product directory: {product_dir.name}")
        
        return product_dir
    
    def save_asset(
        self,
        image: Image.Image,
        campaign_dir: Path,
        product_name: str,
        aspect_ratio: str,
        format: str = "PNG"
    ) -> Optional[Path]:
        """
        Save a generated asset.
        
        Args:
            image: PIL Image to save
            campaign_dir: Campaign directory
            product_name: Product name
            aspect_ratio: Aspect ratio (e.g., "16:9")
            format: Image format (PNG, JPEG)
            
        Returns:
            Path to saved file if successful, None otherwise
        """
        try:
            # Create product directory
            product_dir = self.create_product_directory(campaign_dir, product_name)
            
            # Create filename: aspectratio.ext
            ratio_str = aspect_ratio.replace(":", "x")
            filename = f"{ratio_str}.{format.lower()}"
            filepath = product_dir / filename
            
            # Save image
            image.save(filepath, format=format, optimize=True)
            
            file_size = filepath.stat().st_size
            app_logger.info(
                f" Saved asset: {product_name}/{filename} ({file_size:,} bytes)"
            )
            
            return filepath
            
        except Exception as e:
            app_logger.error(f"Failed to save asset for {product_name}: {e}")
            return None
    
    def save_metadata(
        self,
        campaign_dir: Path,
        output: CampaignOutput
    ) -> bool:
        """
        Save campaign metadata to JSON file.
        
        Args:
            campaign_dir: Campaign directory
            output: CampaignOutput object with metadata
            
        Returns:
            True if successful, False otherwise
        """
        try:
            import json
            
            metadata_file = campaign_dir / "metadata.json"
            
            metadata = {
                "campaign_id": output.campaign_id,
                "campaign_name": output.campaign_name,
                "language": output.language,
                "generated_at": output.generated_at,
                "output_directory": str(output.output_directory),
                "assets_count": output.success_count(),
                "generated_assets": output.generated_assets,
                "errors": output.errors
            }
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            app_logger.info(f" Saved metadata: {metadata_file.name}")
            return True
            
        except Exception as e:
            app_logger.error(f"Failed to save metadata: {e}")
            return False
    
    def get_relative_path(self, filepath: Path) -> str:
        """
        Get path relative to base output directory.
        
        Args:
            filepath: Absolute file path
            
        Returns:
            Relative path string
        """
        try:
            return str(filepath.relative_to(self.base_output_dir))
        except ValueError:
            return str(filepath)
    
    @staticmethod
    def _sanitize_filename(name: str) -> str:
        """
        Sanitize string for use as filename.
        
        Args:
            name: Original name
            
        Returns:
            Sanitized name
        """
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
        
        # Remove leading/trailing spaces and dots
        name = name.strip('. ')
        
        # Replace spaces with underscores
        name = name.replace(' ', '_')
        
        return name
    
    def list_campaigns(self) -> list[dict]:
        """
        List all campaign outputs.
        
        Returns:
            List of campaign info dictionaries
        """
        campaigns = []
        
        if not self.base_output_dir.exists():
            return campaigns
        
        for campaign_dir in self.base_output_dir.iterdir():
            if campaign_dir.is_dir():
                metadata_file = campaign_dir / "metadata.json"
                
                if metadata_file.exists():
                    try:
                        import json
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                        campaigns.append(metadata)
                    except Exception as e:
                        app_logger.warning(f"Could not read metadata for {campaign_dir.name}: {e}")
                else:
                    # Basic info without metadata
                    campaigns.append({
                        "campaign_id": campaign_dir.name,
                        "output_directory": str(campaign_dir)
                    })
        
        return sorted(campaigns, key=lambda x: x.get('generated_at', ''), reverse=True)