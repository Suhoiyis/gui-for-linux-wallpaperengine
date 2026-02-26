//! 通用对话框 - GTK4 实现

use gtk4::prelude::*;

/// 删除确认对话框
pub fn show_delete_dialog(parent: &gtk4::Window, title: &str, on_confirm: impl Fn() + 'static) {
    let dialog = gtk4::Dialog::builder()
        .transient_for(parent)
        .modal(true)
        .title("确认删除")
        .build();

    let content = dialog.content_area();
    content.set_margin_start(12);
    content.set_margin_end(12);
    content.set_margin_top(12);
    content.set_margin_bottom(12);

    let label = gtk4::Label::new(Some(&format!("确定要删除 \"{}\" 吗？", title)));
    label.set_wrap(true);
    content.append(&label);

    dialog.add_button("取消", gtk4::ResponseType::Cancel);
    dialog.add_button("删除", gtk4::ResponseType::Accept);

    dialog.connect_response(move |dialog, response| {
        if response == gtk4::ResponseType::Accept {
            on_confirm();
        }
        dialog.close();
    });

    dialog.show();
}

/// 错误提示对话框
pub fn show_error_dialog(parent: &gtk4::Window, title: &str, message: &str) {
    let dialog = gtk4::Dialog::builder()
        .transient_for(parent)
        .modal(true)
        .title(title)
        .build();

    let content = dialog.content_area();
    content.set_margin_start(12);
    content.set_margin_end(12);
    content.set_margin_top(12);
    content.set_margin_bottom(12);

    let label = gtk4::Label::new(Some(message));
    label.set_wrap(true);
    content.append(&label);

    dialog.add_button("确定", gtk4::ResponseType::Ok);

    dialog.connect_response(|dialog, _| {
        dialog.close();
    });

    dialog.show();
}

/// 截图成功对话框
pub fn show_screenshot_success_dialog(
    parent: &gtk4::Window,
    path: &str,
    on_open_folder: impl Fn() + 'static,
) {
    let dialog = gtk4::Dialog::builder()
        .transient_for(parent)
        .modal(true)
        .title("截图成功")
        .build();

    let content = dialog.content_area();
    content.set_margin_start(12);
    content.set_margin_end(12);
    content.set_margin_top(12);
    content.set_margin_bottom(12);

    let label = gtk4::Label::new(Some(&format!("截图已保存到：{}", path)));
    label.set_wrap(true);
    content.append(&label);

    dialog.add_button("打开文件夹", gtk4::ResponseType::Accept);
    dialog.add_button("确定", gtk4::ResponseType::Ok);

    dialog.connect_response(move |dialog, response| {
        if response == gtk4::ResponseType::Accept {
            on_open_folder();
        }
        dialog.close();
    });

    dialog.show();
}

/// 昵称设置对话框
pub fn show_nickname_dialog(
    parent: &gtk4::Window,
    current_nickname: Option<&str>,
    on_save: impl Fn(Option<String>) + 'static,
) {
    let dialog = gtk4::Dialog::builder()
        .transient_for(parent)
        .modal(true)
        .title("设置昵称")
        .build();

    let content = dialog.content_area();
    content.set_margin_start(12);
    content.set_margin_end(12);
    content.set_margin_top(12);
    content.set_margin_bottom(12);

    let entry = gtk4::Entry::new();
    entry.set_placeholder_text(Some("留空使用原标题"));
    if let Some(nickname) = current_nickname {
        entry.set_text(nickname);
    }
    content.append(&entry);

    dialog.add_button("取消", gtk4::ResponseType::Cancel);
    dialog.add_button("保存", gtk4::ResponseType::Ok);

    let entry_clone = entry.clone();
    dialog.connect_response(move |dialog, response| {
        if response == gtk4::ResponseType::Ok {
            let text = entry_clone.text().trim().to_string();
            if text.is_empty() {
                on_save(None);
            } else {
                on_save(Some(text));
            }
        } else {
            on_save(None);
        }
        dialog.close();
    });

    dialog.show();
}
