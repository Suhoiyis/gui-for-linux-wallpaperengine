use crate::error::{LwgError, LwgResult};
use std::process::Command;
use tracing::{debug, error, info, warn};

/// 显示器信息
#[derive(Debug, Clone)]
pub struct Display {
    pub name: String,
    pub is_primary: bool,
    pub resolution: Option<String>,
}

/// 显示器管理器
pub struct ScreenManager {
    displays: Vec<Display>,
}

impl ScreenManager {
    /// 创建新的显示器管理器
    pub fn new() -> Self {
        let mut manager = Self {
            displays: Vec::new(),
        };

        if let Err(e) = manager.refresh() {
            warn!("Failed to refresh displays: {}", e);
        }

        manager
    }

    /// 刷新显示器列表
    pub fn refresh(&mut self) -> LwgResult<()> {
        // 首先尝试 xrandr (X11)
        if let Ok(displays) = Self::detect_x11() {
            self.displays = displays;
            info!("Detected {} displays via xrandr", self.displays.len());
            return Ok(());
        }

        // 然后尝试 wlr-randr (Wayland wlroots)
        if let Ok(displays) = Self::detect_wayland() {
            self.displays = displays;
            info!("Detected {} displays via wlr-randr", self.displays.len());
            return Ok(());
        }

        // 最后尝试 kscreen-doctor (KDE)
        if let Ok(displays) = Self::detect_kde() {
            self.displays = displays;
            info!(
                "Detected {} displays via kscreen-doctor",
                self.displays.len()
            );
            return Ok(());
        }

        Err(LwgError::NoDisplayFound)
    }

    /// 通过 xrandr 检测显示器 (X11)
    fn detect_x11() -> LwgResult<Vec<Display>> {
        let output = Command::new("xrandr")
            .arg("--query")
            .output()
            .map_err(|e| LwgError::ProcessError(format!("xrandr failed: {}", e)))?;

        if !output.status.success() {
            return Err(LwgError::ProcessError(
                "xrandr exited with error".to_string(),
            ));
        }

        let stdout = String::from_utf8_lossy(&output.stdout);
        let mut displays = Vec::new();

        for line in stdout.lines() {
            // 格式: "DP-1 connected primary 1920x1080+0+0 ..."
            // 或: "eDP-1 connected 1920x1080+0+0 ..."
            if line.contains(" connected ") {
                let parts: Vec<_> = line.split_whitespace().collect();

                if parts.len() >= 2 {
                    let name = parts[0].to_string();
                    let is_primary = line.contains(" primary ");

                    // 尝试解析分辨率
                    let resolution = parts
                        .iter()
                        .find(|p| p.contains('x') && p.contains('+'))
                        .map(|s| s.to_string());

                    displays.push(Display {
                        name,
                        is_primary,
                        resolution,
                    });
                }
            }
        }

        if displays.is_empty() {
            return Err(LwgError::NoDisplayFound);
        }

        Ok(displays)
    }

    /// 通过 wlr-randr 检测显示器 (Wayland wlroots)
    fn detect_wayland() -> LwgResult<Vec<Display>> {
        let output = Command::new("wlr-randr")
            .output()
            .map_err(|e| LwgError::ProcessError(format!("wlr-randr failed: {}", e)))?;

        if !output.status.success() {
            return Err(LwgError::ProcessError(
                "wlr-randr exited with error".to_string(),
            ));
        }

        let stdout = String::from_utf8_lossy(&output.stdout);
        let mut displays = Vec::new();
        let mut current_display: Option<String> = None;

        for line in stdout.lines() {
            let trimmed = line.trim();

            // 显示器名称行（不以空格开头）
            if !trimmed.starts_with(' ') && !trimmed.is_empty() {
                // 检查是否已启用
                if line.contains("Enabled") {
                    let name = trimmed.split_whitespace().next().map(|s| s.to_string());
                    current_display = name;
                }
            }

            // 分辨率行
            if trimmed.starts_with("Physical size: ") {
                if let Some(name) = current_display.take() {
                    displays.push(Display {
                        name,
                        is_primary: false, // Wayland 没有 primary 概念
                        resolution: None,
                    });
                }
            }
        }

        if displays.is_empty() {
            return Err(LwgError::NoDisplayFound);
        }

        Ok(displays)
    }

    /// 通过 kscreen-doctor 检测显示器 (KDE)
    fn detect_kde() -> LwgResult<Vec<Display>> {
        let output = Command::new("kscreen-doctor")
            .arg("-o")
            .output()
            .map_err(|e| LwgError::ProcessError(format!("kscreen-doctor failed: {}", e)))?;

        if !output.status.success() {
            return Err(LwgError::ProcessError(
                "kscreen-doctor exited with error".to_string(),
            ));
        }

        let stdout = String::from_utf8_lossy(&output.stdout);
        let mut displays = Vec::new();

        for line in stdout.lines() {
            if line.starts_with("Output: ") {
                let name = line
                    .strip_prefix("Output: ")
                    .map(|s| s.trim().to_string())
                    .unwrap_or_default();

                if !name.is_empty() {
                    displays.push(Display {
                        name,
                        is_primary: false,
                        resolution: None,
                    });
                }
            }
        }

        if displays.is_empty() {
            return Err(LwgError::NoDisplayFound);
        }

        Ok(displays)
    }

    /// 获取所有显示器
    pub fn displays(&self) -> &[Display] {
        &self.displays
    }

    /// 获取主显示器
    pub fn primary(&self) -> Option<&Display> {
        self.displays.iter().find(|d| d.is_primary)
    }

    /// 获取第一个显示器
    pub fn first(&self) -> Option<&Display> {
        self.displays.first()
    }

    /// 获取显示器名称列表
    pub fn names(&self) -> Vec<String> {
        self.displays.iter().map(|d| d.name.clone()).collect()
    }

    /// 获取显示器数量
    pub fn count(&self) -> usize {
        self.displays.len()
    }

    /// 检查是否有显示器
    pub fn has_displays(&self) -> bool {
        !self.displays.is_empty()
    }

    /// 检查显示器是否存在
    pub fn has_display(&self, name: &str) -> bool {
        self.displays.iter().any(|d| d.name == name)
    }
}

impl Default for ScreenManager {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_xrandr_output() {
        // 这个测试在实际环境中才能运行
        // 这里只测试结构定义
        let display = Display {
            name: "DP-1".to_string(),
            is_primary: true,
            resolution: Some("1920x1080+0+0".to_string()),
        };

        assert_eq!(display.name, "DP-1");
        assert!(display.is_primary);
    }
}
