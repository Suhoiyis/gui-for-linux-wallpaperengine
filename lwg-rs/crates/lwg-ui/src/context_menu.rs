use gtk4::prelude::*;

/// 右键菜单项
#[derive(Debug, Clone)]
pub enum ContextMenuItem {
    Apply,
    Stop,
    SetNickname,
    Separator,
    Delete,
    OpenFolder,
}

/// 创建壁纸右键菜单
pub fn create_wallpaper_context_menu() -> gtk4::PopoverMenu {
    let menu = gtk4::gio::Menu::new();
    
    menu.append(Some("应用壁纸"), Some("wallpaper.apply"));
    menu.append(Some("停止壁纸"), Some("wallpaper.stop"));
    menu.append(Some("设置昵称"), Some("wallpaper.nickname"));
    
    menu.append(Some("删除"), Some("wallpaper.delete"));
    menu.append(Some("打开文件夹"), Some("wallpaper.open_folder"));
    
    gtk4::PopoverMenu::from_model(Some(&menu))
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_context_menu_items() {
        let items = vec![
            ContextMenuItem::Apply,
            ContextMenuItem::Stop,
            ContextMenuItem::SetNickname,
            ContextMenuItem::Separator,
            ContextMenuItem::Delete,
            ContextMenuItem::OpenFolder,
        ];
        assert_eq!(items.len(), 6);
    }
}
