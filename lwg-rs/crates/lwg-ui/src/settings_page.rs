//! 设置页面 - 简化可编译版

use gtk4::prelude::*;
use relm4::prelude::*;

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
pub enum SettingsPageOutput {
    ConfigChanged(String, serde_json::Value),
    PathSelected(String, String),
    OpenNicknameManager,
}

pub struct SettingsPage {
    current_section: SettingsSection,
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
                },

                gtk4::Button {
                    set_label: "音频",
                },

                gtk4::Button {
                    set_label: "高级",
                },

                gtk4::Button {
                    set_label: "日志",
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
            },
        }
    }

    fn init(
        _init: Self::Init,
        _root: Self::Root,
        _sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        let model = Self {
            current_section: SettingsSection::General,
        };

        let widgets = view_output!();

        // 动态添加页面
        let general = gtk4::Label::new(Some("通用设置（待完善）"));
        widgets.content_stack.add_named(&general, Some("general"));

        let audio = gtk4::Label::new(Some("音频设置（待完善）"));
        widgets.content_stack.add_named(&audio, Some("audio"));

        let advanced = gtk4::Label::new(Some("高级设置（待完善）"));
        widgets.content_stack.add_named(&advanced, Some("advanced"));

        let logs = gtk4::Label::new(Some("日志（待完善）"));
        widgets.content_stack.add_named(&logs, Some("logs"));

        widgets.content_stack.set_visible_child(&general);

        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, _sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            SettingsPageInput::NavigateTo(section) => {
                self.current_section = section;
            }
        }
    }
}
