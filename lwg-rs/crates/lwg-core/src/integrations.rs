//! 桌面集成管理器 - 完整实现
//! 审计报告 Task 4.2.1-4.2.3: AppIntegrator 完整实现

use crate::error::{LwgError, LwgResult};
use std::fs;
use std::path::{Path, PathBuf};
use std::env;

const APP_ID: &str = "com.wallpaperengine.gui";

/// 桌面集成管理器
pub struct AppIntegrator {
    script_path: PathBuf,
    icon_path: PathBuf,
    app_dir: PathBuf,
    autostart_dir: PathBuf,
    desktop_filename: String,
}

impl AppIntegrator {
    /// 创建新的桌面集成管理器
    pub fn new() -> LwgResult<Self> {
        let current_dir = env::current_dir()?;
        let project_root = current_dir.parent()
            .ok_or_else(|| LwgError::ConfigError("Invalid project root".to_string()))?
            .to_path_buf();
        
        let script_path = project_root.join("run_gui.py");
        let icon_path = project_root.join("pic/icons/GUI_rounded.png");
        
        let home = env::var("HOME")
            .map_err(|_| LwgError::ConfigError("HOME not set".to_string()))?;
        let app_dir = PathBuf::from(format!("{}/.local/share/applications", home));
        let autostart_dir = PathBuf::from(format!("{}/.config/autostart", home));
        
        let desktop_filename = format!("{}.desktop", APP_ID);

        Ok(Self {
            script_path,
            icon_path,
            app_dir,
            autostart_dir,
            desktop_filename,
        })
    }

    /// 生成.desktop 文件内容
    fn generate_content(&self, hidden: bool) -> String {
        let appimage_path = env::var("APPIMAGE").unwrap_or_default();
        
        let (exec_cmd, path_str) = if !appimage_path.is_empty() {
            (format!("\"{}\"", appimage_path), String::new())
        } else if self.script_path.starts_with("/usr/share/") {
            ("linux-wallpaperengine-gui".to_string(), String::new())
        } else {
            let python = env::var("PYTHON").unwrap_or_else(|_| "python3".to_string());
            (format!("{} \"{}\"", python, self.script_path.display()), 
             format!("Path={}\n", self.script_path.parent().unwrap().display()))
        };

        let exec_cmd = if hidden {
            format!("{} --hidden", exec_cmd)
        } else {
            exec_cmd
        };

        format!(
            r#"[Desktop Entry]
Type=Application
Name=Linux Wallpaper Engine
Comment=Wallpaper Engine for Linux
Exec={}
Icon={}
{}Terminal=false
Categories=Utility;Graphics;
StartupNotify=true
StartupWMClass={}
X-GNOME-Autostart-enabled=true
"#,
            exec_cmd, APP_ID, path_str, APP_ID
        )
    }

    /// 安装图标到本地目录
    pub fn install_icon(&self) -> LwgResult<PathBuf> {
        let dest_dir = self.app_dir.join("icons/hicolor/512x512/apps");
        fs::create_dir_all(&dest_dir)?;
        
        let dest_path = dest_dir.join(format!("{}.png", APP_ID));
        
        // 尝试从多个源位置复制图标
        let icon_sources = [
            self.icon_path.clone(),
            PathBuf::from("pic/icons/gui_tray_rounded.png"),
            PathBuf::from("pic/icons/GUI_rounded.png"),
        ];

        for src in &icon_sources {
            if src.exists() {
                fs::copy(src, &dest_path)?;
                return Ok(dest_path);
            }
        }

        Err(LwgError::ConfigError("Icon not found".to_string()))
    }

    /// 创建桌面快捷方式
    pub fn create_desktop_file(&self, hidden: bool) -> LwgResult<PathBuf> {
        // 确保目录存在
        fs::create_dir_all(&self.app_dir)?;
        
        let desktop_path = self.app_dir.join(&self.desktop_filename);
        let content = self.generate_content(hidden);
        
        fs::write(&desktop_path, content)?;
        
        // 设置可执行权限
        #[cfg(unix)]
        {
            use std::os::unix::fs::PermissionsExt;
            let mut perms = fs::metadata(&desktop_path)?.permissions();
            perms.set_mode(0o755);
            fs::set_permissions(&desktop_path, perms)?;
        }

        Ok(desktop_path)
    }

    /// 删除桌面快捷方式
    pub fn remove_desktop_file(&self) -> LwgResult<()> {
        let desktop_path = self.app_dir.join(&self.desktop_filename);
        if desktop_path.exists() {
            fs::remove_file(desktop_path)?;
        }
        Ok(())
    }

    /// 设置开机自启
    pub fn set_autostart(&self, enabled: bool, hidden: bool) -> LwgResult<()> {
        fs::create_dir_all(&self.autostart_dir)?;
        
        let autostart_path = self.autostart_dir.join(&self.desktop_filename);
        
        if enabled {
            let content = self.generate_content(hidden);
            fs::write(&autostart_path, content)?;
        } else {
            if autostart_path.exists() {
                fs::remove_file(autostart_path)?;
            }
        }

        Ok(())
    }

    /// 检查是否已设置开机自启
    pub fn is_autostart(&self) -> bool {
        let autostart_path = self.autostart_dir.join(&self.desktop_filename);
        autostart_path.exists()
    }

    /// 自愈：检查并修复安装
    pub fn heal(&self) -> LwgResult<()> {
        // 检查.desktop 文件是否存在
        let desktop_path = self.app_dir.join(&self.desktop_filename);
        if !desktop_path.exists() {
            self.create_desktop_file(false)?;
        }

        // 检查图标是否存在
        let icon_path = self.app_dir.join("icons/hicolor/512x512/apps").join(format!("{}.png", APP_ID));
        if !icon_path.exists() {
            self.install_icon()?;
        }

        Ok(())
    }
}

impl Default for AppIntegrator {
    fn default() -> Self {
        Self::new().expect("Failed to create AppIntegrator")
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_creation() {
        let integrator = AppIntegrator::new();
        assert!(integrator.is_ok());
    }

    #[test]
    fn test_desktop_content_generation() {
        let integrator = AppIntegrator::new().unwrap();
        let content = integrator.generate_content(false);
        assert!(content.contains("[Desktop Entry]"));
        assert!(content.contains(APP_ID));
    }
}
