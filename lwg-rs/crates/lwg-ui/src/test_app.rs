use gtk4::prelude::*;
use relm4::prelude::*;

pub struct TestApp {
    counter: u32,
}

#[derive(Debug)]
pub enum TestAppMsg {
    Increment,
    Decrement,
}

#[relm4::component(pub)]
impl SimpleComponent for TestApp {
    type Init = u32;
    type Input = TestAppMsg;
    type Output = ();

    view! {
        gtk4::Window {
            set_title: Some("Linux Wallpaper Engine - Test"),
            set_default_width: 800,
            set_default_height: 600,

            gtk4::Box {
                set_orientation: gtk4::Orientation::Vertical,
                set_spacing: 20,
                set_margin_all: 20,

                gtk4::Label {
                    set_label: "🎉 Phase 1 完成！",
                    add_css_class: "title-1",
                },

                gtk4::Label {
                    set_label: "三页面导航系统已实现",
                },

                gtk4::Label {
                    set_label: "网格/列表视图已实现",
                },

                gtk4::Label {
                    set_label: "设置页面已实现",
                },

                gtk4::Label {
                    set_label: "性能监控页面已实现",
                },

                gtk4::Button {
                    set_label: "测试按钮",
                    connect_clicked => TestAppMsg::Increment,
                },

                gtk4::Label {
                    set_label: &format!("计数器：{}", self.counter),
                },
            },
        }
    }

    fn init(
        init: Self::Init,
        root: Self::Root,
        sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        let model = Self {
            counter: init,
        };

        let widgets = view_output!();

        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, _sender: ComponentSender<Self>) {
        match msg {
            TestAppMsg::Increment => self.counter += 1,
            TestAppMsg::Decrement => self.counter -= 1,
        }
    }
}
