use gtk4::prelude::*;
use relm4::prelude::*;
use libadwaita::{self, prelude::*};
use crate::wallpaper_list::{WallpaperList, WallpaperListOutput};
use crate::toolbar::{Toolbar, ToolbarInput, ToolbarOutput, ViewMode};
use crate::grid_view::{GridView, GridViewInput, GridViewOutput};
use crate::list_view::{ListView, ListViewInput, ListViewOutput};
use crate::status_panel::{StatusPanel, StatusPanelInput};
use crate::settings_page::{SettingsPage, SettingsPageInput};
use crate::performance_page::{PerformancePage, PerformancePageInput};
use lwg_core::{ConfigManager, WallpaperController};
use std::sync::Arc;
use tokio::sync::Mutex;

pub struct App {
    wallpaper_list: Controller<WallpaperList>,
    toolbar: Controller<Toolbar>,
    grid_view: Controller<GridView>,
    list_view: Controller<ListView>,
    status_panel: Controller<StatusPanel>,
    settings_page: Controller<SettingsPage>,
    performance_page: Controller<PerformancePage>,
    controller: Arc<Mutex<WallpaperController>>,
    current_page: Page,
    view_mode: ViewMode,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Page {
    Wallpapers,
    Settings,
    Performance,
}

impl Page {
    fn as_str(&self) -> &'static str {
        match self {
            Page::Wallpapers => "wallpapers",
            Page::Settings => "settings",
            Page::Performance => "performance",
        }
    }
}

#[derive(Debug)]
pub enum AppMsg {
    WallpaperSelected(String),
    WallpaperApply(String),
    NavigateTo(Page),
    SwitchViewMode(ViewMode),
    ShowAbout,
    ShowPreferences,
}

#[relm4::component(pub)]
impl Component for App {
    type Init = ();
    type Input = AppMsg;
    type Output = ();
    type CommandOutput = ();

    view! {
        libadwaita::ApplicationWindow {
            set_title: Some("Linux Wallpaper Engine"),
            set_default_width: 1200,
            set_default_height: 800,

            #[wrap(Some)]
            set_content = &gtk4::Box {
                set_orientation: gtk4::Orientation::Vertical,

                libadwaita::HeaderBar {
                    set_title_widget: Some(&gtk4::Label::new(Some("Linux Wallpaper Engine"))),

                    pack_start = &gtk4::Button {
                        set_icon_name: "view-refresh-symbolic",
                        set_tooltip_text: Some("重新扫描"),
                    },

                    pack_end = &gtk4::MenuButton {
                        set_icon_name: "open-menu-symbolic",
                        set_tooltip_text: Some("菜单"),
                    },
                },

                gtk4::Box {
                    set_orientation: gtk4::Orientation::Horizontal,
                    set_spacing: 6,
                    set_halign: gtk4::Align::Center,
                    set_margin_top: 6,
                    set_margin_bottom: 6,

                    #[name = "btn_wallpapers"]
                    gtk4::ToggleButton {
                        set_icon_name: "emblem-photos-symbolic",
                        set_label: "壁纸",
                        add_css_class: "flat",
                        set_active: true,
                        connect_toggled[sender] => move |btn| {
                            if btn.is_active() {
                                sender.input(AppMsg::NavigateTo(Page::Wallpapers));
                            }
                        },
                    },

                    gtk4::ToggleButton {
                        set_icon_name: "preferences-system-symbolic",
                        set_label: "设置",
                        add_css_class: "flat",
                        set_group: Some(&btn_wallpapers),
                        connect_toggled[sender] => move |btn| {
                            if btn.is_active() {
                                sender.input(AppMsg::NavigateTo(Page::Settings));
                            }
                        },
                    },

                    gtk4::ToggleButton {
                        set_icon_name: "utilities-system-monitor-symbolic",
                        set_label: "性能",
                        add_css_class: "flat",
                        set_group: Some(&btn_wallpapers),
                        connect_toggled[sender] => move |btn| {
                            if btn.is_active() {
                                sender.input(AppMsg::NavigateTo(Page::Performance));
                            }
                        },
                    },
                },

                #[name = "stack"]
                gtk4::Stack {
                    set_hexpand: true,
                    set_vexpand: true,
                    set_transition_type: gtk4::StackTransitionType::SlideLeftRight,
                    set_transition_duration: 300,

                    // 壁纸页面
                    add_child: &gtk4::Box {
                        set_orientation: gtk4::Orientation::Vertical,

                        #[local_ref]
                        toolbar_widget -> gtk4::Box {},

                        #[local_ref]
                        status_panel_widget -> gtk4::Box {},

                        #[name = "view_stack"]
                        gtk4::Stack {
                            set_hexpand: true,
                            set_vexpand: true,

                            add_child: &gtk4::Box {
                                #[local_ref]
                                grid_view_widget -> gtk4::ScrolledWindow {},
                            } -> {
                                set_name: "grid",
                            },

                            add_child: &gtk4::Box {
                                #[local_ref]
                                list_view_widget -> gtk4::ScrolledWindow {},
                            } -> {
                                set_name: "list",
                            },
                        },
                    } -> {
                        set_name: "wallpapers",
                    },

                    // 设置页面
                    #[local_ref]
                    settings_page_widget -> gtk4::Box {},

                    // 性能页面
                    #[local_ref]
                    performance_page_widget -> gtk4::Box {},
                },
            },
        }
    }

