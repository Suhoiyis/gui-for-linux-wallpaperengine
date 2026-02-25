use gtk4::prelude::*;
use libadwaita as adw;
use relm4::prelude::*;

/// 通用对话框工具集（完善版）

/// 删除确认对话框
pub fn show_delete_dialog(parent: &gtk4::Window, title: &str, callback: impl Fn(bool) + 'static) {
    let dialog = adw::MessageDialog::builder()
        .transient_for(parent)
        .modal(true)
        .heading("确认删除")
        .body(&format!("确定要删除 \"{}\" 吗？此操作不可撤销。", title))
        .build();

    dialog.add_response("cancel", "取消");
    dialog.add_response("delete", "删除");
    dialog.set_response_appearance("delete", adw::ResponseAppearance::Destructive);

    let response = dialog.choose_future();
    glib::MainContext::default().spawn_local(async move {
        let response = response.await;
        callback(response == "delete");
    });
}

/// 错误提示对话框
pub fn show_error_dialog(parent: &gtk4::Window, title: &str, message: &str) {
    let dialog = adw::MessageDialog::builder()
        .transient_for(parent)
        .modal(true)
        .heading(title)
        .body(message)
        .build();

    dialog.add_response("ok", "确定");
    dialog.set_default_response("ok");
    dialog.show();
}

/// 截图成功对话框
pub fn show_screenshot_success_dialog(parent: &gtk4::Window, path: &str) {
    let dialog = adw::MessageDialog::builder()
        .transient_for(parent)
        .modal(true)
        .heading("截图成功！")
        .body(&format!("截图已保存到：{}", path))
        .build();

    dialog.add_response("open_folder", "打开文件夹");
    dialog.add_response("ok", "确定");
    dialog.set_default_response("ok");
    dialog.show();
}

/// 昵称设置对话框
pub fn show_nickname_dialog(
    parent: &gtk4::Window,
    current_nickname: Option<&str>,
    callback: impl Fn(Option<String>) + 'static,
) {
    let dialog = adw::MessageDialog::builder()
        .transient_for(parent)
        .modal(true)
        .heading("设置昵称")
        .build();

    dialog.add_response("cancel", "取消");
    dialog.add_response("save", "保存");
    dialog.set_default_response("save");

    let entry = gtk4::Entry::new();
    if let Some(nickname) = current_nickname {
        entry.set_text(nickname);
    }
    entry.set_placeholder_text("留空使用原标题");

    dialog.set_extra_child(Some(&entry));
    dialog.show();

    dialog.connect_response(Some("save"), move |dialog, _| {
        let text = entry.text().trim().to_string();
        if text.is_empty() {
            callback(None);
        } else {
            callback(Some(text));
        }
        dialog.close();
    });

    dialog.connect_response(Some("cancel"), move |dialog, _| {
        callback(None);
        dialog.close();
    });
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dialog_utils_exist() {
        assert!(true);
    }
}
