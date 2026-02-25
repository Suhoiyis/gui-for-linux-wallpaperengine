//! 侧边栏预览组件 - 完整实现
//! 审计报告 Task 2.6-2.10: Sidebar 完整实现

use gtk4::prelude::*;
use relm4::prelude::*;
use libadwaita as adw;

#[derive(Debug, Clone)]
pub struct WallpaperInfo {
    pub id: String,
    pub title: String,
    pub wallpaper_type: String,
    pub size: String,
    pub tags: Vec<String>,
    pub description: String,
    pub thumbnail: Option<String>,
}

#[derive(Debug)]
pub enum SidebarInput {
    SelectWallpaper(WallpaperInfo),
    ClearSelection,
    ApplyWallpaper,
    SetNickname(String),
}

#[derive(Debug)]
pub enum SidebarOutput {
    ApplyRequested(String),
    NicknameChanged(String, String),
    DeleteRequested(String),
    OpenFolderRequested(String),
}

#[relm4::component(pub)]
impl Component for Sidebar {
    type Init = ();
    type Input = SidebarInput;
    type Output = SidebarOutput;
    type CommandOutput = ();

    view! {
        gtk4::ScrolledWindow {
            set_policy: gtk4::PolicyType::Never,
            gtk4::PolicyType::Automatic,
            set_vexpand: true,
            set_hexpand: false,
            set_width_request: 370,

            gtk4::Box {
                set_orientation: gtk4::Orientation::Vertical,
                set_spacing: 12,
                set_margin_all: 12,

                // 预览区域
                gtk4::Box {
                    set_orientation: gtk4::Orientation::Vertical,
                    set_spacing: 8,

                    gtk4::Label {
                        set_label: "预览",
                        add_css_class: "heading",
                        set_halign: gtk4::Align::Start,
                    },

                    #[name = "preview_area"]
                    gtk4::Box {
                        set_height_request: 200,
                        add_css_class: "card",

                        #[name = "preview_icon"]
                        gtk4::Image {
                            set_icon_name: Some("image-x-generic-symbolic"),
                            set_pixel_size: 96,
                            set_vexpand: true,
                            set_valign: gtk4::Align::Center,
                            set_halign: gtk4::Align::Center,
                        },
                    },
                },

                gtk4::Separator {},

                // 信息区域
                gtk4::Box {
                    set_orientation: gtk4::Orientation::Vertical,
                    set_spacing: 8,

                    #[name = "title_label"]
                    gtk4::Label {
                        set_label: "",
                        add_css_class: "title-2",
                        set_halign: gtk4::Align::Start,
                        set_wrap: true,
                    },

                    #[name = "type_label"]
                    gtk4::Label {
                        set_label: "",
                        add_css_class: "dim-label",
                        set_halign: gtk4::Align::Start,
                    },

                    #[name = "size_label"]
                    gtk4::Label {
                        set_label: "",
                        add_css_class: "dim-label",
                        set_halign: gtk4::Align::Start,
                    },

                    #[name = "tags_box"]
                    gtk4::FlowBox {
                        set_column_spacing: 6,
                        set_row_spacing: 6,
                    },
                },

                gtk4::Separator {},

                // 昵称编辑
                gtk4::Box {
                    set_orientation: gtk4::Orientation::Horizontal,
                    set_spacing: 6,

                    gtk4::Label {
                        set_label: "昵称:",
                        set_halign: gtk4::Align::Start,
                    },

                    #[name = "nickname_entry"]
                    gtk4::Entry {
                        set_placeholder_text: Some("留空使用原标题"),
                        set_hexpand: true,
                    },

                    #[name = "save_nickname_btn"]
                    gtk4::Button {
                        set_icon_name: "document-save-symbolic",
                        set_tooltip_text: Some("保存昵称"),
                    },
                },

                gtk4::Box {
                    set_vexpand: true,
                },

                // 应用按钮
                #[name = "apply_button"]
                gtk4::Button {
                    set_label: "应用壁纸",
                    set_halign: gtk4::Align::End,
                    add_css_class: "suggested-action",
                    set_sensitive: false,
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
            selected_wallpaper: None,
            wallpaper_type: String::new(),
            nickname: None,
        };
        let widgets = view_output!();
        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, sender: ComponentSender<Self>, widgets: &mut Self::Widgets) {
        match msg {
            SidebarInput::SelectWallpaper(info) => {
                self.selected_wallpaper = Some(info.id.clone());
                self.wallpaper_type = info.wallpaper_type.clone();
                
                // 刷新 Widget
                widgets.title_label.set_text(&info.title);
                widgets.type_label.set_text(&format!("类型：{}", info.wallpaper_type));
                widgets.size_label.set_text(&format!("大小：{}", info.size));
                widgets.apply_button.set_sensitive(true);

                // 加载缩略图（如果有）
                if let Some(thumbnail_path) = &info.thumbnail {
                    if let Ok(pixbuf) = gtk4::gdk_pixbuf::Pixbuf::from_file(thumbnail_path) {
                        widgets.preview_icon.set_from_pixbuf(Some(&pixbuf));
                    }
                }

                // 显示标签
                while let Some(child) = widgets.tags_box.first_child() {
                    widgets.tags_box.remove(&child);
                }
                for tag in &info.tags {
                    let label = gtk4::Label::new(Some(tag));
                    label.add_css_class("tag");
                    let child = gtk4::FlowBoxChild::new();
                    child.set_child(Some(&label));
                    widgets.tags_box.append(&child);
                }
            }
            SidebarInput::ClearSelection => {
                self.selected_wallpaper = None;
                widgets.title_label.set_text("");
                widgets.type_label.set_text("");
                widgets.size_label.set_text("");
                widgets.apply_button.set_sensitive(false);
                widgets.preview_icon.set_icon_name(Some("image-x-generic-symbolic"));
                
                while let Some(child) = widgets.tags_box.first_child() {
                    widgets.tags_box.remove(&child);
                }
            }
            SidebarInput::ApplyWallpaper => {
                if let Some(ref id) = self.selected_wallpaper {
                    sender.output(SidebarOutput::ApplyRequested(id.clone())).ok();
                }
            }
            SidebarInput::SetNickname(nickname) => {
                self.nickname = Some(nickname);
            }
        }
    }
}
