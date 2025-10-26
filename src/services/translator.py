"""
Translation Service
Translates campaign messages using OpenAI GPT models.
"""

from typing import Optional
from openai import OpenAI
from src.config import settings
from src.utils.logger import app_logger


class TranslationService:
    """Translates text using OpenAI."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize TranslationService.
        
        Args:
            api_key: OpenAI API key (defaults to config)
        """
        self.api_key = api_key or settings.openai_api_key
        
        if not self.api_key:
            app_logger.warning("No OpenAI API key provided for translation")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)
            app_logger.info("TranslationService initialized")
    
    def translate(
        self,
        text: str,
        target_language: str,
        source_language: str = "en",
        context: Optional[str] = None
    ) -> Optional[str]:
        """
        Translate text to target language.
        
        Args:
            text: Text to translate
            target_language: Target language code (e.g., 'es', 'fr')
            source_language: Source language code (default: 'en')
            context: Additional context for translation (optional)
            
        Returns:
            Translated text if successful, None otherwise
        """
        if not self.client:
            app_logger.warning("Translation not available: No API key")
            return text  # Return original text
        
        # If source and target are the same, no translation needed
        if source_language.lower() == target_language.lower():
            return text
        
        # Language name mapping
        language_names = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'ja': 'Japanese',
            'zh': 'Chinese',
            'ko': 'Korean',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian'
        }
        
        target_lang_name = language_names.get(target_language.lower(), target_language)
        
        # Build translation prompt
        prompt = f"Translate the following text to {target_lang_name}. "
        
        if context:
            prompt += f"Context: {context}. "
        
        prompt += (
            "Maintain the tone and style. Keep any brand names unchanged. "
            "Provide only the translation without explanations.\n\n"
            f"Text: {text}"
        )
        
        app_logger.info(f"🌐 Translating to {target_lang_name}...")
        app_logger.debug(f"Original text: {text}")
        
        try:
            response = self.client.chat.completions.create(
                model=settings.translation_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional translator. Provide accurate, natural translations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            translated = response.choices[0].message.content.strip()
            app_logger.info(f" Translation complete: '{translated}'")
            
            return translated
            
        except Exception as e:
            app_logger.error(f"Translation failed: {e}")
            return text  # Return original on failure
    
    def translate_campaign_message(
        self,
        message: str,
        target_language: str,
        product_name: Optional[str] = None
    ) -> str:
        """
        Translate a campaign message with appropriate context.
        
        Args:
            message: Campaign message to translate
            target_language: Target language code
            product_name: Product name for context (optional)
            
        Returns:
            Translated message
        """
        context = "This is a marketing campaign message"
        if product_name:
            context += f" for a product called {product_name}"
        
        translated = self.translate(
            text=message,
            target_language=target_language,
            context=context
        )
        
        return translated or message
    
    def is_available(self) -> bool:
        """
        Check if translation service is available.
        
        Returns:
            True if API key is configured, False otherwise
        """
        return self.client is not None
    
    def batch_translate(
        self,
        texts: list[str],
        target_language: str,
        source_language: str = "en"
    ) -> list[str]:
        """
        Translate multiple texts.
        
        Args:
            texts: List of texts to translate
            target_language: Target language code
            source_language: Source language code
            
        Returns:
            List of translated texts
        """
        translations = []
        
        for text in texts:
            translated = self.translate(
                text=text,
                target_language=target_language,
                source_language=source_language
            )
            translations.append(translated or text)
        
        return translations