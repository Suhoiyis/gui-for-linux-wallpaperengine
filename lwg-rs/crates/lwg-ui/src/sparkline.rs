use gtk4::prelude::*;
use relm4::prelude::*;

/// 火花线图表组件（简化实现）
pub struct Sparkline {
    value: f32,
}

#[derive(Debug)]
pub enum SparklineInput {
    UpdateData(f32),
}

#[relm4::component(pub)]
impl Component for Sparkline {
    type Init = ();
    type Input = SparklineInput;
    type Output = ();
    type CommandOutput = ();

    view! {
        gtk4::Box {
            set_orientation: gtk4::Orientation::Horizontal,
            set_spacing: 4,

            gtk4::Label {
                set_label: "CPU:",
                add_css_class: "dim-label",
            },

            gtk4::Label {
                set_label: "0%",
                set_width_request: 50,
            },

            gtk4::ProgressBar {
                set_fraction: 0.0,
                set_width_request: 150,
                set_valign: gtk4::Align::Center,
            },
        }
    }

    fn init(
        _init: Self::Init,
        _root: Self::Root,
        _sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        let model = Self { value: 0.0 };
        let widgets = view_output!();
        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, _sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            SparklineInput::UpdateData(value) => {
                self.value = value;
                // 简化实现：只更新数据，UI 通过 watch 机制更新
            }
        }
    }
}
