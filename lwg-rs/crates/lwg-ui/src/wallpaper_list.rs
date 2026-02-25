use gtk4::prelude::*;
use relm4::prelude::*;
use lwg_core::wallpaper::Wallpaper;

/// 壁纸列表组件
pub struct WallpaperList {
    wallpapers: Vec<Wallpaper>,
    selected_id: Option<String>,
}

#[derive(Debug)]
pub enum WallpaperListInput {
    LoadWallpapers(Vec<Wallpaper>),
    SelectWallpaper(String),
    ScrollTo(String),
}

#[derive(Debug)]
pub enum WallpaperListOutput {
    Selected(String),
    Activated(String),
}

#[relm4::component(pub)]
impl Component for WallpaperList {
    type Init = ();
    type Input = WallpaperListInput;
    type Output = WallpaperListOutput;
    type CommandOutput = ();

    view! {
        gtk4::ScrolledWindow {
            set_hexpand: true,
            set_vexpand: true,

            #[name = "list_box"]
            gtk4::ListBox {
                set_selection_mode: gtk4::SelectionMode::Single,

                connect_row_selected[sender] => move |_, row| {
                    if let Some(row) = row {
                        let index = row.index();
                        sender.input(WallpaperListInput::SelectWallpaper(index.to_string()));
                    }
                },

                connect_row_activated[sender] => move |_, row| {
                    let index = row.index();
                    sender.input(WallpaperListInput::SelectWallpaper(index.to_string()));
                    // TODO: 发送 Activated 信号
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
            wallpapers: Vec::new(),
            selected_id: None,
        };

        let widgets = view_output!();

        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, sender: ComponentSender<Self>, root: &Self::Root) {
        match msg {
            WallpaperListInput::LoadWallpapers(wallpapers) => {
                self.wallpapers = wallpapers;
                self.refresh_list(root);
            }
            WallpaperListInput::SelectWallpaper(id) => {
                self.selected_id = Some(id.clone());
                sender.output(WallpaperListOutput::Selected(id)).ok();
            }
            WallpaperListInput::ScrollTo(id) => {
                // TODO: 滚动到指定壁纸
            }
        }
    }
}

impl WallpaperList {
    /// 刷新列表显示
    fn refresh_list(&self, root: &gtk4::ScrolledWindow) {
        // TODO: 实现完整的列表刷新逻辑
        // 包括：
        // 1. 清空现有列表
        // 2. 根据视图模式（网格/列表）创建不同的项
        // 3. 添加缩略图
        // 4. 添加标题和信息
    }

    /// 创建网格视图项
    fn create_grid_item(&self, wallpaper: &Wallpaper) -> gtk4::Widget {
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
        let title = gtk4::Label::new(Some(&wallpaper.title));
        title.set_max_width_chars(20);
        title.set_ellipsize(gtk4::pango::EllipsizeMode::End);
        title.set_halign(gtk4::Align::Center);

        box_widget.append(&image);
        box_widget.append(&title);

        box_widget.upcast()
    }

    /// 创建列表视图项
    fn create_list_item(&self, wallpaper: &Wallpaper) -> gtk4::Widget {
        let box_widget = gtk4::Box::new(gtk4::Orientation::Horizontal, 12);
        box_widget.set_margin_all(12);

        // 缩略图
        let image = gtk4::Image::from_icon_name("image-x-generic-symbolic");
        image.set_pixel_size(48);

        // 信息区域
        let info_box = gtk4::Box::new(gtk4::Orientation::Vertical, 4);
        info_box.set_hexpand(true);

        let title = gtk4::Label::new(Some(&wallpaper.title));
        title.add_css_class("heading");
        title.set_halign(gtk4::Align::Start);

        let subtitle = gtk4::Label::new(Some(&format!("{} • {}", wallpaper.wp_type, self.format_size(wallpaper.size))));
        subtitle.add_css_class("dim-label");
        subtitle.set_halign(gtk4::Align::Start);

        info_box.append(&title);
        info_box.append(&subtitle);

        // 索引
        let index = gtk4::Label::new(Some(&format!("#{}", wallpaper.id)));
        index.add_css_class("dim-label");

        box_widget.append(&image);
        box_widget.append(&info_box);
        box_widget.append(&index);

        box_widget.upcast()
    }

    /// 格式化文件大小
    fn format_size(&self, bytes: u64) -> String {
        const KB: u64 = 1024;
        const MB: u64 = KB * 1024;

        if bytes >= MB {
            format!("{:.1} MB", bytes as f64 / MB as f64)
        } else if bytes >= KB {
            format!("{:.1} KB", bytes as f64 / KB as f64)
        } else {
            format!("{} B", bytes)
        }
    }
}
