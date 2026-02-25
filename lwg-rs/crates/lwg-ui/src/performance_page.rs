use gtk4::prelude::*;
use relm4::prelude::*;

pub struct PerformancePage {
    cpu_usage: f32,
    memory_usage: f32,
}

#[derive(Debug)]
pub enum PerformancePageInput {
    UpdateStats(f32, f32),
}

#[derive(Debug)]
pub enum PerformancePageOutput {}

#[relm4::component(pub)]
impl Component for PerformancePage {
    type Init = ();
    type Input = PerformancePageInput;
    type Output = PerformancePageOutput;
    type CommandOutput = ();

    view! {
        gtk4::ScrolledWindow {
            set_hexpand: true,
            set_vexpand: true,

            gtk4::Box {
                set_orientation: gtk4::Orientation::Vertical,
                set_spacing: 24,
                set_margin_all: 24,

                gtk4::Label {
                    set_label: "性能监控",
                    add_css_class: "title-1",
                    set_halign: gtk4::Align::Start,
                },

                gtk4::Box {
                    set_orientation: gtk4::Orientation::Horizontal,
                    set_spacing: 16,

                    gtk4::Box {
                        set_orientation: gtk4::Orientation::Vertical,
                        set_spacing: 8,
                        add_css_class: "card",
                        set_margin_all: 12,

                        gtk4::Label {
                            set_label: "CPU",
                            add_css_class: "heading",
                        },

                        gtk4::Label {
                            set_label: "0%",
                            add_css_class: "title-1",
                        },
                    },

                    gtk4::Box {
                        set_orientation: gtk4::Orientation::Vertical,
                        set_spacing: 8,
                        add_css_class: "card",
                        set_margin_all: 12,

                        gtk4::Label {
                            set_label: "内存",
                            add_css_class: "heading",
                        },

                        gtk4::Label {
                            set_label: "0 MB",
                            add_css_class: "title-1",
                        },
                    },
                },

                gtk4::Label {
                    set_label: "进程信息",
                    add_css_class: "title-2",
                    set_halign: gtk4::Align::Start,
                },

                gtk4::ListBox {
                    gtk4::ListBoxRow {
                        gtk4::Label {
                            set_label: "linux-wallpaperengine",
                        },
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
            cpu_usage: 0.0,
            memory_usage: 0.0,
        };

        let widgets = view_output!();

        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, _sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            PerformancePageInput::UpdateStats(cpu, memory) => {
                self.cpu_usage = cpu;
                self.memory_usage = memory;
            }
        }
    }
}
