use gtk4::prelude::*;
use relm4::prelude::*;
use lwg_core::{Wallpaper, WallpaperManager};

pub struct WallpaperList {
    wallpapers: Vec<Wallpaper>,
    list_box: gtk4::ListBox,
}

#[derive(Debug, Clone)]
pub enum WallpaperListInput {
    Scan,
    Scanned(Vec<Wallpaper>),
    Select(String),
    Apply(String),
}

#[derive(Debug, Clone)]
pub enum WallpaperListOutput {
    Selected(String),
    Apply(String),
}

#[relm4::component(pub)]
impl Component for WallpaperList {
    type Init = ();
    type Input = WallpaperListInput;
    type Output = WallpaperListOutput;
    type CommandOutput = Vec<Wallpaper>;

    view! {
        gtk4::ScrolledWindow {
            set_vexpand: true,
            set_hscrollbar_policy: gtk4::PolicyType::Never,
            set_vscrollbar_policy: gtk4::PolicyType::Automatic,

            #[local_ref]
            list_box -> gtk4::ListBox {}
        }
    }

    fn init(
        _init: Self::Init,
        root: Self::Root,
        sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        let list_box = gtk4::ListBox::new();
        list_box.set_selection_mode(gtk4::SelectionMode::Single);

        let model = Self {
            wallpapers: Vec::new(),
            list_box: list_box.clone(),
        };

        let widgets = view_output!();

        sender.input(WallpaperListInput::Scan);

        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            WallpaperListInput::Scan => {
                sender.oneshot_command(async move {
                    let workshop_path = lwg_core::ConfigManager::get_workshop_path();
                    let mut manager = WallpaperManager::new(workshop_path);
                    match manager.scan() {
                        Ok(wallpapers) => wallpapers.values().cloned().collect(),
                        Err(_) => Vec::new(),
                    }
                });
            }
            WallpaperListInput::Scanned(wallpapers) => {
                self.wallpapers = wallpapers;
                self.refresh_list();
            }
            WallpaperListInput::Select(id) => {
                sender.output(WallpaperListOutput::Selected(id));
            }
            WallpaperListInput::Apply(id) => {
                sender.output(WallpaperListOutput::Apply(id));
            }
        }
    }

    fn update_cmd(
        &mut self,
        msg: Self::CommandOutput,
        sender: ComponentSender<Self>,
        _root: &Self::Root,
    ) {
        sender.input(WallpaperListInput::Scanned(msg));
    }
}

impl WallpaperList {
    fn refresh_list(&self) {
        while let Some(child) = self.list_box.first_child() {
            self.list_box.remove(&child);
        }

        for wallpaper in &self.wallpapers {
            let row = gtk4::Box::new(gtk4::Orientation::Horizontal, 10);
            row.set_margin_top(5);
            row.set_margin_bottom(5);
            row.set_margin_start(10);
            row.set_margin_end(10);

            let title_label = gtk4::Label::new(Some(&wallpaper.title));
            title_label.set_halign(gtk4::Align::Start);
            title_label.set_hexpand(true);
            row.append(&title_label);

            let type_label = gtk4::Label::new(Some(&wallpaper.wp_type));
            type_label.add_css_class("dim-label");
            row.append(&type_label);

            let apply_btn = gtk4::Button::with_label("应用");
            let id = wallpaper.id.clone();
            apply_btn.connect_clicked(move |_| {
                println!("应用壁纸: {}", id);
            });
            row.append(&apply_btn);

            let list_box_row = gtk4::ListBoxRow::new();
            list_box_row.set_child(Some(&row));
            self.list_box.append(&list_box_row);
        }

        self.list_box.show();
    }
}
