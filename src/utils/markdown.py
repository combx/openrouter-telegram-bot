import re

class MarkdownCleaner:
    """
    Cleaner for Telegram MarkdownV2.
    Telegram requires specific characters to be escaped:
    _ * [ ] ( ) ~ ` > # + - = | { } . !
    """
    
    # Characters that must be escaped in MarkdownV2
    ESCAPE_CHARS = r"_*[]()~`>#+-=|{}.!"
    
    @staticmethod
    def escape(text: str) -> str:
        """
        Escapes all special characters for MarkdownV2.
        Note: This is a robust escape, but might be too aggressive if the model 
        outputs valid Markdown (tables, bold, etc.).
        
        For LLM output, it's better to ONLY escape characters that are NOT part of valid syntax.
        However, parsing partial markdown stream is hard.
        
        A compromise: 
        If the model outputs code blocks (```), we preserve them.
        Inside code blocks, no escaping is needed (Telegram handles it).
        Outside blocks, we need to be careful.
        """
        # Simple implementation for now:
        # We rely on the fact that models usually produce valid markdown.
        # But Telegram's parser is strict.
        # Just creating a placeholder. For production, a more complex parser is needed.
        return text

    @staticmethod
    def clean_bot_response(text: str) -> str:
        # TODO: Implement a smarter cleaner that preserves code blocks but escapes stray punctuation
        return text
