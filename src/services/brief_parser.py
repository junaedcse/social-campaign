"""
Brief Parser Service
Parses campaign briefs from JSON or YAML files into Pydantic models.
"""

import json
import yaml
from pathlib import Path
from typing import Union
from src.models.campaign import CampaignBrief
from src.utils.logger import app_logger


class BriefParser:
    """Parser for campaign brief files."""
    
    @staticmethod
    def parse_file(filepath: Union[str, Path]) -> CampaignBrief:
        """
        Parse a campaign brief from a file.
        
        Args:
            filepath: Path to JSON or YAML brief file
            
        Returns:
            CampaignBrief object
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid or parsing fails
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"Brief file not found: {filepath}")
        
        app_logger.info(f"Parsing brief file: {filepath.name}")
        
        # Determine format by extension
        if filepath.suffix.lower() == '.json':
            return BriefParser._parse_json(filepath)
        elif filepath.suffix.lower() in ['.yaml', '.yml']:
            return BriefParser._parse_yaml(filepath)
        else:
            raise ValueError(f"Unsupported file format: {filepath.suffix}")
    
    @staticmethod
    def _parse_json(filepath: Path) -> CampaignBrief:
        """Parse JSON brief file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            brief = CampaignBrief(**data)
            app_logger.info(
                f" Parsed JSON brief: {brief.campaign_id} "
                f"({len(brief.products)} products, {brief.language})"
            )
            return brief
            
        except json.JSONDecodeError as e:
            app_logger.error(f"Invalid JSON format: {e}")
            raise ValueError(f"Invalid JSON in {filepath.name}: {e}")
        except Exception as e:
            app_logger.error(f"Failed to parse JSON brief: {e}")
            raise ValueError(f"Failed to parse {filepath.name}: {e}")
    
    @staticmethod
    def _parse_yaml(filepath: Path) -> CampaignBrief:
        """Parse YAML brief file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            brief = CampaignBrief(**data)
            app_logger.info(
                f" Parsed YAML brief: {brief.campaign_id} "
                f"({len(brief.products)} products, {brief.language})"
            )
            return brief
            
        except yaml.YAMLError as e:
            app_logger.error(f"Invalid YAML format: {e}")
            raise ValueError(f"Invalid YAML in {filepath.name}: {e}")
        except Exception as e:
            app_logger.error(f"Failed to parse YAML brief: {e}")
            raise ValueError(f"Failed to parse {filepath.name}: {e}")
    
    @staticmethod
    def parse_string(content: str, format_type: str = 'json') -> CampaignBrief:
        """
        Parse campaign brief from string content.
        
        Args:
            content: String content of brief
            format_type: 'json' or 'yaml'
            
        Returns:
            CampaignBrief object
        """
        try:
            if format_type.lower() == 'json':
                data = json.loads(content)
            else:
                data = yaml.safe_load(content)
            
            return CampaignBrief(**data)
            
        except Exception as e:
            app_logger.error(f"Failed to parse brief string: {e}")
            raise ValueError(f"Failed to parse brief: {e}")
    
    @staticmethod
    def validate_brief(brief: CampaignBrief) -> tuple[bool, list[str]]:
        """
        Validate a campaign brief for completeness.
        
        Args:
            brief: CampaignBrief to validate
            
        Returns:
            Tuple of (is_valid, list of warnings/issues)
        """
        issues = []
        
        # Check for products
        if not brief.products:
            issues.append("No products defined")
        
        # Check each product
        for i, product in enumerate(brief.products):
            if not product.existing_image and not product.generate_image:
                issues.append(
                    f"Product '{product.product_name}' has no image source defined"
                )
            
            if product.generate_image and not product.image_prompt:
                issues.append(
                    f"Product '{product.product_name}' marked for generation but no prompt provided"
                )
        
        # Check aspect ratios
        if not brief.aspect_ratios:
            issues.append("No aspect ratios defined")
        
        # Check brand colors
        if not brief.brand_colors:
            issues.append("No brand colors defined (will use defaults)")
        
        is_valid = len(issues) == 0
        
        if issues:
            app_logger.warning(f"Brief validation issues: {issues}")
        else:
            app_logger.info(f" Brief validation passed for {brief.campaign_id}")
        
        return is_valid, issues