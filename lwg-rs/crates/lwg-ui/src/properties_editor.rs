use gtk4::prelude::*;
use relm4::prelude::*;

/// 属性编辑器组件（最简版）
pub struct PropertiesEditor {
    visible: bool,
}

#[derive(Debug)]
pub enum PropertiesEditorInput {
    Show,
    Hide,
}

#[derive(Debug)]
pub enum PropertiesEditorOutput {
    PropertyChanged(String, String, String),
}

#[relm4::component(pub)]
impl Component for PropertiesEditor {
    type Init = ();
    type Input = PropertiesEditorInput;
    type Output = PropertiesEditorOutput;
    type CommandOutput = ();

    view! {
        gtk4::Box {
            set_orientation: gtk4::Orientation::Vertical,
            set_spacing: 12,
            set_margin_all: 12,

            gtk4::Label {
                set_label: "属性",
                add_css_class: "heading",
                set_halign: gtk4::Align::Start,
            },

            gtk4::Separator {},

            gtk4::Label {
                set_label: "选择 Web 壁纸后显示属性编辑器",
                add_css_class: "dim-label",
                set_halign: gtk4::Align::Center,
            },

            gtk4::Box {
                set_vexpand: true,
            },

            gtk4::Button {
                set_label: "保存",
                set_halign: gtk4::Align::End,
            },
        }
    }

    fn init(
        _init: Self::Init,
        _root: Self::Root,
        _sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        let model = Self { visible: true };
        let widgets = view_output!();
        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, _sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            PropertiesEditorInput::Show => {
                self.visible = true;
            }
            PropertiesEditorInput::Hide => {
                self.visible = false;
            }
        }
    }
}
