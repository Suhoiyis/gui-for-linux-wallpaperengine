use gtk4::prelude::*;
use relm4::prelude::*;

/// 昵称批量管理对话框
pub struct NicknameManagerDialog {
    nickname_count: usize,
}

#[derive(Debug)]
pub enum NicknameManagerDialogInput {
    Show,
    Hide,
    DeleteSelected(Vec<String>),
    EditNickname(String, String),
}

#[derive(Debug)]
pub enum NicknameManagerDialogOutput {
    NicknamesDeleted(Vec<String>),
    NicknameEdited(String, String),
}

#[relm4::component(pub)]
impl Component for NicknameManagerDialog {
    type Init = ();
    type Input = NicknameManagerDialogInput;
    type Output = NicknameManagerDialogOutput;
    type CommandOutput = ();

    view! {
        gtk4::Window {
            set_title: Some("Manage Nicknames"),
            set_default_width: 500,
            set_default_height: 400,
            set_modal: true,

            gtk4::Box {
                set_orientation: gtk4::Orientation::Vertical,
                set_spacing: 12,
                set_margin_all: 12,

                // 标题
                gtk4::Label {
                    set_label: "昵称管理",
                    add_css_class: "title-2",
                },

                gtk4::Separator {},

                // 昵称列表占位
                gtk4::Label {
                    set_label: "昵称管理功能待实现",
                    add_css_class: "dim-label",
                },

                gtk4::Box {
                    set_vexpand: true,
                },

                // 按钮
                gtk4::Box {
                    set_orientation: gtk4::Orientation::Horizontal,
                    set_spacing: 6,

                    gtk4::Box {
                        set_hexpand: true,
                    },

                    gtk4::Button {
                        set_label: "删除选中",
                        add_css_class: "destructive-action",
                    },

                    gtk4::Button {
                        set_label: "关闭",
                    },
                },
            },
        }
    }

    fn init(
        _init: Self::Init,
        _root: Self::Root,
        _sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        let model = Self { nickname_count: 0 };
        let widgets = view_output!();
        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, _sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            NicknameManagerDialogInput::Show => {}
            NicknameManagerDialogInput::Hide => {}
            NicknameManagerDialogInput::DeleteSelected(ids) => {}
            NicknameManagerDialogInput::EditNickname(id, nickname) => {}
        }
    }
}
