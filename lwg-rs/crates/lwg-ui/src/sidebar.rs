//! 侧边栏预览组件 - 简化版（暂不更新 UI）

use gtk4::prelude::*;
use relm4::prelude::*;

#[derive(Debug, Clone)]
pub struct WallpaperInfo {
    pub id: String,
    pub title: String,
    pub wallpaper_type: String,
    pub size: String,
}

#[derive(Debug)]
pub enum SidebarInput {
    SelectWallpaper(WallpaperInfo),
    ClearSelection,
    ApplyWallpaper,
}

#[derive(Debug)]
pub enum SidebarOutput {
    ApplyRequested(String),
    NicknameChanged(String, String),
    DeleteRequested(String),
    OpenFolderRequested(String),
    WallpaperSelected(String, String, String, String), // id, title, type, size
}

pub struct Sidebar {
    selected_wallpaper: Option<String>,
    current_title: String,
    current_type: String,
    current_size: String,
}

#[relm4::component(pub)]
impl Component for Sidebar {
    type Init = ();
    type Input = SidebarInput;
    type Output = SidebarOutput;
    type CommandOutput = ();

    view! {
        gtk4::ScrolledWindow {
            set_policy: (gtk4::PolicyType::Never, gtk4::PolicyType::Automatic),
            set_vexpand: true,
            set_hexpand: false,
            set_width_request: 320,

            gtk4::Box {
                set_orientation: gtk4::Orientation::Vertical,
                set_spacing: 12,
                set_margin_all: 12,

                gtk4::Label {
                    set_label: "预览",
                    add_css_class: "heading",
                    set_halign: gtk4::Align::Start,
                },

                gtk4::Box {
                    set_height_request: 180,
                    add_css_class: "card",
                    
                    gtk4::Image {
                        set_icon_name: Some("image-x-generic-symbolic"),
                        set_pixel_size: 64,
                        set_vexpand: true,
                        set_valign: gtk4::Align::Center,
                        set_halign: gtk4::Align::Center,
                    },
                },

                gtk4::Separator {},

                gtk4::Label {
                    set_label: &model.current_title,
                    add_css_class: "title-2",
                    set_halign: gtk4::Align::Start,
                    set_wrap: true,
                },

                gtk4::Label {
                    set_label: &format!("类型：{}", model.current_type),
                    add_css_class: "dim-label",
                    set_halign: gtk4::Align::Start,
                },

                gtk4::Label {
                    set_label: &format!("大小：{}", model.current_size),
                    add_css_class: "dim-label",
                    set_halign: gtk4::Align::Start,
                },

                gtk4::Box {
                    set_vexpand: true,
                },

                gtk4::Button {
                    set_label: "应用壁纸",
                    set_halign: gtk4::Align::End,
                    add_css_class: "suggested-action",
                    connect_clicked => SidebarInput::ApplyWallpaper,
                    set_sensitive: model.selected_wallpaper.is_some(),
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
            selected_wallpaper: None,
            current_title: String::new(),
            current_type: String::new(),
            current_size: String::new(),
        };

        let widgets = view_output!();
        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            SidebarInput::SelectWallpaper(info) => {
                self.selected_wallpaper = Some(info.id.clone());
                self.current_title = info.title.clone();
                self.current_type = info.wallpaper_type.clone();
                self.current_size = info.size.clone();
                
                eprintln!("选中壁纸：{} - {}", info.id, info.title);
            }
            SidebarInput::ClearSelection => {
                self.selected_wallpaper = None;
                self.current_title = String::new();
                self.current_type = String::new();
                self.current_size = String::new();
            }
            SidebarInput::ApplyWallpaper => {
                if let Some(ref id) = self.selected_wallpaper {
                    sender.output(SidebarOutput::ApplyRequested(id.clone())).ok();
                }
            }
        }
    }
}
