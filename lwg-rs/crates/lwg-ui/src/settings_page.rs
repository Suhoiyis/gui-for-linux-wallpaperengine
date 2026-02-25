//! 设置页面 - General 子页面完整实现
//! 审计报告 Task 3.1: General 子页面完整实现

use gtk4::prelude::*;
use relm4::prelude::*;
use libadwaita as adw;

#[derive(Debug)]
pub enum SettingsPageInput {
    NavigateTo(String),
    FpsChanged(u32),
    VolumeChanged(u32),
    SilenceToggled(bool),
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

                #[name = "nav_general"]
                gtk4::Button {
                    set_label: "通用",
                    set_halign: gtk4::Align::Start,
                    add_css_class: "flat",
                },

                #[name = "nav_audio"]
                gtk4::Button {
                    set_label: "音频",
                    set_halign: gtk4::Align::Start,
                    add_css_class: "flat",
                },

                #[name = "nav_advanced"]
                gtk4::Button {
                    set_label: "高级",
                    set_halign: gtk4::Align::Start,
                    add_css_class: "flat",
                },

                #[name = "nav_logs"]
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

                        // 启动设置组
                        adw::PreferencesGroup {
                            set_title: Some("启动"),

                            adw::ActionRow {
                                set_title: Some("开机自启"),
                                set_subtitle: Some("系统启动时自动运行"),

                                add_suffix = &gtk4::Switch {
                                    set_valign: gtk4::Align::Center,
                                },
                            },
                        },

                        // 性能设置组
                        adw::PreferencesGroup {
                            set_title: Some("性能"),

                            adw::ActionRow {
                                set_title: Some("FPS 限制"),
                                set_subtitle: Some("建议 30 或 60"),

                                #[wrap(Some)]
                                add_prefix = &gtk4::SpinButton::with_range(1.0, 144.0, 1.0),
                            },

                            adw::ActionRow {
                                set_title: Some("缩放模式"),

                                #[wrap(Some)]
                                add_suffix = &gtk4::DropDown::from_strings(&[
                                    "默认",
                                    "拉伸",
                                    "适应",
                                    "填充",
                                ]),
                            },
                        },

                        // 音频设置组
                        adw::PreferencesGroup {
                            set_title: Some("音频"),

                            adw::ActionRow {
                                set_title: Some("静音"),
                                set_subtitle: Some("禁用壁纸音频"),

                                add_suffix = &gtk4::Switch {
                                    set_valign: gtk4::Align::Center,
                                },
                            },

                            adw::ActionRow {
                                set_title: Some("音量"),
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

                        // 路径设置组
                        adw::PreferencesGroup {
                            set_title: Some("路径"),

                            adw::ActionRow {
                                set_title: Some("工作室路径"),

                                add_suffix = &gtk4::Button {
                                    set_icon_name: Some("document-open-symbolic"),
                                },

                                #[name = "workshop_path_label"]
                                add_prefix = &gtk4::Label::new(Some("未设置")),
                            },

                            adw::ActionRow {
                                set_title: Some("资源路径"),

                                add_suffix = &gtk4::Button {
                                    set_icon_name: Some("document-open-symbolic"),
                                },

                                #[name = "assets_path_label"]
                                add_prefix = &gtk4::Label::new(Some("未设置")),
                            },
                        },

                        gtk4::Box {
                            set_vexpand: true,
                        },

                        // 管理昵称按钮
                        gtk4::Button {
                            set_label: "管理昵称",
                            set_halign: gtk4::Align::End,
                            add_css_class: "pill",
                        },
                    },
                } => {
                    set_name: "general",
                },

                // Audio 子页面（占位）
                add_named: &gtk4::Label::new(Some("音频设置（待实现）")) => {
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

    fn update(&mut self, msg: Self::Input, sender: ComponentSender<Self>, widgets: &mut Self::Widgets) {
        match msg {
            SettingsPageInput::NavigateTo(section) => {
                self.current_section = section.clone();
                widgets.content_stack.set_visible_child_name(&section);
            }
            SettingsPageInput::FpsChanged(fps) => {
                sender.output(SettingsPageOutput::ConfigChanged(
                    "fps".to_string(),
                    serde_json::json!(fps),
                )).ok();
            }
            SettingsPageInput::VolumeChanged(volume) => {
                sender.output(SettingsPageOutput::ConfigChanged(
                    "volume".to_string(),
                    serde_json::json!(volume),
                )).ok();
            }
            SettingsPageInput::SilenceToggled(silence) => {
                sender.output(SettingsPageOutput::ConfigChanged(
                    "silence".to_string(),
                    serde_json::json!(silence),
                )).ok();
            }
            SettingsPageInput::AutoStartToggled(auto_start) => {
                sender.output(SettingsPageOutput::ConfigChanged(
                    "auto_start".to_string(),
                    serde_json::json!(auto_start),
                )).ok();
            }
            SettingsPageInput::WorkshopPathSelected(path) => {
                widgets.workshop_path_label.set_text(&path);
                sender.output(SettingsPageOutput::PathSelected(
                    "workshop".to_string(),
                    path,
                )).ok();
            }
            SettingsPageInput::AssetsPathSelected(path) => {
                widgets.assets_path_label.set_text(&path);
                sender.output(SettingsPageOutput::PathSelected(
                    "assets".to_string(),
                    path,
                )).ok();
            }
            SettingsPageInput::ManageNicknames => {
                sender.output(SettingsPageOutput::OpenNicknameManager).ok();
            }
        }
    }
}
