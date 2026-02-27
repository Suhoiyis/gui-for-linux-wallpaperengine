use gtk4::prelude::*;
use relm4::prelude::*;
use std::time::Duration;
use tracing::{info, debug, error, warn};

use crate::navbar::{NavBar, NavBarOutput};
use crate::wallpaper_list::{WallpaperList, WallpaperListInput, WallpaperListOutput};
use crate::sidebar::{Sidebar, SidebarInput, SidebarOutput};
use crate::performance_page::{PerformancePage, PerformancePageInput};
use std::sync::Arc;
use tokio::sync::Mutex;
use lwg_core::wallpaper::WallpaperManager;
use lwg_core::config::{ConfigManager, AppConfig};
use lwg_core::performance::PerformanceMonitor;
use lwg_core::controller::WallpaperController;
use crate::thumbnail_cache::ThumbnailCache;
use lwg_core::history::HistoryManager;
use lwg_core::nickname::NicknameManager;

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum AppPage {
    Wallpapers,
    Settings,
    Performance,
}

impl AppPage {
    fn name(&self) -> &'static str {
        match self {
            AppPage::Wallpapers => "wallpapers",
            AppPage::Settings => "settings",
            AppPage::Performance => "performance",
        }
    }
}

pub struct App {
    current_page: AppPage,
    navbar: Controller<NavBar>,
    wallpaper_list: Controller<WallpaperList>,
    sidebar: Controller<Sidebar>,
    settings_page: Controller<crate::settings_page::SettingsPage>,
    performance_page: Controller<PerformancePage>,
    wallpaper_manager: Option<WallpaperManager>,
    config: Arc<Mutex<AppConfig>>,
    wallpaper_controller: Arc<Mutex<WallpaperController>>,
    thumbnail_cache: Arc<ThumbnailCache>,
    nickname_manager: Arc<Mutex<NicknameManager>>,
    history_manager: Arc<Mutex<HistoryManager>>,
    // Store Stack reference for page switching
    main_stack: gtk4::Stack,
}

#[derive(Debug)]
pub enum AppMsg {
    NavigateTo(AppPage),
    NavBarMessage(NavBarOutput),
    WallpaperListMessage(WallpaperListOutput),
    SidebarMessage(SidebarOutput),
    SettingsPageMessage(crate::settings_page::SettingsPageOutput),
    WallpapersScanned(Vec<lwg_core::wallpaper::Wallpaper>),
    UpdatePerformance(f32, f32), // cpu, memory
}

#[relm4::component(pub)]
impl Component for App {
    type Init = ();
    type Input = AppMsg;
    type Output = ();
    type CommandOutput = ();

    view! {
        gtk4::ApplicationWindow {
            set_title: Some("Linux Wallpaper Engine"),
            set_default_width: 1200,
            set_default_height: 800,

            gtk4::Box {
                set_orientation: gtk4::Orientation::Vertical,

                #[name = "nav_container"]
                gtk4::Box {
                    set_orientation: gtk4::Orientation::Vertical,
                },

                gtk4::Box {
                    set_orientation: gtk4::Orientation::Horizontal,
                    set_spacing: 6,
                    set_margin_all: 6,

                    gtk4::Button {
                        set_label: "壁纸",
                        connect_clicked => AppMsg::NavigateTo(AppPage::Wallpapers),
                    },
                    gtk4::Button {
                        set_label: "设置",
                        connect_clicked => AppMsg::NavigateTo(AppPage::Settings),
                    },
                    gtk4::Button {
                        set_label: "性能",
                        connect_clicked => AppMsg::NavigateTo(AppPage::Performance),
                    },
                },

                #[name = "main_stack"]
                gtk4::Stack {
                    set_hexpand: true,
                    set_vexpand: true,
                    set_transition_type: gtk4::StackTransitionType::Crossfade,
                },
            },
        }
    }

