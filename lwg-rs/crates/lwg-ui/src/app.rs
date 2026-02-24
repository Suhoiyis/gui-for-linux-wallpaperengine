use gtk4::prelude::*;
use relm4::prelude::*;
use crate::wallpaper_list::{WallpaperList, WallpaperListInput, WallpaperListOutput};
use lwg_core::{ConfigManager, WallpaperController};
use std::sync::Arc;
use tokio::sync::Mutex;

pub struct App {
    wallpaper_list: Controller<WallpaperList>,
    controller: Arc<Mutex<WallpaperController>>,
}

#[derive(Debug)]
pub enum AppMsg {
    WallpaperSelected(String),
    WallpaperApply(String),
}

#[relm4::component(pub)]
impl Component for App {
    type Init = ();
    type Input = AppMsg;
    type Output = ();
    type CommandOutput = ();

    view! {
        gtk4::ApplicationWindow {
            set_title: Some("Linux Wallpaper Engine - Rust"),
            set_default_width: 900,
            set_default_height: 700,

            gtk4::Box {
                set_orientation: gtk4::Orientation::Vertical,

                gtk4::HeaderBar {
                    pack_start = &gtk4::Button {
                        set_icon_name: "view-refresh-symbolic",
                        set_tooltip_text: Some("重新扫描"),
                    },
                    pack_end = &gtk4::MenuButton {
                        set_icon_name: "open-menu-symbolic",
                        set_tooltip_text: Some("菜单"),
                    },
                },

                gtk4::Box {
                    set_orientation: gtk4::Orientation::Horizontal,
                    set_spacing: 10,
                    set_margin_all: 10,
                    set_vexpand: true,

                    gtk4::Box {
                        set_orientation: gtk4::Orientation::Vertical,
                        set_spacing: 10,
                        set_width_request: 200,

                        gtk4::Label {
                            set_label: "壁纸库",
                            add_css_class: "title-2",
                        },

                        gtk4::Separator {},

                        gtk4::SearchEntry {
                            set_placeholder_text: Some("搜索壁纸..."),
                        },

                        gtk4::Label {
                            set_label: "选择壁纸应用",
                            add_css_class: "dim-label",
                        },
                    },

                    gtk4::Separator {
                        set_orientation: gtk4::Orientation::Vertical,
                    },

                    #[local_ref]
                    wallpaper_list_widget -> gtk4::ScrolledWindow {},
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
        };

        let wallpaper_list_widget = model.wallpaper_list.widget();
        let widgets = view_output!();

        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, _sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            AppMsg::WallpaperSelected(id) => {
                println!("选中：{}", id);
            }
            AppMsg::WallpaperApply(id) => {
                println!("应用：{}", id);
                let controller = Arc::clone(&self.controller);
                relm4::spawn(async move {
                    let mut ctrl = controller.lock().await;
                    let _ = ctrl.apply(&id, None).await;
                });
            }
        }
    }
}
