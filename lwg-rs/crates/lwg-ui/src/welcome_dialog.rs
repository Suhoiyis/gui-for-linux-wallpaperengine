use gtk4::prelude::*;
use std::path::Path;

/// 欢迎向导配置
#[derive(Debug, Clone)]
pub struct WelcomeDialogConfig {
    pub workshop_path: Option<String>,
    pub auto_start: bool,
    pub onboarding_completed: bool,
}

impl Default for WelcomeDialogConfig {
    fn default() -> Self {
        Self {
            workshop_path: None,
            auto_start: false,
            onboarding_completed: false,
        }
    }
}

impl WelcomeDialogConfig {
    /// 检测是否需要显示欢迎向导
    pub fn should_show(config_path: &Path) -> bool {
        !config_path.exists()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_welcome_dialog_config() {
        let config = WelcomeDialogConfig::default();
        assert!(!config.onboarding_completed);
    }
}
