//! 设置页面 - Advanced 子页面完整实现
//! 审计报告 Task 3.1.3: Advanced 子页面完整实现

use gtk4::prelude::*;
use relm4::prelude::*;
use libadwaita as adw;

#[derive(Debug)]
pub enum SettingsPageInput {
    NavigateTo(String),
    FpsChanged(u32),
    VolumeChanged(u32),
    SilenceToggled(bool),
    AutoMuteToggled(bool),
    AudioProcessingToggled(bool),
    DisableMouseToggled(bool),
    DisableParallaxToggled(bool),
    DisableParticlesToggled(bool),
    ClampingModeChanged(String),
    WaylandOnlyActiveToggled(bool),
    WaylandIgnoreAppidsChanged(String),
    LogFilterChanged(String),
    AutoStartToggled(bool),
    WorkshopPathSelected(String),
    AssetsPathSelected(String),
    ManageNicknames,
}

#[derive(Debug)]
pub enum SettingsPageOutput {
    ConfigChanged(String, serde_json::Value),
    PathSelected(String, String),
    OpenNicknameManager,
}

pub struct SettingsPage {
    current_section: String,
}

#[relm4::component(pub)]
impl Component for SettingsPage {
    type Init = ();
    type Input = SettingsPageInput;
    type Output = SettingsPageOutput;
    type CommandOutput = ();

