use gtk4::prelude::*;
use relm4::prelude::*;

/// 通用对话框工具集（简化版）

/// 删除确认对话框（简化）
pub fn show_delete_dialog_simple(title: &str) -> String {
    format!("确认删除：{}", title)
}

/// 错误提示对话框（简化）
pub fn show_error_dialog_simple(message: &str) -> String {
    format!("错误：{}", message)
}

/// 截图成功对话框（简化）
pub fn show_screenshot_success_dialog_simple(path: &str) -> String {
    format!("截图已保存：{}", path)
}

/// 昵称设置对话框（简化）
pub fn show_nickname_dialog_simple(current: Option<&str>) -> Option<String> {
    current.map(String::from)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dialog_utils() {
        assert_eq!(show_delete_dialog_simple("Test"), "确认删除：Test");
    }
}
