use gtk4::prelude::*;
use lwg_ui::App;
use relm4::prelude::*;
use std::include_str;

fn main() {
    // 创建应用
    let app = RelmApp::new("com.wallpaperengine.gui");

    // 加载 CSS 样式
    app.connect_activate(|_| {
        let provider = gtk4::CssProvider::new();
        provider.load_from_data(include_str!("../resources/style.css"));

        // 应用到默认显示
        if let Some(display) = gtk4::gdk::Display::default() {
            gtk4::style_context_add_provider_for_display(
                &display,
                &provider,
                gtk4::STYLE_PROVIDER_PRIORITY_APPLICATION,
            );
        }
    });

    app.run::<App>(());
}
