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
impl Component for App {
    type Init = u32;
    type Input = AppMsg;
    type Output = ();
    type CommandOutput = ();

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
                    set_label: "✅ 功能列表:",
                },

                gtk4::Box {
                    set_orientation: gtk4::Orientation::Vertical,
                    set_spacing: 5,
                    set_margin_start: 20,

                    gtk4::Label {
                        set_label: "• 三页面导航系统",
                        set_halign: gtk4::Align::Start,
                    },

                    gtk4::Label {
                        set_label: "• 网格/列表视图",
                        set_halign: gtk4::Align::Start,
                    },

                    gtk4::Label {
                        set_label: "• 设置页面",
                        set_halign: gtk4::Align::Start,
                    },

                    gtk4::Label {
                        set_label: "• 性能监控页面",
                        set_halign: gtk4::Align::Start,
                    },
                },

                gtk4::Button {
                    set_label: "点击测试交互",
                    connect_clicked => AppMsg::Increment,
                },

                #[local_ref]
                counter_label -> gtk4::Label {
                    set_label: "点击次数：0",
                },
            },
        }
    }

    fn init(
        init: Self::Init,
        root: Self::Root,
        sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        let counter_label = gtk4::Label::new(Some("点击次数：0"));
        
        let model = Self { counter: init };
        let widgets = view_output!();
        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, _sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            AppMsg::Increment => {
                self.counter += 1;
                println!("点击次数：{}", self.counter);
            }
        }
    }
}
