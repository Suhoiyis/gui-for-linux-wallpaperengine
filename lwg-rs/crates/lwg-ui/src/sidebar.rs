use gtk4::prelude::*;
use libadwaita::{self, prelude::*};
use relm4::prelude::*;

pub struct Sidebar {
    selected_wallpaper: Option<WallpaperInfo>,
}

#[derive(Debug, Clone)]
pub struct WallpaperInfo {
    pub id: String,
    pub title: String,
    pub wallpaper_type: String,
    pub size: String,
    pub tags: Vec<String>,
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
}

#[relm4::component(pub)]
impl Component for Sidebar {
    type Init = ();
    type Input = SidebarInput;
    type Output = SidebarOutput;
    type CommandOutput = ();

    view! {
        gtk4::Box {
            set_orientation: gtk4::Orientation::Vertical,
            set_spacing: 16,
            set_width_request: 320,
            set_margin_all: 16,

            // 预览区域
            gtk4::Box {
                set_orientation: gtk4::Orientation::Vertical,
                set_spacing: 8,

                gtk4::Label {
                    set_label: "预览",
                    add_css_class: "heading",
                    set_halign: gtk4::Align::Start,
                },

                #[name = "preview_image"]
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
            },

            gtk4::Separator {},

            // 信息区域
            gtk4::Box {
                set_orientation: gtk4::Orientation::Vertical,
                set_spacing: 12,
                set_hexpand: true,

                #[name = "info_box"]
                gtk4::Box {
                    set_orientation: gtk4::Orientation::Vertical,
                    set_spacing: 8,
                    set_visible: false,

                    #[name = "title_label"]
                    gtk4::Label {
                        add_css_class: "title-2",
                        set_halign: gtk4::Align::Start,
                        set_wrap: true,
                    },

                    #[name = "type_label"]
                    gtk4::Label {
                        set_halign: gtk4::Align::Start,
                        add_css_class: "dim-label",
                    },

                    #[name = "size_label"]
                    gtk4::Label {
                        set_halign: gtk4::Align::Start,
                        add_css_class: "dim-label",
                    },

                    gtk4::Box {
                        set_orientation: gtk4::Orientation::Horizontal,
                        set_spacing: 8,
                        set_margin_top: 8,

                        #[name = "tags_box"]
                        gtk4::Box {
                            set_orientation: gtk4::Orientation::Horizontal,
                            set_spacing: 6,
                        },
                    },
                },

                #[name = "empty_label"]
                gtk4::Label {
                    set_label: "选择壁纸查看详情",
                    add_css_class: "dim-label",
                    set_halign: gtk4::Align::Center,
                    set_vexpand: true,
                },
            },

            gtk4::Box {
                set_vexpand: true,
            },

            // 操作按钮
            gtk4::Box {
                set_orientation: gtk4::Orientation::Vertical,
                set_spacing: 8,

                #[name = "apply_button"]
                gtk4::Button {
                    set_label: "应用壁纸",
                    add_css_class: "suggested-action",
                    add_css_class: "pill",
                    set_sensitive: false,
                    connect_clicked(sender) => move |_| {
                        sender.input(SidebarInput::ApplyWallpaper);
                    },
                },

                gtk4::Button {
                    set_label: "停止壁纸",
                    add_css_class: "destructive-action",
                },
            },
        }
    }

    fn init(
        _init: Self::Init,
        root: Self::Root,
        sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        let model = Self {
            selected_wallpaper: None,
        };

        let widgets = view_output!();

        ComponentParts { model, widgets }
    }

    fn update(
        &mut self,
        msg: Self::Input,
        sender: ComponentSender<Self>,
        widgets: &mut Self::Widgets,
    ) {
        match msg {
            SidebarInput::SelectWallpaper(info) => {
                self.selected_wallpaper = Some(info.clone());

                // 显示信息
                widgets.title_label.set_label(&info.title);
                widgets
                    .type_label
                    .set_label(&format!("类型: {}", info.wallpaper_type));
                widgets
                    .size_label
                    .set_label(&format!("大小: {}", info.size));

                // 清空并添加标签
                while let Some(child) = widgets.tags_box.first_child() {
                    widgets.tags_box.remove(&child);
                }
                for tag in &info.tags {
                    let label = gtk4::Label::new(Some(tag));
                    label.add_css_class("tag");
                    widgets.tags_box.append(&label);
                }

                widgets.info_box.set_visible(true);
                widgets.empty_label.set_visible(false);
                widgets.apply_button.set_sensitive(true);
            }
            SidebarInput::ClearSelection => {
                self.selected_wallpaper = None;
                widgets.info_box.set_visible(false);
                widgets.empty_label.set_visible(true);
                widgets.apply_button.set_sensitive(false);
            }
            SidebarInput::ApplyWallpaper => {
                if let Some(ref info) = self.selected_wallpaper {
                    sender
                        .output(SidebarOutput::ApplyRequested(info.id.clone()))
                        .ok();
                }
            }
        }
    }
}
