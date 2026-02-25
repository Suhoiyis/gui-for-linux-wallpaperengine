use std::fmt::Write;

/// Markdown/BBCode 转 Pango markup
/// 
/// 支持:
/// - **bold** → <b>bold</b>
/// - *italic* → <i>italic</i>
/// - [url=xxx]text[/url] → <a href="xxx">text</a>
/// - [color=red]text[/color] → <span color="red">text</span>
/// - XML 转义（& → &amp; 等）
pub fn markdown_to_pango(text: &str) -> String {
    let mut result = String::new();
    let mut chars = text.chars().peekable();
    
    while let Some(c) = chars.next() {
        match c {
            // XML 转义
            '&' => result.push_str("&amp;"),
            '<' => result.push_str("&lt;"),
            '>' => result.push_str("&gt;"),
            '"' => result.push_str("&quot;"),
            
            // **bold**
            '*' if chars.peek() == Some(&'*') => {
                chars.next();
                result.push_str("<b>");
                while let Some(&c) = chars.peek() {
                    if c == '*' {
                        chars.next();
                        if chars.peek() == Some(&'*') {
                            chars.next();
                            result.push_str("</b>");
                            break;
                        } else {
                            result.push('*');
                        }
                    } else {
                        result.push(chars.next().unwrap());
                    }
                }
            }
            
            // *italic*
            '*' => {
                result.push_str("<i>");
                while let Some(&c) = chars.peek() {
                    if c == '*' {
                        chars.next();
                        result.push_str("</i>");
                        break;
                    } else {
                        result.push(chars.next().unwrap());
                    }
                }
            }
            
            // [ 开始 BBCode
            '[' => {
                let mut bbcode = String::new();
                while let Some(&c) = chars.peek() {
                    if c == ']' {
                        chars.next();
                        break;
                    } else {
                        bbcode.push(chars.next().unwrap());
                    }
                }
                
                // 解析 BBCode
                if bbcode.starts_with("url=") {
                    if let Some(url) = bbcode.strip_prefix("url=") {
                        write!(result, "<a href=\"{}\">", escape_attr(url)).ok();
                        
                        // 读取链接文本
                        let mut link_text = String::new();
                        while let Some(&c) = chars.peek() {
                            if c == '[' {
                                chars.next();
                                let mut end_tag = String::new();
                                while let Some(&c) = chars.peek() {
                                    if c == ']' {
                                        chars.next();
                                        break;
                                    } else {
                                        end_tag.push(chars.next().unwrap());
                                    }
                                }
                                if end_tag == "/url" {
                                    break;
                                } else {
                                    link_text.push('[');
                                    link_text.push_str(&end_tag);
                                    link_text.push(']');
                                }
                            } else {
                                link_text.push(chars.next().unwrap());
                            }
                        }
                        result.push_str(&escape_html(&link_text));
                        result.push_str("</a>");
                    }
                } else if bbcode.starts_with("color=") {
                    if let Some(color) = bbcode.strip_prefix("color=") {
                        write!(result, "<span color=\"{}\">", escape_attr(color)).ok();
                        
                        // 读取文本直到 [/color]
                        let mut content = String::new();
                        while let Some(&c) = chars.peek() {
                            if c == '[' {
                                chars.next();
                                let mut end_tag = String::new();
                                while let Some(&c) = chars.peek() {
                                    if c == ']' {
                                        chars.next();
                                        break;
                                    } else {
                                        end_tag.push(chars.next().unwrap());
                                    }
                                }
                                if end_tag == "/color" {
                                    break;
                                } else {
                                    content.push('[');
                                    content.push_str(&end_tag);
                                    content.push(']');
                                }
                            } else {
                                content.push(chars.next().unwrap());
                            }
                        }
                        result.push_str(&escape_html(&content));
                        result.push_str("</span>");
                    }
                } else {
                    // 未知 BBCode，原样输出
                    write!(result, "[{}]", bbcode).ok();
                }
            }
            
            _ => result.push(c),
        }
    }
    
    result
}

/// HTML 转义
fn escape_html(text: &str) -> String {
    let mut result = String::new();
    for c in text.chars() {
        match c {
            '&' => result.push_str("&amp;"),
            '<' => result.push_str("&lt;"),
            '>' => result.push_str("&gt;"),
            _ => result.push(c),
        }
    }
    result
}

/// 属性转义（用于 href 等）
fn escape_attr(text: &str) -> String {
    let mut result = String::new();
    for c in text.chars() {
        match c {
            '&' => result.push_str("&amp;"),
            '<' => result.push_str("&lt;"),
            '>' => result.push_str("&gt;"),
            '"' => result.push_str("&quot;"),
            _ => result.push(c),
        }
    }
    result
}

/// 格式化文件大小
pub fn format_size(bytes: u64) -> String {
    const KB: u64 = 1024;
    const MB: u64 = KB * 1024;
    const GB: u64 = MB * 1024;
    
    if bytes >= GB {
        format!("{:.2} GB", bytes as f64 / GB as f64)
    } else if bytes >= MB {
        format!("{:.2} MB", bytes as f64 / MB as f64)
    } else if bytes >= KB {
        format!("{:.2} KB", bytes as f64 / KB as f64)
    } else {
        format!("{} B", bytes)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_bold() {
        assert_eq!(markdown_to_pango("**bold**"), "<b>bold</b>");
    }
    
    #[test]
    fn test_italic() {
        assert_eq!(markdown_to_pango("*italic*"), "<i>italic</i>");
    }
    
    #[test]
    fn test_mixed() {
        assert_eq!(markdown_to_pango("**bold** and *italic*"), "<b>bold</b> and <i>italic</i>");
    }
    
    #[test]
    fn test_xml_escape() {
        assert_eq!(markdown_to_pango("5 > 3 & 2 < 4"), "5 &gt; 3 &amp; 2 &lt; 4");
    }
    
    #[test]
    fn test_format_size() {
        assert_eq!(format_size(1024), "1.00 KB");
        assert_eq!(format_size(1048576), "1.00 MB");
        assert_eq!(format_size(500), "500 B");
    }
}
