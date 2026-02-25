use gtk4::prelude::*;
use relm4::prelude::*;

pub struct StatusPanel {
    is_running: bool,
    current_wallpaper: Option<String>,
}

#[derive(Debug)]
pub enum StatusPanelInput {
    SetRunning(bool),
    SetWallpaper(String),
    ClearWallpaper,
}

#[derive(Debug)]
pub enum StatusPanelOutput {
    StopWallpaper,
    ApplyLast,
}

#[relm4::component(pub)]
impl Component for StatusPanel {
    type Init = ();
    type Input = StatusPanelInput;
    type Output = StatusPanelOutput;
    type CommandOutput = ();

    view! {
        gtk4::Box {
            set_orientation: gtk4::Orientation::Horizontal,
            set_spacing: 12,
            set_margin_all: 12,
            add_css_class: "toolbar",

            // 左侧：状态指示器
            gtk4::Box {
                set_orientation: gtk4::Orientation::Horizontal,
                set_spacing: 8,

                #[name = "status_icon"]
                gtk4::Image {
                    set_icon_name: Some("media-playback-stop-symbolic"),
                    set_pixel_size: 16,
                },

                #[name = "status_label"]
                gtk4::Label {
                    set_label: "已停止",
                    add_css_class: "dim-label",
                },
            },

            gtk4::Box {
                set_hexpand: true,
            },

            // 中间：当前壁纸信息
            #[name = "wallpaper_info"]
            gtk4::Box {
                set_orientation: gtk4::Orientation::Horizontal,
                set_spacing: 8,
                set_visible: false,

                gtk4::Label {
                    set_label: "当前:",
                    add_css_class: "dim-label",
                },

                #[name = "wallpaper_name"]
                gtk4::Label {
                    set_label: "",
                    add_css_class: "heading",
                },
            },

            gtk4::Box {
                set_hexpand: true,
            },

            // 右侧：控制按钮
            gtk4::Box {
                set_orientation: gtk4::Orientation::Horizontal,
                set_spacing: 6,

                #[name = "btn_stop"]
                gtk4::Button {
                    set_icon_name: "media-playback-stop-symbolic",
                    set_tooltip_text: Some("停止壁纸"),
                    set_sensitive: false,
                    add_css_class: "flat",
                    connect_clicked[sender] => move |_| {
                        sender.output(StatusPanelOutput::StopWallpaper).ok();
                    },
                },

                #[name = "btn_reapply"]
                gtk4::Button {
                    set_icon_name: "view-refresh-symbolic",
                    set_tooltip_text: Some("重新应用"),
                    add_css_class: "flat",
                    connect_clicked[sender] => move |_| {
                        sender.output(StatusPanelOutput::ApplyLast).ok();
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
            is_running: false,
            current_wallpaper: None,
        };

        let widgets = view_output!();

        ComponentParts { model, widgets }
    }

    fn update(
        &mut self,
        msg: Self::Input,
        _sender: ComponentSender<Self>,
        widgets: &Self::Widgets,
    ) {
        match msg {
            StatusPanelInput::SetRunning(running) => {
                self.is_running = running;

                if running {
                    widgets
                        .status_icon
                        .set_icon_name(Some("media-playback-start-symbolic"));
                    widgets.status_label.set_label("运行中");
                    widgets.status_label.add_css_class("accent");
                    widgets.btn_stop.set_sensitive(true);
                } else {
                    widgets
                        .status_icon
                        .set_icon_name(Some("media-playback-stop-symbolic"));
                    widgets.status_label.set_label("已停止");
                    widgets.status_label.remove_css_class("accent");
                    widgets.btn_stop.set_sensitive(false);
                }
            }
            StatusPanelInput::SetWallpaper(name) => {
                self.current_wallpaper = Some(name.clone());
                widgets.wallpaper_name.set_label(&name);
                widgets.wallpaper_info.set_visible(true);
            }
            StatusPanelInput::ClearWallpaper => {
                self.current_wallpaper = None;
                widgets.wallpaper_info.set_visible(false);
            }
        }
    }
}
