use gtk4::prelude::*;
use std::collections::HashMap;

/// 壁纸属性类型
#[derive(Debug, Clone)]
pub enum PropertyType {
    Slider { min: f64, max: f64, step: f64 },
    Color,
    Boolean,
    Options { options: Vec<String> },
}

/// 壁纸属性
#[derive(Debug, Clone)]
pub struct WallpaperProperty {
    pub name: String,
    pub title: String,
    pub prop_type: PropertyType,
    pub value: String,
}

/// 属性编辑器组件
pub struct PropertiesEditor {
    properties: HashMap<String, WallpaperProperty>,
}

impl PropertiesEditor {
    pub fn new() -> Self {
        Self {
            properties: HashMap::new(),
        }
    }
    
    /// 解析后端返回的属性列表
    pub fn parse_properties(output: &str) -> Vec<WallpaperProperty> {
        let mut properties = Vec::new();
        
        for line in output.lines() {
            if line.contains('=') {
                let parts: Vec<&str> = line.splitn(2, '=').collect();
                if parts.len() == 2 {
                    properties.push(WallpaperProperty {
                        name: parts[0].trim().to_string(),
                        title: parts[0].trim().to_string(),
                        prop_type: PropertyType::Boolean,
                        value: parts[1].trim().to_string(),
                    });
                }
            }
        }
        
        properties
    }
}

impl Default for PropertiesEditor {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_properties_editor() {
        let editor = PropertiesEditor::new();
        assert!(editor.properties.is_empty());
    }
}
