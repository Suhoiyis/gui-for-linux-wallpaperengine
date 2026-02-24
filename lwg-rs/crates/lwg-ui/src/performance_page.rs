use gtk4::prelude::*;
use libadwaita::{self, prelude::*};
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

                // 标题
                gtk4::Label {
                    set_label: "性能监控",
                    add_css_class: "title-1",
                    set_halign: gtk4::Align::Start,
                },

                // 资源使用卡片
                libadwaita::PreferencesGroup {
                    set_title: "资源使用",

                    gtk4::Box {
                        set_orientation: gtk4::Orientation::Horizontal,
                        set_spacing: 16,

                        // CPU 使用率
                        gtk4::Box {
                            set_orientation: gtk4::Orientation::Vertical,
                            set_spacing: 8,
                            add_css_class: "card",
                            set_margin_all: 12,
                            set_width_request: 150,

                            gtk4::Label {
                                set_label: "CPU",
                                add_css_class: "heading",
                            },

                            #[name = "cpu_label"]
                            gtk4::Label {
                                set_label: "0%",
                                add_css_class: "title-1",
                            },

                            gtk4::ProgressBar {
                                set_fraction: 0.0,
                                set_width_request: 100,
                            },
                        },

                        // 内存使用
                        gtk4::Box {
                            set_orientation: gtk4::Orientation::Vertical,
                            set_spacing: 8,
                            add_css_class: "card",
                            set_margin_all: 12,
                            set_width_request: 150,

                            gtk4::Label {
                                set_label: "内存",
                                add_css_class: "heading",
                            },

                            #[name = "memory_label"]
                            gtk4::Label {
                                set_label: "0 MB",
                                add_css_class: "title-1",
                            },

                            gtk4::ProgressBar {
                                set_fraction: 0.0,
                                set_width_request: 100,
                            },
                        },

                        // FPS
                        gtk4::Box {
                            set_orientation: gtk4::Orientation::Vertical,
                            set_spacing: 8,
                            add_css_class: "card",
                            set_margin_all: 12,
                            set_width_request: 150,

                            gtk4::Label {
                                set_label: "FPS",
                                add_css_class: "heading",
                            },

                            gtk4::Label {
                                set_label: "60",
                                add_css_class: "title-1",
                            },

                            gtk4::Label {
                                set_label: "目标: 60",
                                add_css_class: "dim-label",
                            },
                        },
                    },
                },

                // 进程信息
                libadwaita::PreferencesGroup {
                    set_title: "进程信息",

                    gtk4::ListBox {
                        add_css_class: "rich-list",

                        gtk4::ListBoxRow {
                            gtk4::Box {
                                set_orientation: gtk4::Orientation::Horizontal,
                                set_spacing: 12,
                                set_margin_all: 12,

                                gtk4::Image {
                                    set_icon_name: Some("application-x-executable-symbolic"),
                                },

                                gtk4::Box {
                                    set_orientation: gtk4::Orientation::Vertical,
                                    set_spacing: 4,
                                    set_hexpand: true,

                                    gtk4::Label {
                                        set_label: "linux-wallpaperengine",
                                        add_css_class: "heading",
                                        set_halign: gtk4::Align::Start,
                                    },

                                    gtk4::Label {
                                        set_label: "PID: 12345",
                                        add_css_class: "dim-label",
                                        set_halign: gtk4::Align::Start,
                                    },
                                },

                                gtk4::Label {
                                    set_label: "运行中",
                                    add_css_class: "accent",
                                },
                            },
                        },

                        gtk4::ListBoxRow {
                            gtk4::Box {
                                set_orientation: gtk4::Orientation::Horizontal,
                                set_spacing: 12,
                                set_margin_all: 12,

                                gtk4::Image {
                                    set_icon_name: Some("application-x-executable-symbolic"),
                                },

                                gtk4::Box {
                                    set_orientation: gtk4::Orientation::Vertical,
                                    set_spacing: 4,
                                    set_hexpand: true,

                                    gtk4::Label {
                                        set_label: "lwg-ui",
                                        add_css_class: "heading",
                                        set_halign: gtk4::Align::Start,
                                    },

                                    gtk4::Label {
                                        set_label: "PID: 12344",
                                        add_css_class: "dim-label",
                                        set_halign: gtk4::Align::Start,
                                    },
                                },

                                gtk4::Label {
                                    set_label: "运行中",
                                    add_css_class: "accent",
                                },
                            },
                        },
                    },
                },

                // 截图历史
                libadwaita::PreferencesGroup {
                    set_title: "截图历史",

                    gtk4::Label {
                        set_label: "暂无截图",
                        add_css_class: "dim-label",
                        set_halign: gtk4::Align::Start,
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

    fn update(
        &mut self,
        msg: Self::Input,
        _sender: ComponentSender<Self>,
        widgets: &mut Self::Widgets,
    ) {
        match msg {
            PerformancePageInput::UpdateStats(cpu, memory) => {
                self.cpu_usage = cpu;
                self.memory_usage = memory;
                widgets.cpu_label.set_label(&format!("{:.1}%", cpu));
                widgets.memory_label.set_label(&format!("{:.0} MB", memory));
            }
        }
    }
}
