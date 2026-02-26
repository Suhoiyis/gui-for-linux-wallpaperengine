//! Linux Wallpaper Engine GUI - 主应用窗口
//! Phase 4B Task 4B.2: 连接 PerformanceMonitor（修复版）

use gtk4::prelude::*;
use relm4::prelude::*;
use libadwaita as adw;
use std::time::Duration;

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

                adw::HeaderBar {},

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
        let workshop_path = config_manager.config.assets_path.clone();
        
        if let Some(path) = workshop_path {
            eprintln!("使用 Workshop 路径：{}", path);
            let mut wm = WallpaperManager::new(path);
            if let Ok(wallpapers) = wm.scan() {
                let wallpapers_vec: Vec<_> = wallpapers.values().cloned().collect();
                eprintln!("✅ 扫描到 {} 个壁纸", wallpapers_vec.len());
                wallpaper_manager = Some(wm);
                
                let sender_clone = sender.input_sender().clone();
                std::thread::spawn(move || {
                    sender_clone.send(AppMsg::WallpapersScanned(wallpapers_vec)).ok();
                });
            }
        }

        let model = Self {
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

        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, _sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            AppMsg::NavigateTo(page) => {
                self.current_page = page;
            }
            AppMsg::NavBarMessage(nav_output) => {
                match nav_output {
                    NavBarOutput::CompactModeToggled(enabled) => {
                        eprintln!("紧凑模式：{}", enabled);
                    }
                    NavBarOutput::HistoryRequested => {
                        eprintln!("请求历史记录");
                    }
                    NavBarOutput::AboutRequested => {
                        eprintln!("请求关于");
                    }
                    NavBarOutput::ScreenChanged(screen) => {
                        eprintln!("屏幕切换：{}", screen);
                    }
                }
            }
            AppMsg::UpdatePerformance(cpu, memory) => {
                eprintln!("📊 CPU: {:.1}% | 内存：{:.0} MB", cpu, memory);
                self.performance_page.emit(PerformancePageInput::UpdateStats(cpu, memory));
            }
            AppMsg::WallpapersScanned(wallpapers) => {
                eprintln!("📋 加载 {} 个壁纸到列表", wallpapers.len());
                self.wallpaper_list.emit(WallpaperListInput::LoadWallpapers(wallpapers));
            }
            AppMsg::WallpaperListMessage(output) => {
                match output {
                    WallpaperListOutput::Selected(id) => {
                        eprintln!("🎨 壁纸选中：{}", id);
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
                        eprintln!("▶️  壁纸激活：{}", id);
                        let controller = self.wallpaper_controller.clone();
                        tokio::spawn(async move {
                            let mut controller = controller.lock().await;
                            if let Err(e) = controller.apply(&id, None).await {
                                eprintln!("❌ 应用壁纸失败：{:?}", e);
                            } else {
                                eprintln!("✅ 壁纸已应用：{}", id);
                            }
                        });
                    }
                }
            }
            AppMsg::SidebarMessage(output) => {
                match output {
                    SidebarOutput::ApplyRequested(id) => {
                        eprintln!("💾 应用壁纸：{}", id);
                        let controller = self.wallpaper_controller.clone();
                        tokio::spawn(async move {
                            let mut controller = controller.lock().await;
                            if let Err(e) = controller.apply(&id, None).await {
                                eprintln!("❌ 应用壁纸失败：{:?}", e);
                            } else {
                                eprintln!("✅ 壁纸已应用：{}", id);
                            }
                        });
                    }
                    SidebarOutput::NicknameChanged(id, nickname) => {
                        eprintln!("🏷️  昵称变更：{} -> {}", id, nickname);
                    }
                    SidebarOutput::DeleteRequested(id) => {
                        eprintln!("🗑️  删除壁纸：{}", id);
                    }
                    SidebarOutput::OpenFolderRequested(id) => {
                        eprintln!("📂 打开文件夹：{}", id);
                    }
                    SidebarOutput::WallpaperSelected(id, title, wp_type, size) => {
                        eprintln!("📄 壁纸详情：{} - {} ({} / {})", id, title, wp_type, size);
                    }
                }
            }
            AppMsg::SettingsPageMessage(output) => {
                match output {
                    crate::settings_page::SettingsPageOutput::ConfigChanged(key, value) => {
                        eprintln!("⚙️  设置变更：{} = {:?}", key, value);
                    }
                    crate::settings_page::SettingsPageOutput::PathSelected(category, path) => {
                        eprintln!("📁 路径选择：{} = {}", category, path);
                    }
                    crate::settings_page::SettingsPageOutput::OpenNicknameManager => {
                        eprintln!("打开昵称管理器");
                    }
                }
            }
        }
    }
}

