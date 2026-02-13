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
        Escapes special characters for Telegram MarkdownV2, but preserves code blocks.
        """
        if not text:
            return ""

        # Pattern to find code blocks (```...``` or `...`)
        # We split the text by these blocks
        # Group 1: ```...``` (multiline code)
        # Group 2: `...` (inline code)
        pattern = re.compile(r'(```.*?```|`[^`]*`)', re.DOTALL)
        
        parts = pattern.split(text)
        
        escaped_parts = []
        for part in parts:
            if part.startswith('`') or part.startswith('```'):
                # This is a code block, leave it as is (but maybe escape backslashes if needed, 
                # strictly speaking inline code needs escaping of ` and \ but we assume valid block)
                escaped_parts.append(part)
            else:
                # This is normal text, escape ALL special chars
                # _ * [ ] ( ) ~ ` > # + - = | { } . !
                # We use re.sub to escape them
                escaped = re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', part)
                escaped_parts.append(escaped)
                
        return "".join(escaped_parts)

    @staticmethod
    def clean_bot_response(text: str) -> str:
        return MarkdownCleaner.escape(text)
