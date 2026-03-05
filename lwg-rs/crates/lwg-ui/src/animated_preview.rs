use gtk4::prelude::*;
use relm4::prelude::*;

/// 动态预览组件（GIF/WebP 动画）
pub struct AnimatedPreview {
    playing: bool,
    current_file: Option<String>,
}

#[derive(Debug)]
pub enum AnimatedPreviewInput {
    Play,
    Pause,
    LoadFile(String),
}

#[relm4::component(pub)]
impl Component for AnimatedPreview {
    type Init = ();
    type Input = AnimatedPreviewInput;
    type Output = ();
    type CommandOutput = ();

    view! {
        gtk4::Box {
            set_orientation: gtk4::Orientation::Vertical,
            set_spacing: 8,

            gtk4::Image {
                set_icon_name: Some("image-x-generic-symbolic"),
                set_pixel_size: 128,
                set_vexpand: true,
                set_valign: gtk4::Align::Center,
                set_halign: gtk4::Align::Center,
            },

            gtk4::Label {
                set_label: "预览",
                add_css_class: "dim-label",
            },
        }
    }

    fn init(
        _init: Self::Init,
        _root: Self::Root,
        _sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        let model = Self {
            playing: false,
            current_file: None,
        };
        let widgets = view_output!();
        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, _sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            AnimatedPreviewInput::Play => {
                self.playing = true;
            }
            AnimatedPreviewInput::Pause => {
                self.playing = false;
            }
            AnimatedPreviewInput::LoadFile(path) => {
                self.current_file = Some(path);
            }
        }
    }
}
