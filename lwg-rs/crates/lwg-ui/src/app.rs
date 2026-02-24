use gtk4::prelude::*;
use relm4::prelude::*;

pub struct App {
    window: gtk::ApplicationWindow,
}

#[derive(Debug)]
pub enum AppMsg {
    Quit,
}

#[relm4::component(pub)]
impl SimpleComponent for App {
    type Init = ();
    type Input = AppMsg;
    type Output = ();

    view! {
        gtk::ApplicationWindow {
            set_title: Some("Linux Wallpaper Engine GUI"),
            set_default_width: 800,
            set_default_height: 600,

            gtk::Box {
                set_orientation: gtk::Orientation::Vertical,
                set_spacing: 10,
                set_margin_all: 10,

                gtk::Label {
                    set_label: "Rust version of Linux Wallpaper Engine GUI",
                },

                gtk::Label {
                    set_label: "Coming soon...",
                }
            }
        }
    }

    fn init(
        _init: Self::Init,
        root: Self::Root,
        _sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        let model = App {
            window: root.clone(),
        };
        let widgets = view_output!();
        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, _sender: ComponentSender<Self>) {
        match msg {
            AppMsg::Quit => {
                self.window.close();
            }
        }
    }
}
