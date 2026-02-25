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
            set_title: Some("Linux Wallpaper Engine"),

            gtk4::Box {
                set_orientation: gtk4::Orientation::Vertical,
                set_spacing: 20,
                set_margin_all: 20,

                gtk4::Label {
                    set_label: "🎉 Phase 1 完成！",
                },

                gtk4::Button {
                    set_label: "点击我",
                    connect_clicked => AppMsg::Increment,
                },

                gtk4::Label {
                    #[watch]
                    set_label: &format!("次数：{}", model.counter),
                },
            },
        }
    }

    fn init(init: Self::Init, root: Self::Root, sender: ComponentSender<Self>) -> ComponentParts<Self> {
        let model = Self { counter: init };
        let widgets = view_output!();
        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, _sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            AppMsg::Increment => self.counter += 1,
        }
    }
}