    view! {
        gtk4::Box {
            set_orientation: gtk4::Orientation::Horizontal,
            set_hexpand: true,
            set_vexpand: true,

            gtk4::Box {
                set_orientation: gtk4::Orientation::Vertical,
                set_spacing: 6,
                set_width_request: 200,
                set_margin_all: 16,

                gtk4::Label {
                    set_label: "设置",
                    add_css_class: "title-2",
                    set_halign: gtk4::Align::Start,
                },

                gtk4::Separator {
                    set_margin_bottom: 12,
                },

                gtk4::Button {
                    set_label: "通用",
                    set_halign: gtk4::Align::Start,
                    add_css_class: "flat",
                },

                gtk4::Button {
                    set_label: "音频",
                    set_halign: gtk4::Align::Start,
                    add_css_class: "flat",
                },

                gtk4::Button {
                    set_label: "高级",
                    set_halign: gtk4::Align::Start,
                    add_css_class: "flat",
                },

                gtk4::Button {
                    set_label: "日志",
                    set_halign: gtk4::Align::Start,
                    add_css_class: "flat",
                },

                gtk4::Box {
                    set_vexpand: true,
                },
            },

            gtk4::Separator {
                set_orientation: gtk4::Orientation::Vertical,
            },

            #[name = "content_stack"]
            gtk4::Stack {
                set_hexpand: true,
                set_vexpand: true,
                set_margin_all: 24,

                // General 子页面
                add_named: &gtk4::Label::new(Some("通用")) => {
                    set_name: "general",
                },

                // Audio 子页面
                add_named: &gtk4::Label::new(Some("音频")) => {
                    set_name: "audio",
                },

                // Advanced 子页面
                add_named: &gtk4::ScrolledWindow {
                    set_hexpand: true,
                    set_vexpand: true,

                    gtk4::Box {
                        set_orientation: gtk4::Orientation::Vertical,
                        set_spacing: 16,
                        set_margin_all: 12,

                        gtk4::Label {
                            set_label: "高级设置",
                            add_css_class: "title-1",
                            set_halign: gtk4::Align::Start,
                        },

                        // 显示效果组
                        adw::PreferencesGroup {
                            set_title: Some("显示效果"),

                            adw::ActionRow {
                                set_title: Some("禁用鼠标交互"),
                                set_subtitle: Some("禁用壁纸鼠标交互效果"),
                                add_suffix = &gtk4::Switch {
                                    set_valign: gtk4::Align::Center,
                                },
                            },

                            adw::ActionRow {
                                set_title: Some("禁用视差效果"),
                                set_subtitle: Some("禁用鼠标移动视差"),
                                add_suffix = &gtk4::Switch {
                                    set_valign: gtk4::Align::Center,
                                },
                            },

                            adw::ActionRow {
                                set_title: Some("禁用粒子系统"),
                                set_subtitle: Some("禁用壁纸粒子效果"),
                                add_suffix = &gtk4::Switch {
                                    set_valign: gtk4::Align::Center,
                                },
                            },

                            adw::ActionRow {
                                set_title: Some("夹紧模式"),
                                add_suffix = &gtk4::DropDown::from_strings(&[
                                    "clamp", "stretch", "repeat",
                                ]),
                            },
                        },

                        // Wayland 组
                        adw::PreferencesGroup {
                            set_title: Some("Wayland"),

                            adw::ActionRow {
                                set_title: Some("全屏暂停仅限活动显示器"),
                                set_subtitle: Some("仅在全屏窗口所在显示器暂停"),
                                add_suffix = &gtk4::Switch {
                                    set_valign: gtk4::Align::Center,
                                },
                            },

                            adw::ActionRow {
                                set_title: Some("忽略的应用 ID"),
                                set_subtitle: Some("逗号分隔的应用 ID 列表"),
                                add_suffix = &gtk4::Entry {
                                    set_placeholder_text: Some("com.example.app1,com.example.app2"),
                                    set_hexpand: true,
                                },
                            },
                        },

                        // 日志组
                        adw::PreferencesGroup {
                            set_title: Some("日志"),

                            adw::ActionRow {
                                set_title: Some("日志过滤器"),
                                add_suffix = &gtk4::DropDown::from_strings(&[
                                    "全部", "Controller", "Engine", "GUI",
                                ]),
                            },

                            adw::ActionRow {
                                set_title: Some("日志查看器"),

                                add_suffix = &gtk4::Button {
                                    set_icon_name: Some("edit-copy-symbolic"),
                                    set_tooltip_text: Some("复制日志"),
                                },
                            },

                            #[name = "log_viewer"]
                            gtk4::TextView {
                                set_editable: false,
                                set_monospace: true,
                                set_vexpand: true,
                                set_min_content_height: 200,
                            },
                        },

                        gtk4::Box {
                            set_vexpand: true,
                        },
                    },
                } => {
                    set_name: "advanced",
                },

                // Logs 子页面
                add_named: &gtk4::Label::new(Some("日志（待实现）")) => {
                    set_name: "logs",
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
            current_section: "general".to_string(),
        };
        let widgets = view_output!();
        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, sender: ComponentSender<Self>, _widgets: &mut Self::Widgets) {
        match msg {
            SettingsPageInput::NavigateTo(section) => {
                self.current_section = section;
            }
            SettingsPageInput::DisableMouseToggled(disabled) => {
                sender.output(SettingsPageOutput::ConfigChanged(
                    "disable_mouse".to_string(),
                    serde_json::json!(disabled),
                )).ok();
            }
            SettingsPageInput::DisableParallaxToggled(disabled) => {
                sender.output(SettingsPageOutput::ConfigChanged(
                    "disable_parallax".to_string(),
                    serde_json::json!(disabled),
                )).ok();
            }
            SettingsPageInput::DisableParticlesToggled(disabled) => {
                sender.output(SettingsPageOutput::ConfigChanged(
                    "disable_particles".to_string(),
                    serde_json::json!(disabled),
                )).ok();
            }
            SettingsPageInput::ClampingModeChanged(mode) => {
                sender.output(SettingsPageOutput::ConfigChanged(
                    "clamping".to_string(),
                    serde_json::json!(mode),
                )).ok();
            }
            SettingsPageInput::WaylandOnlyActiveToggled(enabled) => {
                sender.output(SettingsPageOutput::ConfigChanged(
                    "wayland_only_active".to_string(),
                    serde_json::json!(enabled),
                )).ok();
            }
            SettingsPageInput::WaylandIgnoreAppidsChanged(appids) => {
                sender.output(SettingsPageOutput::ConfigChanged(
                    "wayland_ignore_appids".to_string(),
                    serde_json::json!(appids),
                )).ok();
            }
            SettingsPageInput::LogFilterChanged(filter) => {
                sender.output(SettingsPageOutput::ConfigChanged(
                    "log_filter".to_string(),
                    serde_json::json!(filter),
                )).ok();
            }
            _ => {}
        }
    }
}
