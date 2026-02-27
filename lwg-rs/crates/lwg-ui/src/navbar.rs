use gtk4::prelude::*;
use relm4::prelude::*;
use libadwaita::{self, prelude::*};
use lwg_core::screen::ScreenManager;

/// 导航栏组件
pub struct NavBar {
    compact_mode: bool,
    screens: Vec<String>,
}

#[derive(Debug)]
pub enum NavBarInput {
    ToggleCompactMode,
    ShowHistory,
    ShowAbout,
    ScreenChanged(String),
}

#[derive(Debug)]
pub enum NavBarOutput {
    CompactModeToggled(bool),
    HistoryRequested,
    AboutRequested,
    ScreenChanged(String),
}

#[relm4::component(pub)]
impl Component for NavBar {
    type Init = ();
    type Input = NavBarInput;
    type Output = NavBarOutput;
    type CommandOutput = ();

    view! {
        gtk4::Box {
            set_orientation: gtk4::Orientation::Horizontal,
            set_spacing: 6,
            set_margin_all: 6,

            // 汉堡菜单按钮
            gtk4::MenuButton {
                set_icon_name: "open-menu-symbolic",
                set_tooltip_text: Some("菜单"),

                #[wrap(Some)]
                set_popover = &gtk4::PopoverMenu::from_model(Some(&menu_model)),
            },

            gtk4::Separator {
                set_orientation: gtk4::Orientation::Vertical,
            },

            // 播放历史按钮
            gtk4::Button {
                set_icon_name: "document-open-recent-symbolic",
                set_tooltip_text: Some("播放历史"),
                connect_clicked[sender] => move |_| {
                    sender.input(NavBarInput::ShowHistory);
                },
            },

            gtk4::Separator {
                set_orientation: gtk4::Orientation::Vertical,
            },

            // 屏幕选择器
            gtk4::Box {
                set_orientation: gtk4::Orientation::Horizontal,
                set_spacing: 6,

                gtk4::Label {
                    set_label: "屏幕:",
                    set_margin_end: 6,
                },

                #[name = "screen_selector"]
                gtk4::DropDown {
                    set_model: Some(&gtk4::StringList::new(&["Loading..."])),  // Will be updated in init
                    set_selected: 0,
                    set_tooltip_text: Some("选择显示器"),
                    connect_selected_notify[sender] => move |dropdown| {
                        if let Some(model) = dropdown.model() {
                            let selected = dropdown.selected();
                            if let Some(item) = model.item(selected) {
                                if let Some(name) = item.downcast_ref::<gtk4::StringObject>() {
                                    sender.input(NavBarInput::ScreenChanged(name.string().to_string()));
                                }
                            }
                        }
                    },
                },
            },

            gtk4::Box {
                set_hexpand: true,
            },

            // 紧凑模式切换
            gtk4::ToggleButton {
                set_icon_name: "view-restore-symbolic",
                set_tooltip_text: Some("紧凑模式"),
                set_active: false,
                connect_toggled[sender] => move |btn| {
                    sender.input(NavBarInput::ToggleCompactMode);
                },
            },
        }
    }

    fn init(
        _init: Self::Init,
        root: Self::Root,
        sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        // 创建菜单模型
        let menu_model = gtk4::gio::Menu::new();
        menu_model.append(Some("关于"), Some("nav.about"));

        // 检测真实屏幕
        let screen_manager = ScreenManager::new();
        let screens = screen_manager.names();
        
        // 如果没有检测到屏幕，使用默认值
        let screen_names: Vec<&str> = if screens.is_empty() {
            vec!["Default"]
        } else {
            screens.iter().map(|s| s.as_str()).collect()
        };

        let model = Self {
            compact_mode: false,
            screens: screens.clone(),
        };

        let widgets = view_output!();
        
        // 更新屏幕选择器
        widgets.screen_selector.set_model(Some(&gtk4::StringList::new(&screen_names)));

        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            NavBarInput::ToggleCompactMode => {
                self.compact_mode = !self.compact_mode;
                sender.output(NavBarOutput::CompactModeToggled(self.compact_mode)).ok();
            }
            NavBarInput::ShowHistory => {
                sender.output(NavBarOutput::HistoryRequested).ok();
            }
            NavBarInput::ShowAbout => {
                sender.output(NavBarOutput::AboutRequested).ok();
            }
            NavBarInput::ScreenChanged(screen) => {
                sender.output(NavBarOutput::ScreenChanged(screen)).ok();
            }
        }
    }
}
