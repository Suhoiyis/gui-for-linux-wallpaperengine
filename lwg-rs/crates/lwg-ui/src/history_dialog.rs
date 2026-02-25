use gtk4::prelude::*;
use libadwaita as adw;
use relm4::prelude::*;

/// 播放历史对话框（简化版）
pub struct HistoryDialog {
    history_count: usize,
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
        gtk4::Window {
            set_title: Some("Playback History"),
            set_default_width: 600,
            set_default_height: 500,
            set_modal: true,

            gtk4::Box {
                set_orientation: gtk4::Orientation::Vertical,
                set_spacing: 12,
                set_margin_all: 12,

                // 标题
                gtk4::Label {
                    set_label: "播放历史",
                    add_css_class: "title-2",
                },

                gtk4::Separator {},

                // 历史列表占位
                gtk4::Label {
                    set_label: "历史功能待实现",
                    add_css_class: "dim-label",
                },

                gtk4::Box {
                    set_vexpand: true,
                },

                // 关闭按钮
                gtk4::Button {
                    set_label: "关闭",
                    set_halign: gtk4::Align::End,
                },
            },
        }
    }

    fn init(
        _init: Self::Init,
        _root: Self::Root,
        _sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        let model = Self { history_count: 0 };
        let widgets = view_output!();
        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, _sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            HistoryDialogInput::Show => {}
            HistoryDialogInput::Hide => {}
            HistoryDialogInput::Replay(_) => {}
            HistoryDialogInput::Clear => {
                self.history_count = 0;
            }
        }
    }
}
