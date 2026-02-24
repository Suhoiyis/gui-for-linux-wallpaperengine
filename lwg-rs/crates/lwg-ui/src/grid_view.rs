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
            set_hscrollbar_policy: gtk4::PolicyType::Never,

            #[name = "flow_box"]
            gtk4::FlowBox {
                set_hexpand: true,
                set_vexpand: true,
                set_max_children_per_line: 4,
                set_min_children_per_line: 2,
                set_column_spacing: 12,
                set_row_spacing: 12,
                set_margin_all: 12,
                set_selection_mode: gtk4::SelectionMode::Single,

                gtk4::FlowBoxChild {
                    gtk4::Box {
                        set_orientation: gtk4::Orientation::Vertical,
                        set_spacing: 8,
                        set_width_request: 200,
                        set_height_request: 150,
                        add_css_class: "card",

                        gtk4::Box {
                            set_vexpand: true,
                            set_height_request: 100,

                            gtk4::Image {
                                set_icon_name: Some("image-x-generic-symbolic"),
                                set_pixel_size: 64,
                                set_vexpand: true,
                                set_valign: gtk4::Align::Center,
                                set_halign: gtk4::Align::Center,
                            },
                        },

                        gtk4::Label {
                            set_label: "示例壁纸 1",
                            set_max_width_chars: 20,
                            set_ellipsize: gtk4::pango::EllipsizeMode::End,
                            set_halign: gtk4::Align::Center,
                        },
                    },
                },

                gtk4::FlowBoxChild {
                    gtk4::Box {
                        set_orientation: gtk4::Orientation::Vertical,
                        set_spacing: 8,
                        set_width_request: 200,
                        set_height_request: 150,
                        add_css_class: "card",

                        gtk4::Box {
                            set_vexpand: true,
                            set_height_request: 100,

                            gtk4::Image {
                                set_icon_name: Some("image-x-generic-symbolic"),
                                set_pixel_size: 64,
                                set_vexpand: true,
                                set_valign: gtk4::Align::Center,
                                set_halign: gtk4::Align::Center,
                            },
                        },

                        gtk4::Label {
                            set_label: "示例壁纸 2",
                            set_max_width_chars: 20,
                            set_ellipsize: gtk4::pango::EllipsizeMode::End,
                            set_halign: gtk4::Align::Center,
                        },
                    },
                },

                gtk4::FlowBoxChild {
                    gtk4::Box {
                        set_orientation: gtk4::Orientation::Vertical,
                        set_spacing: 8,
                        set_width_request: 200,
                        set_height_request: 150,
                        add_css_class: "card",

                        gtk4::Box {
                            set_vexpand: true,
                            set_height_request: 100,

                            gtk4::Image {
                                set_icon_name: Some("image-x-generic-symbolic"),
                                set_pixel_size: 64,
                                set_vexpand: true,
                                set_valign: gtk4::Align::Center,
                                set_halign: gtk4::Align::Center,
                            },
                        },

                        gtk4::Label {
                            set_label: "示例壁纸 3",
                            set_max_width_chars: 20,
                            set_ellipsize: gtk4::pango::EllipsizeMode::End,
                            set_halign: gtk4::Align::Center,
                        },
                    },
                },

                connect_child_activated(sender) => move |_, child| {
                    let index = child.index();
                    sender.input(GridViewInput::ItemActivated(index.to_string()));
                },

                connect_selected_children_changed(sender) => move |flowbox| {
                    if let Some(child) = flowbox.selected_children().first() {
                        let index = child.index();
                        sender.input(GridViewInput::ItemSelected(index.to_string()));
                    }
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
