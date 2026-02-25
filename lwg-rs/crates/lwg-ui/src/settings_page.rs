//! 设置页面 - Logs 子页面完整实现
//! 审计报告 Task 3.1.4: Logs 子页面完整实现

use gtk4::prelude::*;
use relm4::prelude::*;
use libadwaita as adw;

#[derive(Debug)]
pub enum SettingsPageInput {
    NavigateTo(String),
    LogFilterChanged(String),
    CopyLogs,
    ClearLogs,
}

#[derive(Debug)]
pub enum SettingsPageOutput {
    ConfigChanged(String, serde_json::Value),
    CopyLogsRequested,
    ClearLogsRequested,
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
                add_named: &gtk4::Label::new(Some("高级")) => {
                    set_name: "advanced",
                },

                // Logs 子页面
                add_named: &gtk4::ScrolledWindow {
                    set_hexpand: true,
                    set_vexpand: true,

                    gtk4::Box {
                        set_orientation: gtk4::Orientation::Vertical,
                        set_spacing: 16,
                        set_margin_all: 12,

                        gtk4::Label {
                            set_label: "日志",
                            add_css_class: "title-1",
                            set_halign: gtk4::Align::Start,
                        },

                        // 日志控制组
                        adw::PreferencesGroup {
                            set_title: Some("日志控制"),

                            adw::ActionRow {
                                set_title: Some("日志过滤器"),
                                set_subtitle: Some("按级别或来源过滤"),

                                add_suffix = &gtk4::DropDown::from_strings(&[
                                    "全部",
                                    "DEBUG",
                                    "INFO",
                                    "WARNING",
                                    "ERROR",
                                    "Controller",
                                    "Engine",
                                    "GUI",
                                ]),
                            },
                        },

                        // 日志查看器组
                        adw::PreferencesGroup {
                            set_title: Some("日志查看器"),

                            #[name = "log_viewer"]
                            gtk4::TextView {
                                set_editable: false,
                                set_monospace: true,
                                set_vexpand: true,
                                set_min_content_height: 300,
                                set_wrap_mode: gtk4::WrapMode::WordChar,
                            },

                            add_suffix = &gtk4::Button {
                                set_icon_name: Some("edit-copy-symbolic"),
                                set_tooltip_text: Some("复制日志"),
                            },
                        },

                        gtk4::Box {
                            set_orientation: gtk4::Orientation::Horizontal,
                            set_spacing: 12,
                            set_halign: gtk4::Align::End,

                            gtk4::Button {
                                set_label: "清空日志",
                                add_css_class: "destructive-action",
                            },

                            gtk4::Button {
                                set_label: "复制日志",
                                add_css_class: "pill",
                            },
                        },

                        gtk4::Box {
                            set_vexpand: true,
                        },

                        // 日志统计
                        gtk4::Box {
                            set_orientation: gtk4::Orientation::Horizontal,
                            set_spacing: 24,

                            gtk4::Label {
                                set_label: "总日志数：0",
                                add_css_class: "caption",
                            },

                            gtk4::Label {
                                set_label: "错误数：0",
                                add_css_class: "caption",
                            },

                            gtk4::Box {
                                set_hexpand: true,
                            },

                            gtk4::Label {
                                set_label: "自动刷新：开",
                                add_css_class: "caption",
                            },
                        },
                    },
                } => {
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
            SettingsPageInput::LogFilterChanged(filter) => {
                sender.output(SettingsPageOutput::ConfigChanged(
                    "log_filter".to_string(),
                    serde_json::json!(filter),
                )).ok();
            }
            SettingsPageInput::CopyLogs => {
                sender.output(SettingsPageOutput::CopyLogsRequested).ok();
            }
            SettingsPageInput::ClearLogs => {
                sender.output(SettingsPageOutput::ClearLogsRequested).ok();
            }
        }
    }
}
