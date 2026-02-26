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
use lwg_core::wallpaper::WallpaperManager;
use lwg_core::config::ConfigManager;
use lwg_core::performance::PerformanceMonitor;

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
        let navbar = NavBar::builder()
            .launch(())
            .forward(sender.input_sender(), |output| AppMsg::NavBarMessage(output));

        let wallpaper_list = WallpaperList::builder()
            .launch(())
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
        
        match ConfigManager::new() {
            Ok(config) => {
                match &config.config.assets_path {
                    Some(workshop_path) => {
                        eprintln!("使用 Workshop 路径：{}", workshop_path);
                        let mut wm = WallpaperManager::new(workshop_path);
                        match wm.scan() {
                            Ok(wallpapers) => {
                                let wallpapers_vec: Vec<_> = wallpapers.values().cloned().collect();
                                eprintln!("✅ 扫描到 {} 个壁纸", wallpapers_vec.len());
                                wallpaper_manager = Some(wm);
                                
                                let sender_clone = sender.input_sender().clone();
                                std::thread::spawn(move || {
                                    sender_clone.send(AppMsg::WallpapersScanned(wallpapers_vec)).ok();
                                });
                            }
                            Err(e) => {
                                eprintln!("❌ 扫描壁纸失败：{:?}", e);
                            }
                        }
                    }
                    None => {
                        eprintln!("⚠️  未配置 Workshop 路径");
                    }
                }
            }
            Err(e) => {
                eprintln!("❌ 加载配置失败：{:?}", e);
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

    fn update(&mut self, msg: Self::Input, sender: ComponentSender<Self>, _root: &Self::Root) {
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
                // 发送数据到 PerformancePage
                self.performance_page.emit(PerformancePageInput::UpdateStats(cpu, memory));
            }
            AppMsg::WallpapersScanned(wallpapers) => {
                eprintln!("📋 加载 {} 个壁纸到列表", wallpapers.len());
                self.wallpaper_list
                    .emit(WallpaperListInput::LoadWallpapers(wallpapers));
            }
            AppMsg::WallpaperListMessage(output) => {
                match output {
                    WallpaperListOutput::Selected(id) => {
                        eprintln!("🎨 壁纸选中：{}", id);
                    }
                    WallpaperListOutput::Activated(id) => {
                        eprintln!("▶️  壁纸激活：{}", id);
                    }
                }
            }
            AppMsg::SidebarMessage(output) => {
                match output {
                    SidebarOutput::ApplyRequested(id) => {
                        eprintln!("💾 应用壁纸：{}", id);
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
