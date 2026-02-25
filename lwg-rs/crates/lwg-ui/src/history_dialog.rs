use gtk4::prelude::*;
use relm4::prelude::*;
use libadwaita::{self, prelude::*};

/// 播放历史对话框
pub struct HistoryDialog {
    history_count: usize,
}

#[derive(Debug, Clone)]
pub struct HistoryItem {
    pub id: String,
    pub title: String,
    pub timestamp: String,
    pub thumbnail: Option<String>,
}

#[derive(Debug)]
pub enum HistoryDialogInput {
    Show,
    Hide,
    Replay(String),
    Clear,
}

#[derive(Debug)]
pub enum HistoryDialogOutput {
    ReplayRequested(String),
    HistoryCleared,
}

#[relm4::component(pub)]
impl Component for HistoryDialog {
    type Init = ();
    type Input = HistoryDialogInput;
    type Output = HistoryDialogOutput;
    type CommandOutput = ();

    view! {
        #[local_ref]
        dialog -> adw::Dialog {
            set_title: Some("Playback History"),
            set_content_width: 600,
            set_content_height: 500,

            gtk4::Box {
                set_orientation: gtk4::Orientation::Vertical,
                set_spacing: 12,
                set_margin_all: 12,

                // 标题和容量显示
                gtk4::Box {
                    set_orientation: gtk4::Orientation::Horizontal,
                    set_spacing: 6,

                    gtk4::Label {
                        set_label: "播放历史",
                        add_css_class: "title-2",
                    },

                    gtk4::Label {
                        set_label: "(0/30)",
                        add_css_class: "dim-label",
                    },

                    gtk4::Box {
                        set_hexpand: true,
                    },

                    gtk4::Button {
                        set_label: "清空历史",
                        add_css_class: "destructive-action",
                    },
                },

                gtk4::Separator {},

                // 历史列表
                gtk4::ScrolledWindow {
                    set_vexpand: true,

                    gtk4::ListBox {
                        add_css_class: "rich-list",

                        // 示例项
                        gtk4::ListBoxRow {
                            gtk4::Box {
                                set_orientation: gtk4::Orientation::Horizontal,
                                set_spacing: 12,
                                set_margin_all: 12,

                                gtk4::Image {
                                    set_icon_name: Some("image-x-generic-symbolic"),
                                    set_pixel_size: 48,
                                },

                                gtk4::Box {
                                    set_orientation: gtk4::Orientation::Vertical,
                                    set_spacing: 4,
                                    set_hexpand: true,

                                    gtk4::Label {
                                        set_label: "示例壁纸",
                                        add_css_class: "heading",
                                        set_halign: gtk4::Align::Start,
                                    },

                                    gtk4::Label {
                                        set_label: "2024-01-01 12:00",
                                        add_css_class: "dim-label",
                                        set_halign: gtk4::Align::Start,
                                    },
                                },

                                gtk4::Button {
                                    set_icon_name: "media-playback-start-symbolic",
                                    set_tooltip_text: Some("回放"),
                                },
                            },
                        },
                    },
                },

                gtk4::Separator {},

                // 底部按钮
                gtk4::Box {
                    set_orientation: gtk4::Orientation::Horizontal,
                    set_spacing: 6,

                    gtk4::Box {
                        set_hexpand: true,
                    },

                    gtk4::Button {
                        set_label: "关闭",
                        add_css_class: "pill",
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
            history_count: 0,
        };

        let dialog = adw::Dialog::new();
        let widgets = view_output!();

        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            HistoryDialogInput::Show => {
                // 显示对话框
            }
            HistoryDialogInput::Hide => {
                // 隐藏对话框
            }
            HistoryDialogInput::Replay(id) => {
                sender.output(HistoryDialogOutput::ReplayRequested(id)).ok();
            }
            HistoryDialogInput::Clear => {
                self.history_count = 0;
                sender.output(HistoryDialogOutput::HistoryCleared).ok();
            }
        }
    }
}
