use gtk4::prelude::*;
use relm4::prelude::*;

pub struct ListView {
    selected_id: Option<String>,
}

#[derive(Debug)]
pub enum ListViewInput {
    ItemSelected(String),
    ItemActivated(String),
}

#[derive(Debug)]
pub enum ListViewOutput {
    Selected(String),
    Activated(String),
}

#[relm4::component(pub)]
impl Component for ListView {
    type Init = ();
    type Input = ListViewInput;
    type Output = ListViewOutput;
    type CommandOutput = ();

    view! {
        gtk4::ScrolledWindow {
            set_hexpand: true,
            set_vexpand: true,

            #[name = "list_box"]
            gtk4::ListBox {
                set_hexpand: true,
                set_vexpand: true,
                set_selection_mode: gtk4::SelectionMode::Single,
                add_css_class: "rich-list",

                // 示例列表项
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
                                set_label: "示例壁纸 1",
                                set_halign: gtk4::Align::Start,
                                add_css_class: "heading",
                            },

                            gtk4::Label {
                                set_label: "Video • 15MB",
                                set_halign: gtk4::Align::Start,
                                add_css_class: "dim-label",
                            },
                        },

                        gtk4::Label {
                            set_label: "#1",
                            add_css_class: "dim-label",
                        },
                    },
                },

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
                                set_label: "示例壁纸 2",
                                set_halign: gtk4::Align::Start,
                                add_css_class: "heading",
                            },

                            gtk4::Label {
                                set_label: "Scene • 23MB",
                                set_halign: gtk4::Align::Start,
                                add_css_class: "dim-label",
                            },
                        },

                        gtk4::Label {
                            set_label: "#2",
                            add_css_class: "dim-label",
                        },
                    },
                },

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
                                set_label: "示例壁纸 3",
                                set_halign: gtk4::Align::Start,
                                add_css_class: "heading",
                            },

                            gtk4::Label {
                                set_label: "Web • 8MB",
                                set_halign: gtk4::Align::Start,
                                add_css_class: "dim-label",
                            },
                        },

                        gtk4::Label {
                            set_label: "#3",
                            add_css_class: "dim-label",
                        },
                    },
                },

                connect_row_activated[sender] => move |_, row| {
                    let index = row.index();
                    sender.input(ListViewInput::ItemActivated(index.to_string()));
                },

                connect_selected_rows_changed[sender] => move |listbox| {
                    if let Some(row) = listbox.selected_row() {
                        let index = row.index();
                        sender.input(ListViewInput::ItemSelected(index.to_string()));
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
        let model = Self { selected_id: None };

        let widgets = view_output!();

        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            ListViewInput::ItemSelected(id) => {
                self.selected_id = Some(id.clone());
                sender.output(ListViewOutput::Selected(id)).ok();
            }
            ListViewInput::ItemActivated(id) => {
                sender.output(ListViewOutput::Activated(id)).ok();
            }
        }
    }
}
