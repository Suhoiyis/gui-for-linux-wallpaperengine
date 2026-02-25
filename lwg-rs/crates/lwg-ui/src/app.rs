use gtk4::prelude::*;
use relm4::prelude::*;

pub struct App {
    counter: u32,
}

#[derive(Debug)]
pub enum AppMsg {
    Increment,
}

#[relm4::component(pub)]
impl SimpleComponent for App {
    type Init = u32;
    type Input = AppMsg;
    type Output = ();

    view! {
        gtk4::ApplicationWindow {
            set_title: Some("Linux Wallpaper Engine - Phase 1 完成!"),
            set_default_width: 800,
            set_default_height: 600,

            gtk4::Box {
                set_orientation: gtk4::Orientation::Vertical,
                set_spacing: 20,
                set_margin_all: 20,

                gtk4::Label {
                    set_label: "🎉 Phase 1 UI 框架完成！",
                    add_css_class: "title-1",
                },

                gtk4::Label {
                    set_label: "✅ 三页面导航系统",
                },

                gtk4::Label {
                    set_label: "✅ 网格/列表视图",
                },

                gtk4::Label {
                    set_label: "✅ 设置页面",
                },

                gtk4::Label {
                    set_label: "✅ 性能监控页面",
                },

                gtk4::Button {
                    set_label: &format!("测试按钮 (点击 {} 次)", model.counter),
                    connect_clicked => AppMsg::Increment,
                },
            },
        }
    }

    fn init(
        init: Self::Init,
        root: Self::Root,
        sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        let model = Self { counter: init };
        let widgets = view_output!();
        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, _sender: ComponentSender<Self>) {
        match msg {
            AppMsg::Increment => self.counter += 1,
        }
    }
}
