//! Linux Wallpaper Engine GUI - 主应用窗口
//! 基于审计报告 Task 1.1 重写

use gtk4::prelude::*;
use relm4::prelude::*;
use libadwaita as adw;
use std::path::PathBuf;

/// 应用页面
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

/// 主应用
pub struct App {
    current_page: AppPage,
}

/// 应用消息
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

                // HeaderBar
                adw::HeaderBar {
                },

                // 导航按钮
                gtk4::Box {
                    set_orientation: gtk4::Orientation::Horizontal,
                    set_spacing: 6,
                    set_margin_all: 6,

                    gtk4::Button {
                        set_label: "壁纸",
                        add_css_class: if self.current_page == AppPage::Wallpapers { "suggested-action" } else { "" },
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

                // 页面 Stack
                #[name = "page_stack"]
                gtk4::Stack {
                    set_hexpand: true,
                    set_vexpand: true,
                    set_transition_type: gtk4::StackTransitionType::SlideLeftRight,
                    set_transition_duration: 300,

                    gtk4::ScrolledWindow {
                        set_child: Some(&gtk4::Label::new(Some("壁纸页面"))),
                    } => {
                        set_name: "wallpapers",
                    },

                    gtk4::ScrolledWindow {
                        set_child: Some(&gtk4::Label::new(Some("设置页面"))),
                    } => {
                        set_name: "settings",
                    },

                    gtk4::ScrolledWindow {
                        set_child: Some(&gtk4::Label::new(Some("性能页面"))),
                    } => {
                        set_name: "performance",
                    },
                },

                // 状态栏
                gtk4::Box {
                    set_orientation: gtk4::Orientation::Horizontal,
                    set_spacing: 6,
                    set_margin_all: 6,

                    gtk4::Label {
                        set_label: "Rust Edition v2.0.0",
                        add_css_class: "caption",
                    },

                    gtk4::Box {
                        set_hexpand: true,
                    },

                    gtk4::Label {
                        set_label: "就绪",
                        add_css_class: "caption",
                    },
                },
            },
        }
    }

    fn init(
        _init: Self::Init,
        _root: Self::Root,
        sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        let model = Self {
            current_page: AppPage::Wallpapers,
        };

        let widgets = view_output!();

        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, _sender: ComponentSender<Self>, widgets: &mut Self::Widgets) {
        match msg {
            AppMsg::NavigateTo(page) => {
                if self.current_page != page {
                    self.current_page = page;
                    widgets.page_stack.set_visible_child_name(page.name());
                }
            }
        }
    }
}