    fn init(
        _init: Self::Init,
        root: Self::Root,
        sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        let wallpaper_list = WallpaperList::builder()
            .launch(())
            .forward(sender.input_sender(), |msg| match msg {
                WallpaperListOutput::Selected(id) => AppMsg::WallpaperSelected(id),
                WallpaperListOutput::Apply(id) => AppMsg::WallpaperApply(id),
            });

        let toolbar = Toolbar::builder()
            .launch(())
            .forward(sender.input_sender(), |msg| match msg {
                ToolbarOutput::ViewModeChanged(mode) => AppMsg::SwitchViewMode(mode),
                _ => AppMsg::ShowPreferences,
            });

        let grid_view = GridView::builder()
            .launch(())
            .detach();

        let list_view = ListView::builder()
            .launch(())
            .detach();

        let status_panel = StatusPanel::builder()
            .launch(())
            .detach();

        let settings_page = SettingsPage::builder()
            .launch(())
            .detach();

        let performance_page = PerformancePage::builder()
            .launch(())
            .detach();

        let config = Arc::new(Mutex::new(
            ConfigManager::new().map(|c| c.config).unwrap_or_default()
        ));
        let controller = Arc::new(Mutex::new(WallpaperController::new(Arc::clone(&config))));

        let model = Self {
            wallpaper_list,
            toolbar,
            grid_view,
            list_view,
            status_panel,
            settings_page,
            performance_page,
            controller,
            current_page: Page::Wallpapers,
            view_mode: ViewMode::Grid,
        };

        let wallpaper_list_widget = model.wallpaper_list.widget();
        let toolbar_widget = model.toolbar.widget();
        let grid_view_widget = model.grid_view.widget();
        let list_view_widget = model.list_view.widget();
        let status_panel_widget = model.status_panel.widget();
        let settings_page_widget = model.settings_page.widget();
        let performance_page_widget = model.performance_page.widget();

        let widgets = view_output!();

        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, _sender: ComponentSender<Self>, widgets: &mut Self::Widgets) {
        match msg {
            AppMsg::WallpaperSelected(id) => {
                println!("选中壁纸：{}", id);
                self.status_panel.sender().send(StatusPanelInput::SetWallpaper(id)).ok();
            }
            AppMsg::WallpaperApply(id) => {
                println!("应用壁纸：{}", id);
                let controller = Arc::clone(&self.controller);
                relm4::spawn(async move {
                    let mut ctrl = controller.lock().await;
                    let _ = ctrl.apply(&id, None).await;
                });
                self.status_panel.sender().send(StatusPanelInput::SetRunning(true)).ok();
            }
            AppMsg::NavigateTo(page) => {
                if self.current_page != page {
                    println!("导航到页面：{:?}", page);
                    self.current_page = page;
                    widgets.stack.set_visible_child_name(page.as_str());
                }
            }
            AppMsg::SwitchViewMode(mode) => {
                if self.view_mode != mode {
                    println!("切换视图模式：{:?}", mode);
                    self.view_mode = mode;
                    let view_name = match mode {
                        ViewMode::Grid => "grid",
                        ViewMode::List => "list",
                    };
                    widgets.view_stack.set_visible_child_name(view_name);
                }
            }
            AppMsg::ShowAbout => {
                println!("显示关于对话框");
            }
            AppMsg::ShowPreferences => {
                println!("显示首选项");
            }
        }
    }
}
