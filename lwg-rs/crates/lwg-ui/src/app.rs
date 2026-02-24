use gtk4::prelude::*;
use relm4::prelude::*;
use libadwaita::{self, prelude::*};
use crate::wallpaper_list::{WallpaperList, WallpaperListOutput};
use lwg_core::{ConfigManager, WallpaperController};
use std::sync::Arc;
use tokio::sync::Mutex;

pub struct App {
    wallpaper_list: Controller<WallpaperList>,
    controller: Arc<Mutex<WallpaperController>>,
    current_page: Page,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Page {
    Wallpapers,
    Settings,
    Performance,
}

#[derive(Debug)]
pub enum AppMsg {
    WallpaperSelected(String),
    WallpaperApply(String),
    NavigateTo(Page),
    ShowAbout,
    ShowPreferences,
}

#[relm4::component(pub)]
impl Component for App {
    type Init = ();
    type Input = AppMsg;
    type Output = ();
    type CommandOutput = ();

    view! {
        libadwaita::ApplicationWindow {
            set_title: Some("Linux Wallpaper Engine"),
            set_default_width: 1200,
            set_default_height: 800,

            #[wrap(Some)]
            set_content = &gtk4::Box {
                set_orientation: gtk4::Orientation::Vertical,

                // 导航栏
                libadwaita::HeaderBar {
                    set_title_widget: Some(&gtk4::Label::new(Some("Linux Wallpaper Engine"))),

                    pack_start = &gtk4::Button {
                        set_icon_name: "view-refresh-symbolic",
                        set_tooltip_text: Some("重新扫描"),
                    },

                    pack_end = &gtk4::MenuButton {
                        set_icon_name: "open-menu-symbolic",
                        set_tooltip_text: Some("菜单"),
                    },
                },

                // 视图切换器
                gtk4::Box {
                    set_orientation: gtk4::Orientation::Horizontal,
                    set_spacing: 0,
                    set_halign: gtk4::Align::Center,
                    set_margin_top: 6,
                    set_margin_bottom: 6,

                    gtk4::Button {
                        set_icon_name: "emblem-photos-symbolic",
                        set_label: "壁纸",
                        add_css_class: "flat",
                        connect_clicked => AppMsg::NavigateTo(Page::Wallpapers),
                    },

                    gtk4::Button {
                        set_icon_name: "preferences-system-symbolic",
                        set_label: "设置",
                        add_css_class: "flat",
                        connect_clicked => AppMsg::NavigateTo(Page::Settings),
                    },

                    gtk4::Button {
                        set_icon_name: "utilities-system-monitor-symbolic",
                        set_label: "性能",
                        add_css_class: "flat",
                        connect_clicked => AppMsg::NavigateTo(Page::Performance),
                    },
                },

                // 页面内容
                gtk4::Stack {
                    set_hexpand: true,
                    set_vexpand: true,

                    add_child: wallpapers_page = &gtk4::Box {
                        set_orientation: gtk4::Orientation::Horizontal,
                        set_spacing: 0,

                        // 左侧边栏
                        gtk4::Box {
                            set_orientation: gtk4::Orientation::Vertical,
                            set_spacing: 12,
                            set_width_request: 280,
                            set_margin_all: 12,

                            gtk4::Label {
                                set_label: "壁纸库",
                                add_css_class: "title-2",
                                set_halign: gtk4::Align::Start,
                            },

                            gtk4::Separator {},

                            gtk4::SearchEntry {
                                set_placeholder_text: Some("搜索壁纸..."),
                            },

                            gtk4::Label {
                                set_label: "选择壁纸应用",
                                add_css_class: "dim-label",
                                set_halign: gtk4::Align::Start,
                            },
                        },

                        gtk4::Separator {
                            set_orientation: gtk4::Orientation::Vertical,
                        },

                        // 主内容区
                        #[local_ref]
                        wallpaper_list_widget -> gtk4::ScrolledWindow {
                            set_hexpand: true,
                            set_vexpand: true,
                        },
                    } -> {
                        set_name: "wallpapers",
                        set_title: "壁纸",
                    },

                    add_child: settings_page = &gtk4::Box {
                        set_orientation: gtk4::Orientation::Vertical,
                        set_spacing: 12,
                        set_margin_all: 24,

                        gtk4::Label {
                            set_label: "设置",
                            add_css_class: "title-1",
                            set_halign: gtk4::Align::Start,
                        },

                        gtk4::Label {
                            set_label: "设置页面内容待实现",
                            set_halign: gtk4::Align::Start,
                        },
                    } -> {
                        set_name: "settings",
                        set_title: "设置",
                    },

                    add_child: performance_page = &gtk4::Box {
                        set_orientation: gtk4::Orientation::Vertical,
                        set_spacing: 12,
                        set_margin_all: 24,

                        gtk4::Label {
                            set_label: "性能监控",
                            add_css_class: "title-1",
                            set_halign: gtk4::Align::Start,
                        },

                        gtk4::Label {
                            set_label: "性能监控页面内容待实现",
                            set_halign: gtk4::Align::Start,
                        },
                    } -> {
                        set_name: "performance",
                        set_title: "性能",
                    },
                },
            },
        }
    }

    fn init(
        _init: Self::Init,
        root: Self::Root,
        sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        let wallpaper_list = WallpaperList::builder()
            .launch(())
            .forward(sender.input_sender(), |msg| match msg {
                WallpaperListOutput::Selected(id) => AppMsg::WallpaperSelected(id),
                WallpaperListOutput::Apply(id) => AppMsg::WallpaperApply(id),
            });

        let config = Arc::new(Mutex::new(
            ConfigManager::new().map(|c| c.config).unwrap_or_default()
        ));
        let controller = Arc::new(Mutex::new(WallpaperController::new(Arc::clone(&config))));

        let model = Self {
            wallpaper_list,
            controller,
            current_page: Page::Wallpapers,
        };

        let wallpaper_list_widget = model.wallpaper_list.widget();
        let widgets = view_output!();

        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, _sender: ComponentSender<Self>, root: &Self::Root) {
        match msg {
            AppMsg::WallpaperSelected(id) => {
                println!("选中壁纸：{}", id);
            }
            AppMsg::WallpaperApply(id) => {
                println!("应用壁纸：{}", id);
                let controller = Arc::clone(&self.controller);
                relm4::spawn(async move {
                    let mut ctrl = controller.lock().await;
                    let _ = ctrl.apply(&id, None).await;
                });
            }
            AppMsg::NavigateTo(page) => {
                println!("导航到页面：{:?}", page);
                self.current_page = page;
                
                // 获取 Stack 并切换页面
                if let Some(content) = root.content() {
                    if let Some(stack) = content.downcast_ref::<gtk4::Stack>() {
                        let page_name = match page {
                            Page::Wallpapers => "wallpapers",
                            Page::Settings => "settings",
                            Page::Performance => "performance",
                        };
                        stack.set_visible_child_name(page_name);
                    }
                }
            }
            AppMsg::ShowAbout => {
                println!("显示关于对话框");
            }
            AppMsg::ShowPreferences => {
                println!("显示首选项");
            }
        }
    }
}
