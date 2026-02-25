//! Linux Wallpaper Engine GUI - 主应用窗口

use gtk4::prelude::*;
use relm4::prelude::*;
use libadwaita as adw;

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum AppPage {
    Wallpapers,
    Settings,
    Performance,
}

pub struct App {
    current_page: AppPage,
}

#[derive(Debug)]
pub enum AppMsg {
    NavigateTo(AppPage),
}

#[relm4::component(pub)]
impl Component for App {
    type Init = ();
    type Input = AppMsg;
    type Output = ();
    type CommandOutput = ();

    view! {
        gtk4::ApplicationWindow {
            set_title: Some("Linux Wallpaper Engine"),
            set_default_width: 1200,
            set_default_height: 800,

            gtk4::Box {
                set_orientation: gtk4::Orientation::Vertical,

                adw::HeaderBar {},

                gtk4::Box {
                    set_orientation: gtk4::Orientation::Horizontal,
                    set_spacing: 6,
                    set_margin_all: 6,

                    gtk4::Button {
                        set_label: "壁纸",
                    },

                    gtk4::Button {
                        set_label: "设置",
                    },

                    gtk4::Button {
                        set_label: "性能",
                    },
                },

                gtk4::Stack {
                    set_hexpand: true,
                    set_vexpand: true,
                },
            },
        }
    }

    fn init(
        _init: Self::Init,
        _root: Self::Root,
        _sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        let model = Self {
            current_page: AppPage::Wallpapers,
        };

        let widgets = view_output!();

        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, _sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            AppMsg::NavigateTo(_) => {}
        }
    }
}
