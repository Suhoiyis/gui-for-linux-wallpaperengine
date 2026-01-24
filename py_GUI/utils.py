import re
from gi.repository import GLib

def markdown_to_pango(text: str) -> str:
    """
    Convert basic Markdown (*, **, ***) to Pango Markup (<i>, <b>, <b><i>).
    Handles XML escaping first.
    """
    if not text:
        return ""
        
    # 1. Escape XML characters first
    escaped = GLib.markup_escape_text(text)
    
    # 2. Bold+Italic ***text***
    # We use a pattern that allows spaces inside
    escaped = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', escaped)
    
    # 3. Bold **text**
    escaped = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', escaped)
    
    # 4. Italic *text*
    escaped = re.sub(r'\*(.+?)\*', r'<i>\1</i>', escaped)
    
    return escaped
