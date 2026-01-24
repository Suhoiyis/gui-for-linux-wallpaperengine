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
    escaped = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', escaped)
    
    # 3. Bold **text**
    escaped = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', escaped)
    
    # 4. Italic *text*
    escaped = re.sub(r'\*(.+?)\*', r'<i>\1</i>', escaped)
    
    return escaped

def bbcode_to_pango(text: str) -> str:
    """
    Convert Wallpaper Engine BBCode to Pango Markup.
    Strips images and handles basic formatting.
    """
    if not text:
        return ""

    # 1. Strip [img] tags entirely
    text = re.sub(r'\[img\].*?\[/img\]', '', text, flags=re.IGNORECASE)
    
    # 2. Handle [url=...]text[/url] -> text
    text = re.sub(r'\[url=.*?\](.*?)\[/url\]', r'\1', text, flags=re.IGNORECASE)
    
    # 3. Escape for Pango
    escaped = GLib.markup_escape_text(text)
    
    # 4. Basic formatting
    escaped = re.sub(r'\[b\](.*?)\[/b\]', r'<b>\1</b>', escaped, flags=re.IGNORECASE)
    escaped = re.sub(r'\[i\](.*?)\[/i\]', r'<i>\1</i>', escaped, flags=re.IGNORECASE)
    escaped = re.sub(r'\[h1\](.*?)\[/h1\]', r'<span size="large" weight="bold">\1</span>', escaped, flags=re.IGNORECASE)
    
    # 5. Clean up excessive whitespace/newlines
    escaped = escaped.replace('\r\n', '\n')
    lines = [line.strip() for line in escaped.split('\n')]
    cleaned_lines = []
    prev_empty = False
    for line in lines:
        if line:
            cleaned_lines.append(line)
            prev_empty = False
        elif not prev_empty:
            cleaned_lines.append(line)
            prev_empty = True
            
    return '\n'.join(cleaned_lines).strip()
