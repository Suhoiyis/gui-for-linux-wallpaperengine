use gtk4::prelude::*;
use relm4::prelude::*;
use libadwaita::{self, prelude::*};

/// 侧边栏预览组件（完善版）
pub struct Sidebar {
    selected_wallpaper: Option<String>,
    wallpaper_type: String,
    nickname: Option<String>,
}

#[derive(Debug, Clone)]
pub struct WallpaperInfo {
    pub id: String,
    pub title: String,
    pub wallpaper_type: String,
    pub size: String,
    pub tags: Vec<String>,
    pub description: String,
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

                    #[name = "description_label"]
                    gtk4::Label {
                        set_label: "",
                        set_halign: gtk4::Align::Start,
                        set_wrap: true,
                    },
                },

                gtk4::Separator {},

                // 属性编辑区域（Web 壁纸）
                #[name = "properties_group"]
                gtk4::Box {
                    set_orientation: gtk4::Orientation::Vertical,
                    set_spacing: 8,
                    set_visible: false,

                    gtk4::Label {
                        set_label: "属性",
                        add_css_class: "heading",
                        set_halign: gtk4::Align::Start,
                    },

                    // 属性编辑器占位
                    gtk4::Label {
                        set_label: "属性编辑功能待实现",
                        add_css_class: "dim-label",
                    },
                },

                gtk4::Box {
                    set_vexpand: true,
                },

                // 昵称编辑
                gtk4::Box {
                    set_orientation: gtk4::Orientation::Horizontal,
                    set_spacing: 6,

                    gtk4::Label {
                        set_label: "昵称:",
                        set_halign: gtk4::Align::Start,
                    },

                    gtk4::Entry {
                        set_placeholder_text: Some("留空使用原标题"),
                        set_hexpand: true,
                    },

                    gtk4::Button {
                        set_icon_name: "edit-symbolic",
                        set_tooltip_text: Some("编辑昵称"),
                    },
                },

                // 应用按钮区域
                #[name = "apply_button_box"]
                gtk4::Box {
                    set_orientation: gtk4::Orientation::Vertical,
                    set_spacing: 6,

                    gtk4::Button {
                        set_label: "Apply Wallpaper",
                        add_css_class: "suggested-action",
                        set_hexpand: true,
                    },

                    gtk4::Box {
                        set_orientation: gtk4::Orientation::Horizontal,
                        set_spacing: 6,

                        gtk4::Button {
                            set_label: "右键菜单",
                            set_tooltip_text: Some("更多操作"),
                            set_hexpand: true,
                        },

                        gtk4::Button {
                            set_icon_name: "folder-symbolic",
                            set_tooltip_text: Some("打开文件夹"),
                        },
                    },
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
            wallpaper_type: String::new(),
            nickname: None,
        };
        let widgets = view_output!();
        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            SidebarInput::SelectWallpaper(info) => {
                self.selected_wallpaper = Some(info.id.clone());
                self.wallpaper_type = info.wallpaper_type.clone();
            }
            SidebarInput::ClearSelection => {
                self.selected_wallpaper = None;
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
