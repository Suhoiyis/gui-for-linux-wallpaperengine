//! 紧凑模式窗口 - 完整实现

use gtk4::prelude::*;
use relm4::prelude::*;
use libadwaita as adw;

#[derive(Debug)]
pub enum CompactWindowInput {
    Show,
    Hide,
    ToggleFullscreen,
    NextWallpaper,
    PreviousWallpaper,
    SelectWallpaper(usize),
    ApplyCurrent,
    StopWallpaper,
    RandomWallpaper,
}

#[derive(Debug)]
pub enum CompactWindowOutput {
    Closed,
    FullscreenToggled,
    RestartRequested,
    ScreenChanged(String),
    WallpaperSelected(String),
    ApplyWallpaper(String),
    StopWallpaper,
    RandomWallpaper,
}

pub struct CompactWindow {
    visible: bool,
    fullscreen: bool,
    current_index: usize,
    wallpaper_count: usize,
}

#[relm4::component(pub)]
impl Component for CompactWindow {
    type Init = ();
    type Input = CompactWindowInput;
    type Output = CompactWindowOutput;
    type CommandOutput = ();

    view! {
        adw::ApplicationWindow {
            set_title: Some("Wallpaper Preview"),
            set_default_width: 300,
            set_default_height: 700,

            #[wrap(Some)]
            set_content = &gtk4::Box {
                set_orientation: gtk4::Orientation::Vertical,

                // 顶部导航栏
                gtk4::Box {
                    set_orientation: gtk4::Orientation::Horizontal,
                    set_spacing: 6,
                    set_margin_all: 6,

                    #[name = "btn_fullscreen"]
                    gtk4::Button {
                        set_icon_name: "view-fullscreen-symbolic",
                        set_tooltip_text: Some("全屏切换"),
                    },

                    gtk4::Box {
                        set_hexpand: true,
                    },

                    #[name = "btn_restart"]
                    gtk4::Button {
                        set_icon_name: "system-reboot-symbolic",
                        set_tooltip_text: Some("重启壁纸"),
                    },

                    gtk4::Box {
                        set_hexpand: true,
                    },

                    #[name = "screen_selector"]
                    gtk4::DropDown {
                        set_model: Some(&gtk4::StringList::new(&["屏幕 1", "屏幕 2", "屏幕 3"])),
                        set_tooltip_text: Some("选择显示器"),
                    },
                },

                gtk4::Separator {},

                // 预览区域
                gtk4::Box {
                    set_orientation: gtk4::Orientation::Vertical,
                    set_spacing: 12,
                    set_margin_all: 12,
                    set_vexpand: true,

                    #[name = "preview_image"]
                    gtk4::Image {
                        set_icon_name: "image-x-generic-symbolic",
                        set_pixel_size: 128,
                        set_vexpand: true,
                        set_valign: gtk4::Align::Center,
                        set_halign: gtk4::Align::Center,
                    },

                    #[name = "wallpaper_title"]
                    gtk4::Label {
                        set_label: "壁纸名称",
                        add_css_class: "heading",
                        set_ellipsize: gtk4::pango::EllipsizeMode::End,
                        set_max_width_chars: 20,
                    },
                },

                gtk4::Separator {},

                // 缩略图导航（5 个圆形缩略图）
                gtk4::Box {
                    set_orientation: gtk4::Orientation::Horizontal,
                    set_spacing: 8,
                    set_margin_all: 12,
                    set_halign: gtk4::Align::Center,

                    #[name = "btn_prev"]
                    gtk4::Button {
                        set_icon_name: "go-previous-symbolic",
                        set_tooltip_text: Some("上一个"),
                    },

                    // 5 个缩略图占位
                    gtk4::Box {
                        set_orientation: gtk4::Orientation::Horizontal,
                        set_spacing: 8,

                        gtk4::Button {
                            set_width_request: 40,
                            set_height_request: 40,
                            add_css_class: "circular",
                            add_css_class: "thumbnail",
                        },

                        gtk4::Button {
                            set_width_request: 40,
                            set_height_request: 40,
                            add_css_class: "circular",
                            add_css_class: "thumbnail",
                        },

                        gtk4::Button {
                            set_width_request: 40,
                            set_height_request: 40,
                            add_css_class: "circular",
                            add_css_class: "thumbnail",
                        },

                        gtk4::Button {
                            set_width_request: 40,
                            set_height_request: 40,
                            add_css_class: "circular",
                            add_css_class: "thumbnail",
                        },

                        gtk4::Button {
                            set_width_request: 40,
                            set_height_request: 40,
                            add_css_class: "circular",
                            add_css_class: "thumbnail",
                        },
                    },

                    #[name = "btn_next"]
                    gtk4::Button {
                        set_icon_name: "go-next-symbolic",
                        set_tooltip_text: Some("下一个"),
                    },
                },

                gtk4::Separator {},

                // 底部信息
                gtk4::Box {
                    set_orientation: gtk4::Orientation::Horizontal,
                    set_spacing: 6,
                    set_margin_all: 6,

                    #[name = "info_label"]
                    gtk4::Label {
                        set_label: "1/5",
                        add_css_class: "caption",
                        set_hexpand: true,
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
            visible: false,
            fullscreen: false,
            current_index: 0,
            wallpaper_count: 5,
        };

        let widgets = view_output!();

        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            CompactWindowInput::Show => {
                self.visible = true;
            }
            CompactWindowInput::Hide => {
                self.visible = false;
                sender.output(CompactWindowOutput::Closed).ok();
            }
            CompactWindowInput::ToggleFullscreen => {
                self.fullscreen = !self.fullscreen;
                sender.output(CompactWindowOutput::FullscreenToggled).ok();
            }
            CompactWindowInput::NextWallpaper => {
                self.current_index = (self.current_index + 1) % self.wallpaper_count;
            }
            CompactWindowInput::PreviousWallpaper => {
                self.current_index = if self.current_index == 0 {
                    self.wallpaper_count - 1
                } else {
                    self.current_index - 1
                };
            }
            CompactWindowInput::SelectWallpaper(index) => {
                if index < self.wallpaper_count {
                    self.current_index = index;
                }
            }
            CompactWindowInput::ApplyCurrent => {
                sender.output(CompactWindowOutput::ApplyWallpaper(format!("wallpaper_{}", self.current_index))).ok();
            }
            CompactWindowInput::StopWallpaper => {
                sender.output(CompactWindowOutput::StopWallpaper).ok();
            }
            CompactWindowInput::RandomWallpaper => {
                sender.output(CompactWindowOutput::RandomWallpaper).ok();
            }
        }
    }
}
