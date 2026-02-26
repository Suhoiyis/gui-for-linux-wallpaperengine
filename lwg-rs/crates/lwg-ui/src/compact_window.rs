//! 紧凑模式窗口 - 快捷键支持完整实现
//! 审计报告 Task 4.1.3: CompactWindow 快捷键支持

use gtk4::prelude::*;
use relm4::prelude::*;
use libadwaita as adw;
use std::collections::VecDeque;

const THUMB_COUNT: usize = 5;

#[derive(Debug, Clone)]
pub struct WallpaperThumb {
    pub id: String,
    pub title: String,
    pub thumbnail: Option<String>,
}

#[derive(Debug)]
pub enum CompactWindowInput {
    Show,
    Hide,
    ToggleFullscreen,
    RestartWallpaper,
    ScreenChanged(String),
    LoadWallpapers(Vec<WallpaperThumb>),
    NextWallpaper,
    PreviousWallpaper,
    SelectWallpaper(usize),
    KeyPressed(gtk4::gdk::Key),
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
    wallpapers: Vec<WallpaperThumb>,
    current_index: usize,
}

#[relm4::component(pub)]
impl Component for CompactWindow {
    type Init = ();
    type Input = CompactWindowInput;
    type Output = CompactWindowOutput;
    type CommandOutput = ();

    view! {
        #[local_ref]
        adw::ApplicationWindow {
            set_title: Some("Wallpaper Preview"),
            set_default_width: 300,
            set_default_height: 700,
            set_modal: true,

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
                    },

                    #[name = "wallpaper_title"]
                    gtk4::Label {
                        set_label: "壁纸名称",
                        add_css_class: "heading",
                    },
                },

                gtk4::Separator {},

                // 缩略图导航
                gtk4::Box {
                    set_orientation: gtk4::Orientation::Horizontal,
                    set_spacing: 8,
                    set_margin_all: 12,
                    set_halign: gtk4::Align::Center,

                    #[name = "prev_btn"]
                    gtk4::Button {
                        set_icon_name: "go-previous-symbolic",
                        set_tooltip_text: Some("上一个"),
                    },

                    gtk4::Box {
                        set_orientation: gtk4::Orientation::Horizontal,
                        set_spacing: 8,

                        #[name = "thumb_box"]
                        gtk4::Box {
                            set_orientation: gtk4::Orientation::Horizontal,
                            set_spacing: 8,
                        },
                    },

                    #[name = "next_btn"]
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
        root: Self::Root,
        sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        let model = Self {
            visible: false,
            fullscreen: false,
            wallpapers: Vec::new(),
            current_index: 0,
        };

        let widgets = view_output!();

        // 添加快捷键控制器
        let key_controller = gtk4::EventControllerKey::new();
        key_controller.connect_key_pressed(move |_controller, key, _code, _modifier| {
            sender.input(CompactWindowInput::KeyPressed(key));
            gtk4::Inhibit(false)
        });
        root.add_controller(key_controller);

        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, sender: ComponentSender<Self>, widgets: &mut Self::Widgets) {
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
            CompactWindowInput::RestartWallpaper => {
                sender.output(CompactWindowOutput::RestartRequested).ok();
            }
            CompactWindowInput::ScreenChanged(screen) => {
                sender.output(CompactWindowOutput::ScreenChanged(screen)).ok();
            }
            CompactWindowInput::LoadWallpapers(wallpapers) => {
                self.wallpapers = wallpapers;
                self.update_display(widgets);
            }
            CompactWindowInput::NextWallpaper => {
                if !self.wallpapers.is_empty() {
                    self.current_index = (self.current_index + 1) % self.wallpapers.len();
                    self.update_display(widgets);
                }
            }
            CompactWindowInput::PreviousWallpaper => {
                if !self.wallpapers.is_empty() {
                    self.current_index = if self.current_index == 0 {
                        self.wallpapers.len() - 1
                    } else {
                        self.current_index - 1
                    };
                    self.update_display(widgets);
                }
            }
            CompactWindowInput::SelectWallpaper(index) => {
                if index < self.wallpapers.len() {
                    self.current_index = index;
                    self.update_display(widgets);
                    let id = self.wallpapers[index].id.clone();
                    sender.output(CompactWindowOutput::WallpaperSelected(id)).ok();
                }
            }
            CompactWindowInput::KeyPressed(key) => {
                match key {
                    gtk4::gdk::Key::Left => {
                        sender.input(CompactWindowInput::PreviousWallpaper);
                    }
                    gtk4::gdk::Key::Right => {
                        sender.input(CompactWindowInput::NextWallpaper);
                    }
                    gtk4::gdk::Key::Return | gtk4::gdk::Key::KP_Enter => {
                        if !self.wallpapers.is_empty() {
                            let id = self.wallpapers[self.current_index].id.clone();
                            sender.output(CompactWindowOutput::ApplyWallpaper(id)).ok();
                        }
                    }
                    gtk4::gdk::Key::s | gtk4::gdk::Key::S => {
                        sender.output(CompactWindowOutput::StopWallpaper).ok();
                    }
                    gtk4::gdk::Key::l | gtk4::gdk::Key::L => {
                        sender.output(CompactWindowOutput::RandomWallpaper).ok();
                    }
                    gtk4::gdk::Key::KP_1 | gtk4::gdk::Key::_1 => {
                        if self.wallpapers.len() >= 1 {
                            sender.input(CompactWindowInput::SelectWallpaper(0));
                        }
                    }
                    gtk4::gdk::Key::KP_2 | gtk4::gdk::Key::_2 => {
                        if self.wallpapers.len() >= 2 {
                            sender.input(CompactWindowInput::SelectWallpaper(1));
                        }
                    }
                    gtk4::gdk::Key::KP_3 | gtk4::gdk::Key::_3 => {
                        if self.wallpapers.len() >= 3 {
                            sender.input(CompactWindowInput::SelectWallpaper(2));
                        }
                    }
                    gtk4::gdk::Key::KP_4 | gtk4::gdk::Key::_4 => {
                        if self.wallpapers.len() >= 4 {
                            sender.input(CompactWindowInput::SelectWallpaper(3));
                        }
                    }
                    gtk4::gdk::Key::KP_5 | gtk4::gdk::Key::_5 => {
                        if self.wallpapers.len() >= 5 {
                            sender.input(CompactWindowInput::SelectWallpaper(4));
                        }
                    }
                    _ => {}
                }
            }
        }
    }
}

impl CompactWindow {
    fn update_display(&self, widgets: &mut Self::Widgets) {
        if self.current_index < self.wallpapers.len() {
            let wp = &self.wallpapers[self.current_index];
            widgets.wallpaper_title.set_text(&wp.title);
            widgets.info_label.set_text(&format!("{}/{}", self.current_index + 1, self.wallpapers.len()));
        }
    }
}
