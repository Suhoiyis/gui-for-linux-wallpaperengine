//! 性能监控页面 - 实时数据显示

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

                // 总览卡片
                gtk4::Box {
                    set_orientation: gtk4::Orientation::Horizontal,
                    set_spacing: 16,

                    // CPU 卡片
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
                            set_label: &format!("{:.1}%", model.cpu_usage),
                            add_css_class: "title-2",
                        },
                    },

                    // 内存卡片
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
                            set_label: &format!("{:.0} MB", model.memory_usage),
                            add_css_class: "title-2",
                        },
                    },
                },

                gtk4::Separator {},

                // 进程详情
                gtk4::Box {
                    set_orientation: gtk4::Orientation::Vertical,
                    set_spacing: 12,

                    gtk4::Label {
                        set_label: "进程详情",
                        add_css_class: "title-2",
                        set_halign: gtk4::Align::Start,
                    },

                    gtk4::Box {
                        set_orientation: gtk4::Orientation::Vertical,
                        set_spacing: 8,

                        gtk4::Label {
                            set_label: "Frontend: 运行中 ✓",
                            add_css_class: "success",
                        },

                        gtk4::Label {
                            set_label: "Backend: 待接入",
                            add_css_class: "dim-label",
                        },

                        gtk4::Label {
                            set_label: "Tray: 待接入",
                            add_css_class: "dim-label",
                        },
                    },
                },

                gtk4::Separator {},

                // 火花线图表（占位）
                gtk4::Box {
                    set_orientation: gtk4::Orientation::Vertical,
                    set_spacing: 12,

                    gtk4::Label {
                        set_label: "CPU 历史（火花线图表待实现）",
                        add_css_class: "title-2",
                        set_halign: gtk4::Align::Start,
                    },

                    gtk4::Box {
                        set_height_request: 60,
                        add_css_class: "card",
                        
                        gtk4::Label {
                            set_label: "📈 实时数据更新中...",
                            add_css_class: "dim-label",
                            set_halign: gtk4::Align::Center,
                            set_valign: gtk4::Align::Center,
                        },
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
