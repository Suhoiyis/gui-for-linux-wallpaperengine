use gtk4::prelude::*;

/// 通用对话框工具集
pub mod dialog_utils {
    use super::*;
    
    /// 显示删除确认对话框（简化版）
    pub fn show_delete_dialog_simple(title: &str) -> String {
        format!("确认删除：{}", title)
    }
    
    /// 显示错误对话框（简化版）
    pub fn show_error_dialog_simple(message: &str) -> String {
        format!("错误：{}", message)
    }
}
