use crate::error::{LwgError, LwgResult};
use crate::config::ConfigManager;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::process::Command;
use tracing::{debug, error, info, warn};

/// 属性类型
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum PropertyType {
    Slider,
    Color,
    Boolean,
    Options,
}

/// 属性选项
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PropertyOption {
    pub label: String,
    pub value: String,
}

/// 壁纸属性
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WallpaperProperty {
    pub name: String,
    pub prop_type: PropertyType,
    pub text: String,
    pub value: Option<serde_json::Value>,
    pub min: f64,
    pub max: f64,
    pub step: f64,
    pub options: Vec<PropertyOption>,
}

/// PropertiesManager
pub struct PropertiesManager {
    config: ConfigManager,
    properties_cache: HashMap<String, Vec<WallpaperProperty>>,
    user_properties: HashMap<String, HashMap<String, serde_json::Value>>,
}

impl PropertiesManager {
    /// 创建新的 PropertiesManager
    pub fn new(config: ConfigManager) -> Self {
        let mut manager = Self {
            config,
            properties_cache: HashMap::new(),
            user_properties: HashMap::new(),
        };
        manager.load_from_config();
        manager
    }

    /// 从配置加载用户属性
    fn load_from_config(&mut self) {
        if let Some(props) = self.config.get("wallpaperProperties") {
            if let Ok(map) = serde_json::from_value::<HashMap<String, HashMap<String, serde_json::Value>>>(props) {
                self.user_properties = map;
                debug!("Loaded user properties for {} wallpapers", self.user_properties.len());
            }
        }
    }

    /// 获取壁纸属性列表
    pub fn get_properties(&mut self, wp_id: &str) -> LwgResult<Vec<WallpaperProperty>> {
        // 检查缓存
        if let Some(props) = self.properties_cache.get(wp_id) {
            debug!("Cache hit for wallpaper {}", wp_id);
            return Ok(props.clone());
        }

        // 调用后端获取属性
        info!("Fetching properties for wallpaper {}", wp_id);
        let output = Command::new("linux-wallpaperengine")
            .args(["--list-properties", wp_id])
            .output();

        match output {
            Ok(result) => {
                if result.status.success() {
                    let stdout = String::from_utf8_lossy(&result.stdout);
                    let properties = self.parse_properties_output(&stdout)?;
                    self.properties_cache.insert(wp_id.to_string(), properties.clone());
                    info!("Parsed {} properties for wallpaper {}", properties.len(), wp_id);
                    Ok(properties)
                } else {
                    let stderr = String::from_utf8_lossy(&result.stderr);
                    error!("Failed to get properties: {}", stderr);
                    Err(LwgError::ProcessError(format!("Failed to get properties: {}", stderr)))
                }
            }
            Err(e) => {
                error!("Failed to execute command: {}", e);
                Err(LwgError::ProcessError(format!("Failed to execute command: {}", e)))
            }
        }
    }

    /// 解析属性输出
    pub fn parse_properties_output(&self, output: &str) -> LwgResult<Vec<WallpaperProperty>> {
        let mut properties = Vec::new();
        let mut lines = output.lines();
        
        while let Some(line) = lines.next() {
            let line = line.trim();
            if line.is_empty() || line.contains("Running with:") {
                continue;
            }

            if line.contains(" - ") {
                let parts: Vec<&str> = line.splitn(2, " - ").collect();
                if parts.len() == 2 {
                    let name = parts[0].trim().to_string();
                    let prop_type_str = parts[1].trim();
                    
                    let prop_type = match prop_type_str.to_lowercase().as_str() {
                        "slider" => PropertyType::Slider,
                        "color" => PropertyType::Color,
                        "boolean" => PropertyType::Boolean,
                        "options" => PropertyType::Options,
                        _ => PropertyType::Slider,
                    };

                    let mut prop = WallpaperProperty {
                        name: name.clone(),
                        prop_type,
                        text: String::new(),
                        value: None,
                        min: 0.0,
                        max: 100.0,
                        step: 1.0,
                        options: Vec::new(),
                    };

                    // 解析后续行
                    while let Some(subline) = lines.next() {
                        let subline = subline.trim();
                        if subline.is_empty() {
                            continue;
                        }
                        if subline.contains(" - ") {
                            break;
                        }

                        if subline.starts_with("Text:") {
                            prop.text = subline[5..].trim().to_string();
                        } else if subline.starts_with("Value:") {
                            let value_str = subline[6..].trim();
                            prop.value = Some(self.parse_value(value_str, &prop_type));
                        } else if subline.starts_with("Min:") {
                            prop.min = subline[4..].trim().parse().unwrap_or(0.0);
                        } else if subline.starts_with("Max:") {
                            prop.max = subline[4..].trim().parse().unwrap_or(100.0);
                        } else if subline.starts_with("Step:") {
                            prop.step = subline[5..].trim().parse().unwrap_or(1.0);
                        } else if subline.starts_with("Values:") {
                            while let Some(opt_line) = lines.next() {
                                let opt_line = opt_line.trim();
                                if !opt_line.contains('\t') {
                                    break;
                                }
                                if let Some(eq_pos) = opt_line.find('=') {
                                    let label = opt_line[..eq_pos].trim().to_string();
                                    let value = opt_line[eq_pos + 1..].trim().to_string();
                                    prop.options.push(PropertyOption { label, value });
                                }
                            }
                        }
                    }

                    properties.push(prop);
                }
            }
        }

        Ok(properties)
    }

