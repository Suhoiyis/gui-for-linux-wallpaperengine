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
        adw::ApplicationWindow {
            set_title: Some("Linux Wallpaper Engine"),
            set_default_width: 1200,
            set_default_height: 800,

            gtk4::Box {
                set_orientation: gtk4::Orientation::Vertical,

                gtk4::Box {
                    set_orientation: gtk4::Orientation::Horizontal,
                    set_spacing: 6,
                    set_margin_all: 6,

                    gtk4::Button {
                        set_label: "壁纸",
                        connect_clicked[sender] => move |_| {
                            sender.input(AppMsg::NavigateTo(AppPage::Wallpapers));
                        },
                    },

                    gtk4::Button {
                        set_label: "设置",
                        connect_clicked[sender] => move |_| {
                            sender.input(AppMsg::NavigateTo(AppPage::Settings));
                        },
                    },

                    gtk4::Button {
                        set_label: "性能",
                        connect_clicked[sender] => move |_| {
                            sender.input(AppMsg::NavigateTo(AppPage::Performance));
                        },
                    },
                },

                gtk4::Stack {
                    set_hexpand: true,
                    set_vexpand: true,
                    set_transition_type: gtk4::StackTransitionType::SlideLeftRight,
                    set_transition_duration: 300,

                    add_named: (&gtk4::Label::new(Some("壁纸页面")), "wallpapers"),
                    add_named: (&gtk4::Label::new(Some("设置页面")), "settings"),
                    add_named: (&gtk4::Label::new(Some("性能页面")), "performance"),
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

    fn update(&mut self, msg: Self::Input, _sender: ComponentSender<Self>, root: &Self::Root) {
        match msg {
            AppMsg::NavigateTo(page) => {
                self.current_page = page;
                
                let title = match page {
                    AppPage::Wallpapers => "Linux Wallpaper Engine - 壁纸",
                    AppPage::Settings => "Linux Wallpaper Engine - 设置",
                    AppPage::Performance => "Linux Wallpaper Engine - 性能",
                };
                
                if let Some(win) = root.downcast_ref::<adw::ApplicationWindow>() {
                    win.set_title(Some(title));
                }
            }
        }
    }
}
