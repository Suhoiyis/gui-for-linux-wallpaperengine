use gtk4::prelude::*;
use relm4::prelude::*;

pub struct GridView {
    selected_id: Option<String>,
}

#[derive(Debug)]
pub enum GridViewInput {
    ItemSelected(String),
    ItemActivated(String),
}

#[derive(Debug)]
pub enum GridViewOutput {
    Selected(String),
    Activated(String),
}

#[relm4::component(pub)]
impl Component for GridView {
    type Init = ();
    type Input = GridViewInput;
    type Output = GridViewOutput;
    type CommandOutput = ();

    view! {
        gtk4::ScrolledWindow {
            set_hexpand: true,
            set_vexpand: true,

            gtk4::ListBox {
                set_selection_mode: gtk4::SelectionMode::Single,

                gtk4::ListBoxRow {
                    gtk4::Box {
                        set_orientation: gtk4::Orientation::Vertical,
                        set_spacing: 8,
                        set_width_request: 200,
                        set_height_request: 150,
                        add_css_class: "card",

                        gtk4::Image {
                            set_icon_name: Some("image-x-generic-symbolic"),
                            set_pixel_size: 64,
                            set_vexpand: true,
                            set_valign: gtk4::Align::Center,
                            set_halign: gtk4::Align::Center,
                        },

                        gtk4::Label {
                            set_label: "示例壁纸",
                            set_max_width_chars: 20,
                            set_ellipsize: gtk4::pango::EllipsizeMode::End,
                            set_halign: gtk4::Align::Center,
                        },
                    },
                },

                connect_row_selected[sender] => move |_, row| {
                    if let Some(row) = row {
                        sender.input(GridViewInput::ItemSelected(row.index().to_string()));
                    }
                },

                connect_row_activated[sender] => move |_, row| {
                    sender.input(GridViewInput::ItemActivated(row.index().to_string()));
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
            selected_id: None,
        };

        let widgets = view_output!();

        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            GridViewInput::ItemSelected(id) => {
                self.selected_id = Some(id.clone());
                sender.output(GridViewOutput::Selected(id)).ok();
            }
            GridViewInput::ItemActivated(id) => {
                sender.output(GridViewOutput::Activated(id)).ok();
            }
        }
    }
}