    /// 解析属性值
    fn parse_value(&self, value_str: &str, prop_type: &PropertyType) -> serde_json::Value {
        match prop_type {
            PropertyType::Color => {
                let parts: Vec<&str> = value_str.split(',').collect();
                if parts.len() == 3 {
                    let r: f64 = parts[0].trim().parse().unwrap_or(0.0);
                    let g: f64 = parts[1].trim().parse().unwrap_or(0.0);
                    let b: f64 = parts[2].trim().parse().unwrap_or(0.0);
                    serde_json::json!([r, g, b])
                } else {
                    serde_json::json!(value_str)
                }
            }
            PropertyType::Boolean => {
                serde_json::json!(value_str == "1")
            }
            _ => {
                if let Ok(num) = value_str.parse::<f64>() {
                    if num == num.floor() {
                        serde_json::json!(num as i64)
                    } else {
                        serde_json::json!(num)
                    }
                } else {
                    serde_json::json!(value_str)
                }
            }
        }
    }

    /// 获取用户属性值
    pub fn get_user_property(&self, wp_id: &str, prop_name: &str) -> Option<&serde_json::Value> {
        self.user_properties
            .get(wp_id)
            .and_then(|props| props.get(prop_name))
    }

    /// 设置用户属性值
    pub fn set_user_property(&mut self, wp_id: &str, prop_name: &str, value: serde_json::Value) -> LwgResult<()> {
        self.user_properties
            .entry(wp_id.to_string())
            .or_insert_with(HashMap::new)
            .insert(prop_name.to_string(), value);

        let json_value = serde_json::to_value(&self.user_properties)?;
        self.config.set("wallpaperProperties", json_value)?;
        
        debug!("Set property {} for wallpaper {}", prop_name, wp_id);
        Ok(())
    }

    /// 清除壁纸属性缓存
    pub fn clear_cache(&mut self, wp_id: Option<&str>) {
        if let Some(id) = wp_id {
            self.properties_cache.remove(id);
            debug!("Cleared cache for wallpaper {}", id);
        } else {
            self.properties_cache.clear();
            debug!("Cleared all property caches");
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_value_color() {
        let manager = PropertiesManager::new(ConfigManager::new().unwrap());
        let value = manager.parse_value("1.0,0.5,0.0", &PropertyType::Color);
        assert_eq!(value, serde_json::json!([1.0, 0.5, 0.0]));
    }

    #[test]
    fn test_parse_value_boolean() {
        let manager = PropertiesManager::new(ConfigManager::new().unwrap());
        let value = manager.parse_value("1", &PropertyType::Boolean);
        assert_eq!(value, serde_json::json!(true));
    }

    #[test]
    fn test_parse_value_number() {
        let manager = PropertiesManager::new(ConfigManager::new().unwrap());
        let value = manager.parse_value("50", &PropertyType::Slider);
        assert_eq!(value, serde_json::json!(50));
    }
}

#[cfg(test)]
mod tests_properties_extended {
    use super::*;

    #[test]
    fn test_properties_manager_creation() {
        let config = ConfigManager::new().unwrap();
        let manager = PropertiesManager::new(config);
        assert!(manager.get_properties("test").is_ok());
    }

    #[test]
    fn test_user_property_persistence() {
        let mut config = ConfigManager::new().unwrap();
        let mut manager = PropertiesManager::new(config);
        manager.set_user_property("123", "brightness", serde_json::json!(0.8)).unwrap();
        let value = manager.get_user_property("123", "brightness");
        assert_eq!(value, Some(&serde_json::json!(0.8)));
    }
}
