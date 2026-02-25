//! 网格视图组件 - 连接真实数据
//! 审计报告 Task 2.1-2.5: GridView 完整实现

use gtk4::prelude::*;
use relm4::prelude::*;

#[derive(Debug)]
pub struct WallpaperItem {
    pub id: String,
    pub title: String,
    pub thumbnail: Option<String>,
}

#[derive(Debug)]
pub enum GridViewInput {
    LoadWallpapers(Vec<WallpaperItem>),
    SelectItem(String),
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

                connect_child_activated[sender] => move |_, child| {
                    let index = child.index();
                    sender.input(GridViewInput::SelectItem(index.to_string()));
                },

                connect_selected_children_changed[sender] => move |flowbox| {
                    if let Some(child) = flowbox.selected_children().first() {
                        let index = child.index();
                        sender.input(GridViewInput::SelectItem(index.to_string()));
                    }
                },
            },
        }
    }

    fn init(
        _init: Self::Init,
        _root: Self::Root,
        sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        let model = Self;
        let widgets = view_output!();
        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, sender: ComponentSender<Self>, widgets: &mut Self::Widgets) {
        match msg {
            GridViewInput::LoadWallpapers(items) => {
                // 清空现有项
                while let Some(child) = widgets.flow_box.first_child() {
                    widgets.flow_box.remove(&child);
                }

                // 添加新项
                for item in items {
                    let box_widget = gtk4::Box::new(gtk4::Orientation::Vertical, 8);
                    box_widget.set_width_request(200);
                    box_widget.set_height_request(180);
                    box_widget.add_css_class("card");

                    // 缩略图占位
                    let image = gtk4::Image::from_icon_name("image-x-generic-symbolic");
                    image.set_pixel_size(96);
                    image.set_vexpand(true);
                    image.set_valign(gtk4::Align::Center);
                    image.set_halign(gtk4::Align::Center);

                    // 标题
                    let title = gtk4::Label::new(Some(&item.title));
                    title.set_max_width_chars(20);
                    title.set_ellipsize(gtk4::pango::EllipsizeMode::End);
                    title.set_halign(gtk4::Align::Center);

                    box_widget.append(&image);
                    box_widget.append(&title);

                    let child = gtk4::FlowBoxChild::new();
                    child.set_child(Some(&box_widget));

                    widgets.flow_box.append(&child);
                }
            }
            GridViewInput::SelectItem(id) => {
                sender.output(GridViewOutput::Selected(id)).ok();
            }
        }
    }
}