    fn init(
        _init: Self::Init,
        _root: Self::Root,
        sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        // 初始化配置管理器和共享配置
        let config_manager = ConfigManager::new().expect("无法初始化配置管理器");
        let config = Arc::new(Mutex::new(config_manager.config.clone()));
        
        // 初始化缩略图缓存
        let thumbnail_cache = Arc::new(ThumbnailCache::new(100));
        
        // 初始化 NicknameManager
        let config_dir = std::path::PathBuf::from(
            std::env::var("XDG_CONFIG_HOME")
                .unwrap_or_else(|_| format!("{}/.config", std::env::var("HOME").unwrap_or_default()))
        ).join("linux-wallpaperengine-gui");
        
        let nickname_manager = Arc::new(Mutex::new(
            lwg_core::nickname::NicknameManager::new(&config_dir)
        ));
        
        let history_manager = Arc::new(Mutex::new(
            lwg_core::history::HistoryManager::new(&config_dir)
        ));
        
        // 初始化控制器
        let wallpaper_controller = Arc::new(Mutex::new(WallpaperController::new(config.clone())));
        
        let navbar = NavBar::builder()
            .launch(())
            .forward(sender.input_sender(), |output| AppMsg::NavBarMessage(output));

        let wallpaper_list = WallpaperList::builder()
            .launch(thumbnail_cache.clone())
            .forward(sender.input_sender(), |output| AppMsg::WallpaperListMessage(output));

        let sidebar = Sidebar::builder()
            .launch(())
            .forward(sender.input_sender(), |output| AppMsg::SidebarMessage(output));

        let settings_page = crate::settings_page::SettingsPage::builder()
            .launch(())
            .forward(sender.input_sender(), |output| AppMsg::SettingsPageMessage(output));

        let performance_page = PerformancePage::builder()
            .launch(())
            .detach();

        // 初始化 PerformanceMonitor 并启动定时更新
        let perf_monitor = PerformanceMonitor::new();
        
        // 启动 1 秒定时更新
        let sender_clone = sender.input_sender().clone();
        glib::timeout_add_local(Duration::from_secs(1), move || {
            let stats = perf_monitor.get_stats();
            sender_clone.send(AppMsg::UpdatePerformance(stats.total_cpu, stats.total_memory_mb)).ok();
            glib::ControlFlow::Continue
        });

        // 初始化 WallpaperManager
        let mut wallpaper_manager: Option<WallpaperManager> = None;
        
        // Auto-detect Workshop path if not configured
        let workshop_path = config_manager.config.assets_path.clone().or_else(|| {
            let home = std::env::var("HOME").unwrap_or_default();
            // Try common Steam Workshop paths
            let possible_paths = vec![
                format!("{}/.local/share/Steam/steamapps/workshop/content/431960", home),
                format!("{}/.steam/steam/steamapps/workshop/content/431960", home),
                format!("{}/.steam/root/steamapps/workshop/content/431960", home),
            ];
            for path in possible_paths {
                if std::path::Path::new(&path).exists() {
                    info!("Auto-detected Workshop path: {}", path);
                    return Some(path);
                }
            }
            None
        });
        
        if let Some(path) = workshop_path {
            info!("Using Workshop path: {}", path);
            let mut wm = WallpaperManager::new(path);
            if let Ok(wallpapers) = wm.scan() {
                let wallpapers_vec: Vec<_> = wallpapers.values().cloned().collect();
                info!("Scanned {} wallpapers", wallpapers_vec.len());
                wallpaper_manager = Some(wm);
                
                let sender_clone = sender.input_sender().clone();
                std::thread::spawn(move || {
                    sender_clone.send(AppMsg::WallpapersScanned(wallpapers_vec)).ok();
                });
            }
        } else {
            warn!("No Workshop path found. Please configure assets_path in config.json");
        }

        let mut model = Self {
            current_page: AppPage::Wallpapers,
            navbar,
            wallpaper_list,
            sidebar,
            settings_page,
            performance_page,
            wallpaper_manager,
            config,
            wallpaper_controller,
            thumbnail_cache,
            nickname_manager,
            history_manager,
            main_stack: gtk4::Stack::new(), // Temporary, will be replaced after view_output
        };

        let widgets = view_output!();

        widgets.nav_container.append(model.navbar.widget());

        // 创建壁纸页面（Paned 分割）
        let wallpapers_paned = gtk4::Paned::new(gtk4::Orientation::Horizontal);
        wallpapers_paned.set_position(800);
        
        let wp_scroll = gtk4::ScrolledWindow::new();
        wp_scroll.set_hexpand(true);
        wp_scroll.set_vexpand(true);
        wp_scroll.set_child(Some(model.wallpaper_list.widget()));
        
        let sb_scroll = gtk4::ScrolledWindow::new();
        sb_scroll.set_hexpand(false);
        sb_scroll.set_vexpand(true);
        sb_scroll.set_child(Some(model.sidebar.widget()));
        
        wallpapers_paned.set_start_child(Some(&wp_scroll));
        wallpapers_paned.set_end_child(Some(&sb_scroll));

        widgets.main_stack.add_named(&wallpapers_paned, Some("wallpapers"));
        widgets.main_stack.add_named(model.settings_page.widget(), Some("settings"));
        widgets.main_stack.add_named(model.performance_page.widget(), Some("performance"));

        widgets.main_stack.set_visible_child(&wallpapers_paned);
        
        // Update model's main_stack with the actual widget from view
        model.main_stack = widgets.main_stack.clone();

        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, _sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            AppMsg::NavigateTo(page) => {
                self.current_page = page;
                let page_name = match page {
                    AppPage::Wallpapers => "wallpapers",
                    AppPage::Settings => "settings",
                    AppPage::Performance => "performance",
                };
                self.main_stack.set_visible_child_name(page_name);
            }
            AppMsg::NavBarMessage(nav_output) => {
                match nav_output {
                    NavBarOutput::CompactModeToggled(enabled) => {
                        info!("Compact mode toggled: {}", enabled);
                        // TODO: Implement compact window toggle
                    }
                    NavBarOutput::HistoryRequested => {
                        info!("History requested");
                        // TODO: Implement history dialog when HistoryManager is connected
                    }
                    NavBarOutput::AboutRequested => {
                        info!("About requested");
                        // Show a simple about dialog
                        let dialog = gtk4::Dialog::builder()
                            .title("关于")
                            .modal(true)
                            .build();
                        let content = dialog.content_area();
                        let label = gtk4::Label::new(Some("Linux Wallpaper Engine GUI\n\nVersion: 2.0.0 (Rust)\n\nA modern GTK4 interface for managing Steam Workshop live wallpapers."));
                        label.set_margin_all(12);
                        label.set_wrap(true);
                        content.append(&label);
                        dialog.add_button("确定", gtk4::ResponseType::Ok);
                        dialog.connect_response(|d, _| d.close());
                        dialog.show();
                    }
                    NavBarOutput::ScreenChanged(screen) => {
                        info!("Screen changed: {}", screen);
                        // TODO: Update config.last_screen
                    }
                }
            }
            AppMsg::UpdatePerformance(cpu, memory) => {
                debug!("Performance: CPU {:.1}% | Memory {:.0} MB", cpu, memory);
                self.performance_page.emit(PerformancePageInput::UpdateStats(cpu, memory));
            }
            AppMsg::WallpapersScanned(wallpapers) => {
                info!("Loaded {} wallpapers", wallpapers.len());
                self.wallpaper_list.emit(WallpaperListInput::LoadWallpapers(wallpapers));
            }
            AppMsg::WallpaperListMessage(output) => {
                match output {
                    WallpaperListOutput::Selected(id) => {
                        debug!("Wallpaper selected: {}", id);
                        if let Some(ref wm) = self.wallpaper_manager {
                            if let Some(wp) = wm.get(&id) {
                                let info = crate::sidebar::WallpaperInfo {
                                    id: wp.id.clone(),
                                    title: wp.title.clone(),
                                    wallpaper_type: wp.wp_type.clone(),
                                    size: format!("{:.1} MB", wp.size as f64 / 1024.0 / 1024.0),
                                };
                                self.sidebar.emit(crate::sidebar::SidebarInput::SelectWallpaper(info));
                            }
                        }
                    }
                    WallpaperListOutput::Activated(id) => {
                        info!("Wallpaper activated: {}", id);
                        let controller = self.wallpaper_controller.clone();
                        tokio::spawn(async move {
                            let mut controller = controller.lock().await;
                            if let Err(e) = controller.apply(&id, None).await {
                                error!("Failed to apply wallpaper: {:?}", e);
                            } else {
                                info!("Wallpaper applied: {}", id);
                            }
                        });
                    }
                }
            }
            AppMsg::SidebarMessage(output) => {
                match output {
                    SidebarOutput::ApplyRequested(id) => {
                        info!("Applying wallpaper: {}", id);
                        let controller = self.wallpaper_controller.clone();
                        tokio::spawn(async move {
                            let mut controller = controller.lock().await;
                            if let Err(e) = controller.apply(&id, None).await {
                                error!("Failed to apply wallpaper: {:?}", e);
                            } else {
                                info!("Wallpaper applied: {}", id);
                            }
                        });
                    }
SidebarOutput::NicknameChanged(id, nickname) => {
                        let nickname_manager = self.nickname_manager.clone();
                        tokio::spawn(async move {
                            let mut nm = nickname_manager.lock().await;
                            if let Err(e) = nm.set(&id, &nickname) {
                                error!("Failed to set nickname: {}", e);
                            } else {
                                info!("Nickname saved: {} -> {}", id, nickname);
                            }
                        });
                    }
SidebarOutput::DeleteRequested(id) => {
                        info!("Deleting wallpaper: {}", id);
                        if let Some(ref mut wm) = self.wallpaper_manager {
                            match wm.delete(&id) {
                                Ok(true) => {
                                    info!("Wallpaper deleted: {}", id);
                                    // Refresh the wallpaper list
                                    if let Ok(wallpapers) = wm.scan() {
                                        let wallpapers_vec: Vec<_> = wallpapers.values().cloned().collect();
                                        self.wallpaper_list.emit(WallpaperListInput::LoadWallpapers(wallpapers_vec));
                                    }
                                }
                                Ok(false) => warn!("Wallpaper not found: {}", id),
                                Err(e) => error!("Failed to delete wallpaper: {}", e),
                            }
                        }
                    }
SidebarOutput::OpenFolderRequested(id) => {
                        debug!("Opening folder: {}", id);
                        if let Some(ref wm) = self.wallpaper_manager {
                            if let Some(wp) = wm.get(&id) {
                                let path = wp.preview.parent().unwrap_or(&wp.preview);
                                // Try multiple file managers
                                for fm in &["thunar", "nautilus", "dolphin", "xdg-open"] {
                                    if which::which(fm).is_ok() {
                                        if let Err(e) = std::process::Command::new(fm)
                                            .arg(path)
                                            .spawn()
                                        {
                                            error!("Failed to open folder with {}: {}", fm, e);
                                        }
                                        break;
                                    }
                                }
                            }
                        }
                    }
                    SidebarOutput::WallpaperSelected(id, title, wp_type, size) => {
                        debug!("Wallpaper details: {} - {} ({} / {})", id, title, wp_type, size);
                    }
                }
            }
            AppMsg::SettingsPageMessage(output) => {
                match output {
                    crate::settings_page::SettingsPageOutput::ConfigChanged(key, value) => {
                        info!("Config changed: {} = {:?}", key, value);
                        let config = self.config.clone();
                        tokio::spawn(async move {
                            let mut cfg = config.lock().await;
                            match key.as_str() {
                                "fps" => if let Some(v) = value.as_u64() { cfg.fps = v as u32; },
                                "volume" => if let Some(v) = value.as_u64() { cfg.volume = v as u32; },
                                "silence" => if let Some(v) = value.as_bool() { cfg.silence = v; },
                                "scaling" => if let Some(v) = value.as_str() { cfg.scaling = v.to_string(); },
                                "no_fullscreen_pause" => if let Some(v) = value.as_bool() { cfg.no_fullscreen_pause = v; },
                                "disable_mouse" => if let Some(v) = value.as_bool() { cfg.disable_mouse = v; },
                                "no_auto_mute" => if let Some(v) = value.as_bool() { cfg.no_auto_mute = v; },
                                "no_audio_processing" => if let Some(v) = value.as_bool() { cfg.no_audio_processing = v; },
                                "disable_parallax" => if let Some(v) = value.as_bool() { cfg.disable_parallax = v; },
                                "disable_particles" => if let Some(v) = value.as_bool() { cfg.disable_particles = v; },
                                "clamping" => if let Some(v) = value.as_str() { cfg.clamping = v.to_string(); },
                                "screenshot_delay" => if let Some(v) = value.as_u64() { cfg.screenshot_delay = v as u32; },
                                "screenshot_res" => if let Some(v) = value.as_str() { cfg.screenshot_res = v.to_string(); },
                                "prefer_xvfb" => if let Some(v) = value.as_bool() { cfg.prefer_xvfb = v; },
                                "cycle_enabled" => if let Some(v) = value.as_bool() { cfg.cycle_enabled = v; },
                                "cycle_interval" => if let Some(v) = value.as_u64() { cfg.cycle_interval = v as u32; },
                                "cycle_order" => if let Some(v) = value.as_str() { cfg.cycle_order = v.to_string(); },
                                "wayland_only_active" => if let Some(v) = value.as_bool() { cfg.wayland_only_active = v; },
                                "wayland_ignore_appids" => if let Some(v) = value.as_str() { cfg.wayland_ignore_appids = v.to_string(); },
                                "compact_mode" => if let Some(v) = value.as_bool() { cfg.compact_mode = v; },
                                _ => warn!("Unknown config key: {}", key),
                            }
                            // TODO: Save to file
                        });
                    }
                    crate::settings_page::SettingsPageOutput::PathSelected(category, path) => {
                        info!("Path selected: {} = {}", category, path);
                        // TODO: Update config paths and open file chooser if needed
                    }
                    crate::settings_page::SettingsPageOutput::OpenNicknameManager => {
                        info!("Opening nickname manager");
                        // TODO: Open nickname manager dialog
                    }
                }
            }
        }
    }

}
