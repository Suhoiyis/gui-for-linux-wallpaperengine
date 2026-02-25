//! 火花线图表 - 简化实现

use gtk4::prelude::*;
use relm4::prelude::*;
use std::collections::VecDeque;

const HISTORY_SIZE: usize = 60;

#[derive(Debug)]
pub enum SparklineInput {
    UpdateData(f32),
}

pub struct Sparkline {
    data: VecDeque<f32>,
    color_type: String,
}

#[relm4::component(pub)]
impl Component for Sparkline {
    type Init = String;
    type Input = SparklineInput;
    type Output = ();
    type CommandOutput = ();

    view! {
        gtk4::Box {
            set_orientation: gtk4::Orientation::Vertical,
            set_spacing: 4,

            #[name = "value_label"]
            gtk4::Label {
                set_label: "0%",
                add_css_class: "caption",
                set_halign: gtk4::Align::Center,
            },
        }
    }

    fn init(
        color_type: Self::Init,
        _root: Self::Root,
        _sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        let model = Self {
            data: VecDeque::with_capacity(HISTORY_SIZE),
            color_type,
        };

        let widgets = view_output!();

        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, _sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            SparklineInput::UpdateData(value) => {
                if self.data.len() >= HISTORY_SIZE {
                    self.data.pop_front();
                }
                self.data.push_back(value);
            }
        }
    }
}
