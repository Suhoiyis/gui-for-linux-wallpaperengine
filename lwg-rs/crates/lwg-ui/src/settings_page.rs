use gtk4::prelude::*;
use relm4::prelude::*;

pub struct SettingsPage {
    current_section: SettingsSection,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum SettingsSection {
    General,
    Audio,
    Advanced,
    Logs,
}

impl SettingsSection {
    fn name(&self) -> &'static str {
        match self {
            SettingsSection::General => "通用",
            SettingsSection::Audio => "音频",
            SettingsSection::Advanced => "高级",
            SettingsSection::Logs => "日志",
        }
    }
    
    fn as_str(&self) -> &'static str {
        match self {
            SettingsSection::General => "general",
            SettingsSection::Audio => "audio",
            SettingsSection::Advanced => "advanced",
            SettingsSection::Logs => "logs",
        }
    }
}

#[derive(Debug)]
pub enum SettingsPageInput {
    NavigateTo(SettingsSection),
}

#[derive(Debug)]
pub enum SettingsPageOutput {}

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
                    add_css_class: "title-1",
                    set_halign: gtk4::Align::Start,
                    set_margin_bottom: 12,
                },

                gtk4::ListBox {
                    set_selection_mode: gtk4::SelectionMode::Single,

                    gtk4::ListBoxRow {
                        gtk4::Box {
                            set_orientation: gtk4::Orientation::Horizontal,
                            set_spacing: 12,
                            set_margin_all: 12,

                            gtk4::Image {
                                set_icon_name: Some("preferences-system-symbolic"),
                            },

                            gtk4::Label {
                                set_label: "通用",
                            },
                        },
                    },

                    gtk4::ListBoxRow {
                        gtk4::Box {
                            set_orientation: gtk4::Orientation::Horizontal,
                            set_spacing: 12,
                            set_margin_all: 12,

                            gtk4::Image {
                                set_icon_name: Some("audio-volume-high-symbolic"),
                            },

                            gtk4::Label {
                                set_label: "音频",
                            },
                        },
                    },

                    gtk4::ListBoxRow {
                        gtk4::Box {
                            set_orientation: gtk4::Orientation::Horizontal,
                            set_spacing: 12,
                            set_margin_all: 12,

                            gtk4::Image {
                                set_icon_name: Some("preferences-system-symbolic"),
                            },

                            gtk4::Label {
                                set_label: "高级",
                            },
                        },
                    },

                    gtk4::ListBoxRow {
                        gtk4::Box {
                            set_orientation: gtk4::Orientation::Horizontal,
                            set_spacing: 12,
                            set_margin_all: 12,

                            gtk4::Image {
                                set_icon_name: Some("text-x-generic-symbolic"),
                            },

                            gtk4::Label {
                                set_label: "日志",
                            },
                        },
                    },

                    connect_row_selected[sender] => move |_, row| {
                        if let Some(row) = row {
                            let section = match row.index() {
                                0 => SettingsSection::General,
                                1 => SettingsSection::Audio,
                                2 => SettingsSection::Advanced,
                                _ => SettingsSection::Logs,
                            };
                            sender.input(SettingsPageInput::NavigateTo(section));
                        }
                    },
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
                set_transition_type: gtk4::StackTransitionType::Crossfade,

                // 通用设置
                add_child: &gtk4::Box {
                    set_orientation: gtk4::Orientation::Vertical,
                    set_spacing: 16,

                    gtk4::Label {
                        set_label: "通用设置",
                        add_css_class: "title-2",
                        set_halign: gtk4::Align::Start,
                    },

                    gtk4::Box {
                        set_orientation: gtk4::Orientation::Horizontal,
                        set_spacing: 12,

                        gtk4::Label {
                            set_label: "开机自启",
                            set_hexpand: true,
                        },

                        gtk4::Switch {
                            set_valign: gtk4::Align::Center,
                        },
                    },

                    gtk4::Box {
                        set_orientation: gtk4::Orientation::Horizontal,
                        set_spacing: 12,

                        gtk4::Label {
                            set_label: "最小化到托盘",
                            set_hexpand: true,
                        },

                        gtk4::Switch {
                            set_valign: gtk4::Align::Center,
                            set_active: true,
                        },
                    },

                    gtk4::Label {
                        set_label: "Steam Workshop 路径:",
                        set_halign: gtk4::Align::Start,
                    },

                    gtk4::Entry {
                        set_placeholder_text: Some("/path/to/workshop")],
                    },
                } -> {
                    set_name: "general",
                },

                // 音频设置
                add_child: &gtk4::Box {
                    set_orientation: gtk4::Orientation::Vertical,
                    set_spacing: 16,

                    gtk4::Label {
                        set_label: "音频设置",
                        add_css_class: "title-2",
                        set_halign: gtk4::Align::Start,
                    },

                    gtk4::Box {
                        set_orientation: gtk4::Orientation::Horizontal,
                        set_spacing: 12,

                        gtk4::Label {
                            set_label: "默认音量 (0-100):",
                            set_hexpand: true,
                        },

                        gtk4::SpinButton {
                            set_range: (0.0, 100.0),
                            set_value: 50.0,
                        },
                    },
                } -> {
                    set_name: "audio",
                },

                // 高级设置
                add_child: &gtk4::Box {
                    set_orientation: gtk4::Orientation::Vertical,
                    set_spacing: 16,

                    gtk4::Label {
                        set_label: "高级设置",
                        add_css_class: "title-2",
                        set_halign: gtk4::Align::Start,
                    },

                    gtk4::Box {
                        set_orientation: gtk4::Orientation::Horizontal,
                        set_spacing: 12,

                        gtk4::Label {
                            set_label: "FPS 限制:",
                            set_hexpand: true,
                        },

                        gtk4::SpinButton {
                            set_range: (15.0, 240.0),
                            set_value: 60.0,
                        },
                    },
                } -> {
                    set_name: "advanced",
                },

                // 日志
                add_child: &gtk4::Box {
                    set_orientation: gtk4::Orientation::Vertical,
                    set_spacing: 16,

                    gtk4::Label {
                        set_label: "日志",
                        add_css_class: "title-2",
                        set_halign: gtk4::Align::Start,
                    },

                    gtk4::TextView {
                        set_editable: false,
                        set_monospace: true,
                    },
                } -> {
                    set_name: "logs",
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
            current_section: SettingsSection::General,
        };

        let widgets = view_output!();

        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, _sender: ComponentSender<Self>, widgets: &mut Self::Widgets) {
        match msg {
            SettingsPageInput::NavigateTo(section) => {
                if self.current_section != section {
                    self.current_section = section;
                    widgets.content_stack.set_visible_child_name(section.as_str());
                }
            }
        }
    }
}
