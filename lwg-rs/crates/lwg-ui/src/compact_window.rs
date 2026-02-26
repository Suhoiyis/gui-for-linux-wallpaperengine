//! 紧凑模式窗口 - 框架实现
//! 审计报告 Task 4.1.1: CompactWindow 框架

use gtk4::prelude::*;
use relm4::prelude::*;
use libadwaita as adw;

#[derive(Debug)]
pub enum CompactWindowInput {
    Show,
    Hide,
    ToggleFullscreen,
    RestartWallpaper,
    ScreenChanged(String),
}

#[derive(Debug)]
pub enum CompactWindowOutput {
    Closed,
    FullscreenToggled,
    RestartRequested,
    ScreenChanged(String),
}

pub struct CompactWindow {
    visible: bool,
    fullscreen: bool,
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

                // 预览区域（占位）
                gtk4::Box {
                    set_orientation: gtk4::Orientation::Vertical,
                    set_spacing: 12,
                    set_margin_all: 12,
                    set_vexpand: true,

                    gtk4::Label {
                        set_label: "紧凑模式预览",
                        add_css_class: "heading",
                    },

                    gtk4::Image {
                        set_icon_name: "image-x-generic-symbolic",
                        set_pixel_size: 128,
                        set_vexpand: true,
                    },
                },

                gtk4::Separator {},

                // 底部信息
                gtk4::Box {
                    set_orientation: gtk4::Orientation::Horizontal,
                    set_spacing: 6,
                    set_margin_all: 6,

                    gtk4::Label {
                        set_label: "壁纸名称",
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
            CompactWindowInput::RestartWallpaper => {
                sender.output(CompactWindowOutput::RestartRequested).ok();
            }
            CompactWindowInput::ScreenChanged(screen) => {
                sender.output(CompactWindowOutput::ScreenChanged(screen)).ok();
            }
        }
    }
}
