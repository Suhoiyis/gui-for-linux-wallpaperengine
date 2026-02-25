//! 设置页面 - Audio 子页面完整实现
//! 审计报告 Task 3.1.2: Audio 子页面完整实现

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

            // 左侧导航
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

            // 右侧内容区域
            #[name = "content_stack"]
            gtk4::Stack {
                set_hexpand: true,
                set_vexpand: true,
                set_margin_all: 24,

                // General 子页面
                add_named: &gtk4::ScrolledWindow {
                    set_hexpand: true,
                    set_vexpand: true,

                    gtk4::Box {
                        set_orientation: gtk4::Orientation::Vertical,
                        set_spacing: 16,
                        set_margin_all: 12,

                        gtk4::Label {
                            set_label: "通用设置",
                            add_css_class: "title-1",
                            set_halign: gtk4::Align::Start,
                        },

                        adw::PreferencesGroup {
                            set_title: Some("启动"),
                            adw::ActionRow {
                                set_title: Some("开机自启"),
                                add_suffix = &gtk4::Switch {
                                    set_valign: gtk4::Align::Center,
                                },
                            },
                        },

                        adw::PreferencesGroup {
                            set_title: Some("性能"),
                            adw::ActionRow {
                                set_title: Some("FPS 限制"),
                                add_suffix = &gtk4::SpinButton::with_range(1.0, 144.0, 1.0),
                            },
                            adw::ActionRow {
                                set_title: Some("缩放模式"),
                                add_suffix = &gtk4::DropDown::from_strings(&[
                                    "默认", "拉伸", "适应", "填充",
                                ]),
                            },
                        },

                        adw::PreferencesGroup {
                            set_title: Some("音频"),
                            adw::ActionRow {
                                set_title: Some("静音"),
                                add_suffix = &gtk4::Switch {
                                    set_valign: gtk4::Align::Center,
                                },
                            },
                            adw::ActionRow {
                                set_title: Some("音量"),
                                add_suffix = &gtk4::Scale::with_range(
                                    gtk4::Orientation::Horizontal, 0.0, 100.0, 1.0,
                                ),
                            },
                        },

                        gtk4::Box {
                            set_vexpand: true,
                        },
                    },
                } => {
                    set_name: "general",
                },

                // Audio 子页面
                add_named: &gtk4::ScrolledWindow {
                    set_hexpand: true,
                    set_vexpand: true,

                    gtk4::Box {
                        set_orientation: gtk4::Orientation::Vertical,
                        set_spacing: 16,
                        set_margin_all: 12,

                        gtk4::Label {
                            set_label: "音频设置",
                            add_css_class: "title-1",
                            set_halign: gtk4::Align::Start,
                        },

                        // 音量控制组
                        adw::PreferencesGroup {
                            set_title: Some("音量控制"),

                            adw::ActionRow {
                                set_title: Some("默认音量"),
                                set_subtitle: Some("0-100"),

                                #[wrap(Some)]
                                add_prefix = &gtk4::Scale::with_range(
                                    gtk4::Orientation::Horizontal,
                                    0.0,
                                    100.0,
                                    1.0,
                                ),
                            },
                        },

                        // 自动静音组
                        adw::PreferencesGroup {
                            set_title: Some("自动静音"),

                            adw::ActionRow {
                                set_title: Some("自动静音"),
                                set_subtitle: Some("失去焦点时自动静音"),

                                add_suffix = &gtk4::Switch {
                                    set_valign: gtk4::Align::Center,
                                },
                            },
                        },

                        // 音频处理组
                        adw::PreferencesGroup {
                            set_title: Some("音频处理"),

                            adw::ActionRow {
                                set_title: Some("启用音频处理"),
                                set_subtitle: Some("降噪、均衡等效果"),

                                add_suffix = &gtk4::Switch {
                                    set_valign: gtk4::Align::Center,
                                },
                            },
                        },

                        gtk4::Box {
                            set_vexpand: true,
                        },
                    },
                } => {
                    set_name: "audio",
                },

                // Advanced 子页面（占位）
                add_named: &gtk4::Label::new(Some("高级设置（待实现）")) => {
                    set_name: "advanced",
                },

                // Logs 子页面（占位）
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
            SettingsPageInput::VolumeChanged(volume) => {
                sender.output(SettingsPageOutput::ConfigChanged(
                    "volume".to_string(),
                    serde_json::json!(volume),
                )).ok();
            }
            SettingsPageInput::AutoMuteToggled(auto_mute) => {
                sender.output(SettingsPageOutput::ConfigChanged(
                    "auto_mute".to_string(),
                    serde_json::json!(auto_mute),
                )).ok();
            }
            SettingsPageInput::AudioProcessingToggled(enabled) => {
                sender.output(SettingsPageOutput::ConfigChanged(
                    "audio_processing".to_string(),
                    serde_json::json!(enabled),
                )).ok();
            }
            _ => {}
        }
    }
}
