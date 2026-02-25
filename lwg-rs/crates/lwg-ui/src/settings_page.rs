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

                    gtk4::ListBoxRow {
                        gtk4::Label {
                            set_label: "通用",
                        },
                    },

                    gtk4::ListBoxRow {
                        gtk4::Label {
                            set_label: "音频",
                        },
                    },

                    gtk4::ListBoxRow {
                        gtk4::Label {
                            set_label: "高级",
                        },
                    },

                    gtk4::ListBoxRow {
                        gtk4::Label {
                            set_label: "日志",
                        },
                    },
                },
            },

            gtk4::Separator {
                set_orientation: gtk4::Orientation::Vertical,
            },

            gtk4::Stack {
                set_hexpand: true,
                set_vexpand: true,
                set_margin_all: 24,

                gtk4::Box {
                    set_orientation: gtk4::Orientation::Vertical,
                    set_spacing: 16,

                    gtk4::Label {
                        set_label: "通用设置",
                        add_css_class: "title-2",
                        set_halign: gtk4::Align::Start,
                    },

                    gtk4::Box { set_orientation: gtk4::Orientation::Horizontal, set_spacing: 12, gtk4::Label { set_label: "开机自启", set_hexpand: true, }, gtk4::Switch {
                        set_label: "开机自启",
                    },
                } => {
                    set_name: "general",
                },

                gtk4::Box {
                    set_orientation: gtk4::Orientation::Vertical,
                    set_spacing: 16,

                    gtk4::Label {
                        set_label: "音频设置",
                        add_css_class: "title-2",
                        set_halign: gtk4::Align::Start,
                    },
                } => {
                    set_name: "audio",
                },

                gtk4::Box {
                    set_orientation: gtk4::Orientation::Vertical,
                    set_spacing: 16,

                    gtk4::Label {
                        set_label: "高级设置",
                        add_css_class: "title-2",
                        set_halign: gtk4::Align::Start,
                    },
                } => {
                    set_name: "advanced",
                },

                gtk4::Box {
                    set_orientation: gtk4::Orientation::Vertical,
                    set_spacing: 16,

                    gtk4::Label {
                        set_label: "日志",
                        add_css_class: "title-2",
                        set_halign: gtk4::Align::Start,
                    },
                } => {
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

    fn update(&mut self, msg: Self::Input, _sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            SettingsPageInput::NavigateTo(section) => {
                if self.current_section != section {
                    self.current_section = section;
                }
            }
        }
    }
}
