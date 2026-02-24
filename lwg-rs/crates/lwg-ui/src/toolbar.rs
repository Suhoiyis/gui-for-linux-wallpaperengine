use gtk4::prelude::*;
use relm4::prelude::*;

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum ViewMode {
    Grid,
    List,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum SortOrder {
    Name,
    Size,
    Type,
    Date,
}

pub struct Toolbar {
    view_mode: ViewMode,
    sort_order: SortOrder,
}

#[derive(Debug)]
pub enum ToolbarInput {
    SetViewMode(ViewMode),
    SetSortOrder(SortOrder),
    SearchChanged(String),
}

#[derive(Debug)]
pub enum ToolbarOutput {
    ViewModeChanged(ViewMode),
    SortOrderChanged(SortOrder),
    SearchChanged(String),
}

#[relm4::component(pub)]
impl Component for Toolbar {
    type Init = ();
    type Input = ToolbarInput;
    type Output = ToolbarOutput;
    type CommandOutput = ();

    view! {
        gtk4::Box {
            set_orientation: gtk4::Orientation::Horizontal,
            set_spacing: 12,
            set_margin_all: 12,

            // 左侧：状态显示
            gtk4::Label {
                set_label: "准备就绪",
                add_css_class: "dim-label",
                set_width_request: 120,
            },

            gtk4::Box {
                set_hexpand: true,
            },

            // 中间：搜索框
            gtk4::SearchEntry {
                set_placeholder_text: Some("搜索壁纸..."),
                set_width_request: 200,
                connect_search_changed[sender] => move |entry| {
                    sender.input(ToolbarInput::SearchChanged(entry.text().to_string()));
                },
            },

            gtk4::Box {
                set_hexpand: true,
            },

            // 右侧：排序下拉
            gtk4::Box {
                set_orientation: gtk4::Orientation::Horizontal,
                set_spacing: 6,

                gtk4::Label {
                    set_label: "排序:",
                    add_css_class: "dim-label",
                },

                #[name = "sort_dropdown"]
                gtk4::DropDown {
                    set_model: Some(&gtk4::StringList::new(&["名称", "大小", "类型", "日期"])),
                    set_selected: 0,
                    connect_selected_notify[sender] => move |dropdown| {
                        let order = match dropdown.selected() {
                            0 => SortOrder::Name,
                            1 => SortOrder::Size,
                            2 => SortOrder::Type,
                            _ => SortOrder::Date,
                        };
                        sender.input(ToolbarInput::SetSortOrder(order));
                    },
                },
            },

            gtk4::Separator {
                set_orientation: gtk4::Orientation::Vertical,
            },

            // 视图切换按钮组
            gtk4::Box {
                set_orientation: gtk4::Orientation::Horizontal,
                set_spacing: 0,

                #[name = "btn_grid"]
                gtk4::ToggleButton {
                    set_icon_name: "view-grid-symbolic",
                    set_tooltip_text: Some("网格视图"),
                    set_active: true,
                    add_css_class: "flat",
                },

                #[name = "btn_list"]
                gtk4::ToggleButton {
                    set_icon_name: "view-list-symbolic",
                    set_tooltip_text: Some("列表视图"),
                    add_css_class: "flat",
                    set_group: Some(&btn_grid),
                    connect_toggled[sender] => move |btn| {
                        if btn.is_active() {
                            sender.input(ToolbarInput::SetViewMode(ViewMode::List));
                        }
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
            view_mode: ViewMode::Grid,
            sort_order: SortOrder::Name,
        };

        let widgets = view_output!();

        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            ToolbarInput::SetViewMode(mode) => {
                if self.view_mode != mode {
                    self.view_mode = mode;
                    sender.output(ToolbarOutput::ViewModeChanged(mode)).ok();
                }
            }
            ToolbarInput::SetSortOrder(order) => {
                if self.sort_order != order {
                    self.sort_order = order;
                    sender.output(ToolbarOutput::SortOrderChanged(order)).ok();
                }
            }
            ToolbarInput::SearchChanged(text) => {
                sender.output(ToolbarOutput::SearchChanged(text)).ok();
            }
        }
    }
}
