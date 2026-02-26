use gtk4::prelude::*;
use relm4::prelude::*;
use relm4::factory::FactoryVecDeque;
use lwg_core::wallpaper::Wallpaper;
use crate::thumbnail_cache::ThumbnailCache;
use std::sync::Arc;

#[derive(Debug)]
pub struct WallpaperCard {
    wallpaper: Wallpaper,
    is_selected: bool,
    thumbnail_cache: Arc<ThumbnailCache>,
    texture: Option<gtk4::gdk::Texture>,
}

#[derive(Debug)]
pub enum WallpaperCardInput {
    Select(bool),
    ThumbnailLoaded(gtk4::gdk::Texture),
}

#[derive(Debug)]
pub enum WallpaperCardOutput {
    Selected(String),
    Activated(String),
}

#[relm4::factory(pub)]
impl FactoryComponent for WallpaperCard {
    type Init = (Wallpaper, Arc<ThumbnailCache>);
    type Input = WallpaperCardInput;
    type Output = WallpaperCardOutput;
    type CommandOutput = Option<gtk4::gdk::Texture>;


    type ParentWidget = gtk4::FlowBox;

    view! {
        gtk4::Box {
            set_orientation: gtk4::Orientation::Vertical,
            set_spacing: 8,
            set_width_request: 180,
            set_height_request: 220,
            add_css_class: "card",
            
            gtk4::Image {
                set_pixel_size: 120,
                set_vexpand: true,
                set_valign: gtk4::Align::Center,
                set_halign: gtk4::Align::Center,
                #[track(self.texture.is_some())]
                set_paintable: self.texture.as_ref().map(|t| t.upcast_ref::<gtk4::gdk::Paintable>()),

                set_icon_name: if self.texture.is_none() { Some("image-x-generic-symbolic") } else { None },
            },

            gtk4::Label {
                set_label: &self.wallpaper.title,
                set_max_width_chars: 18,
                set_ellipsize: gtk4::pango::EllipsizeMode::End,
                set_halign: gtk4::Align::Center,
                add_css_class: "caption",
            },
        }
    }

    fn init_model(init: Self::Init, _index: &DynamicIndex, sender: FactorySender<Self>) -> Self {
        let (wallpaper, thumbnail_cache) = init;
        
        let preview_path = wallpaper.preview.clone();
        let cache_clone = thumbnail_cache.clone();
        let id_clone = wallpaper.id.clone();
        
        sender.command(|cmd_sender, _| async move {
            let id = id_clone.clone();
            // 先尝试从缓存获取
            if let Some(texture) = cache_clone.get(&id).await {
                cmd_sender.send(Some(texture)).ok();
                return;
            }
            
            // 否则从文件加载
            if let Some(texture) = ThumbnailCache::load_from_file(&preview_path) {
                cache_clone.insert(id.clone(), texture.clone()).await;
                cmd_sender.send(Some(texture)).ok();
            } else {
                cmd_sender.send(None).ok();
            }
        });


        Self {
            wallpaper,
            is_selected: false,
            thumbnail_cache,
            texture: None,
        }
    }

    fn update(&mut self, msg: Self::Input, _sender: FactorySender<Self>) {
        match msg {
            WallpaperCardInput::Select(selected) => {
                self.is_selected = selected;
            }
            WallpaperCardInput::ThumbnailLoaded(texture) => {
                self.texture = Some(texture);
            }
        }
    }
    fn update_cmd(&mut self, msg: Self::CommandOutput, sender: FactorySender<Self>) {
        if let Some(texture) = msg {
            sender.input(WallpaperCardInput::ThumbnailLoaded(texture));
        }
    }

}

pub struct WallpaperList {
    wallpapers: FactoryVecDeque<WallpaperCard>,
    selected_id: Option<String>,
    wallpaper_data: Vec<Wallpaper>,
    thumbnail_cache: Arc<ThumbnailCache>,
}

#[derive(Debug)]
pub enum WallpaperListInput {
    LoadWallpapers(Vec<Wallpaper>),
    SelectWallpaper(String),
    SelectIndex(usize),
}

#[derive(Debug)]
pub enum WallpaperListOutput {
    Selected(String),
    Activated(String),
}

#[relm4::component(pub)]
impl Component for WallpaperList {
    type Init = Arc<ThumbnailCache>;
    type Input = WallpaperListInput;
    type Output = WallpaperListOutput;
    type CommandOutput = ();

    view! {
        gtk4::ScrolledWindow {
            set_hexpand: true,
            set_vexpand: true,

            #[local_ref]
            flow_box -> gtk4::FlowBox {
                set_selection_mode: gtk4::SelectionMode::Single,
                set_max_children_per_line: 10,
                set_min_children_per_line: 2,
                set_column_spacing: 12,
                set_row_spacing: 12,
                set_margin_all: 12,
                
                connect_selected_children_changed[sender] => move |fb| {
                    if let Some(child) = fb.selected_children().first() {
                        sender.input(WallpaperListInput::SelectIndex(child.index() as usize));
                    }
                },
            }
        }
    }

    fn init(
        init: Self::Init,
        root: Self::Root,
        sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        let wallpapers = FactoryVecDeque::builder()
            .launch(gtk4::FlowBox::default())
            .forward(sender.input_sender(), |output| match output {
                WallpaperCardOutput::Selected(id) => WallpaperListInput::SelectWallpaper(id),
                WallpaperCardOutput::Activated(id) => WallpaperListInput::SelectWallpaper(id),
            });

        let model = Self {
            wallpapers,
            selected_id: None,
            wallpaper_data: Vec::new(),
            thumbnail_cache: init,
        };

        let flow_box = model.wallpapers.widget();
        let widgets = view_output!();

        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            WallpaperListInput::LoadWallpapers(wallpapers) => {
                self.wallpaper_data = wallpapers.clone();
                let mut guard = self.wallpapers.guard();
                guard.clear();
                for wp in wallpapers {
                    guard.push_back((wp, self.thumbnail_cache.clone()));
                }
            }
            WallpaperListInput::SelectWallpaper(id) => {
                self.selected_id = Some(id.clone());
                sender.output(WallpaperListOutput::Selected(id)).ok();
            }
            WallpaperListInput::SelectIndex(index) => {
                if let Some(wp) = self.wallpaper_data.get(index) {
                    let id = wp.id.clone();
                    self.selected_id = Some(id.clone());
                    sender.output(WallpaperListOutput::Selected(id)).ok();
                }
            }
        }
    }
}