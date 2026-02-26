//! Linux Wallpaper Engine GUI - 主应用窗口
//! 已集成 NavBar - SettingsPage 待修复后集成

use gtk4::prelude::*;
use relm4::prelude::*;
use libadwaita as adw;

use crate::navbar::{NavBar, NavBarOutput};

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum AppPage {
    Wallpapers,
    Settings,
    Performance,
}

impl AppPage {
    fn name(&self) -> &'static str {
        match self {
            AppPage::Wallpapers => "wallpapers",
            AppPage::Settings => "settings",
            AppPage::Performance => "performance",
        }
    }
}

pub struct App {
    current_page: AppPage,
    navbar: Controller<NavBar>,
}

#[derive(Debug)]
pub enum AppMsg {
    NavigateTo(AppPage),
    NavBarMessage(NavBarOutput),
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

                #[name = "nav_container"]
                gtk4::Box {
                    set_orientation: gtk4::Orientation::Vertical,
                },

                gtk4::Box {
                    set_orientation: gtk4::Orientation::Horizontal,
                    set_spacing: 6,
                    set_margin_all: 6,

                    gtk4::Button {
                        set_label: "壁纸",
                        connect_clicked => AppMsg::NavigateTo(AppPage::Wallpapers),
                    },
                    gtk4::Button {
                        set_label: "设置",
                        connect_clicked => AppMsg::NavigateTo(AppPage::Settings),
                    },
                    gtk4::Button {
                        set_label: "性能",
                        connect_clicked => AppMsg::NavigateTo(AppPage::Performance),
                    },
                },

                #[name = "main_stack"]
                gtk4::Stack {
                    set_hexpand: true,
                    set_vexpand: true,
                    set_transition_type: gtk4::StackTransitionType::Crossfade,
                },
            },
        }
    }

    fn init(
        _init: Self::Init,
        _root: Self::Root,
        sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        let navbar = NavBar::builder()
            .launch(())
            .forward(sender.input_sender(), |output| AppMsg::NavBarMessage(output));

        let model = Self {
            current_page: AppPage::Wallpapers,
            navbar,
        };

        let widgets = view_output!();

        widgets.nav_container.append(model.navbar.widget());

        // 使用 Label 占位符（SettingsPage 待修复后替换）
        let placeholder_wp = gtk4::Label::new(Some("壁纸页面（待接入）"));
        let placeholder_st = gtk4::Label::new(Some("设置页面（SettingsPage 待修复）"));
        let placeholder_pf = gtk4::Label::new(Some("性能页面（待接入）"));

        widgets.main_stack.add_named(&placeholder_wp, Some("wallpapers"));
        widgets.main_stack.add_named(&placeholder_st, Some("settings"));
        widgets.main_stack.add_named(&placeholder_pf, Some("performance"));

        widgets.main_stack.set_visible_child(&placeholder_wp);

        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, _sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            AppMsg::NavigateTo(page) => {
                self.current_page = page;
            }
            AppMsg::NavBarMessage(nav_output) => {
                match nav_output {
                    NavBarOutput::CompactModeToggled(enabled) => {
                        eprintln!("紧凑模式：{}", enabled);
                    }
                    NavBarOutput::HistoryRequested => {
                        eprintln!("请求历史记录");
                    }
                    NavBarOutput::AboutRequested => {
                        eprintln!("请求关于");
                    }
                    NavBarOutput::ScreenChanged(screen) => {
                        eprintln!("屏幕切换：{}", screen);
                    }
                }
            }
        }
    }
}
