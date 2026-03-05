//! 设置页面 - 所有子页面完善

use gtk4::prelude::*;
use relm4::prelude::*;

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum SettingsSection {
    General,
    Audio,
    Advanced,
    Logs,
}

impl SettingsSection {
    fn name(&self) -> &'static str {
        match self {
            SettingsSection::General => "general",
            SettingsSection::Audio => "audio",
            SettingsSection::Advanced => "advanced",
            SettingsSection::Logs => "logs",
        }
    }
}

#[derive(Debug)]
pub enum SettingsPageInput {}

#[derive(Debug)]
pub enum SettingsPageOutput {
    ConfigChanged(String, serde_json::Value),
    PathSelected(String, String),
    OpenNicknameManager,
}

pub struct SettingsPage {
    current_section: SettingsSection,
}

#[relm4::component(pub)]
impl Component for SettingsPage {
    type Init = ();
    type Input = SettingsPageInput;
    type Output = SettingsPageOutput;
    type CommandOutput = ();

    view! {
        gtk4::Box {
            set_orientation: gtk4::Orientation::Horizontal,
            set_hexpand: true,
            set_vexpand: true,

            // 左侧导航
            gtk4::Box {
                set_orientation: gtk4::Orientation::Vertical,
                set_spacing: 6,
                set_width_request: 200,
                set_margin_all: 16,

                gtk4::Label {
                    set_label: "设置",
                    add_css_class: "title-2",
                    set_halign: gtk4::Align::Start,
                },

                gtk4::Separator {
                    set_margin_bottom: 12,
                },

                gtk4::Button {
                    set_label: "通用",
                    set_halign: gtk4::Align::Start,
                    add_css_class: "flat",
                },

                gtk4::Button {
                    set_label: "音频",
                    set_halign: gtk4::Align::Start,
                    add_css_class: "flat",
                },

                gtk4::Button {
                    set_label: "高级",
                    set_halign: gtk4::Align::Start,
                    add_css_class: "flat",
                },

                gtk4::Button {
                    set_label: "日志",
                    set_halign: gtk4::Align::Start,
                    add_css_class: "flat",
                },

                gtk4::Box {
                    set_vexpand: true,
                },
            },

            gtk4::Separator {
                set_orientation: gtk4::Orientation::Vertical,
            },

            // 右侧内容区域
            #[name = "content_stack"]
            gtk4::Stack {
                set_hexpand: true,
                set_vexpand: true,
                set_margin_all: 24,
            },
        }
    }

    fn init(
        _init: Self::Init,
        _root: Self::Root,
        _sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        let model = Self {
            current_section: SettingsSection::General,
        };

        let widgets = view_output!();

        // ========== General 子页面 ==========
        let general_box = gtk4::Box::new(gtk4::Orientation::Vertical, 16);
        general_box.set_margin_all(12);

        let general_title = gtk4::Label::new(Some("通用设置"));
        general_title.add_css_class("title-1");
        general_title.set_halign(gtk4::Align::Start);
        general_box.append(&general_title);

        // 启动设置组
        let startup_frame = create_frame("启动");
        let startup_content = gtk4::Box::new(gtk4::Orientation::Vertical, 8);
        
        let autostart_box = gtk4::Box::new(gtk4::Orientation::Horizontal, 12);
        let autostart_label = gtk4::Label::new(Some("开机自启"));
        autostart_label.set_hexpand(true);
        autostart_label.set_halign(gtk4::Align::Start);
        let autostart_switch = gtk4::Switch::new();
        autostart_box.append(&autostart_label);
        autostart_box.append(&autostart_switch);
        startup_content.append(&autostart_box);
        startup_frame.set_child(Some(&startup_content));
        general_box.append(&startup_frame);

        // 性能设置组
        let performance_frame = create_frame("性能");
        let performance_content = gtk4::Box::new(gtk4::Orientation::Vertical, 8);
        
        let fps_box = gtk4::Box::new(gtk4::Orientation::Horizontal, 12);
        let fps_label = gtk4::Label::new(Some("FPS 限制"));
        fps_label.set_hexpand(true);
        fps_label.set_halign(gtk4::Align::Start);
        let fps_spin = gtk4::SpinButton::with_range(1.0, 144.0, 1.0);
        fps_box.append(&fps_label);
        fps_box.append(&fps_spin);
        performance_content.append(&fps_box);
        
        let scaling_box = gtk4::Box::new(gtk4::Orientation::Horizontal, 12);
        let scaling_label = gtk4::Label::new(Some("缩放模式"));
        scaling_label.set_hexpand(true);
        scaling_label.set_halign(gtk4::Align::Start);
        let scaling_dropdown = gtk4::DropDown::from_strings(&["默认", "拉伸", "适应", "填充"]);
        scaling_box.append(&scaling_label);
        scaling_box.append(&scaling_dropdown);
        performance_content.append(&scaling_box);
        
        performance_frame.set_child(Some(&performance_content));
        general_box.append(&performance_frame);

        // 音频设置组
        let audio_frame = create_frame("音频");
        let audio_content = gtk4::Box::new(gtk4::Orientation::Vertical, 8);
        
        let silence_box = gtk4::Box::new(gtk4::Orientation::Horizontal, 12);
        let silence_label = gtk4::Label::new(Some("静音"));
        silence_label.set_hexpand(true);
        silence_label.set_halign(gtk4::Align::Start);
        let silence_switch = gtk4::Switch::new();
        silence_box.append(&silence_label);
        silence_box.append(&silence_switch);
        audio_content.append(&silence_box);
        audio_frame.set_child(Some(&audio_content));
        general_box.append(&audio_frame);

        widgets.content_stack.add_named(&general_box, Some("general"));

        // ========== Audio 子页面 ==========
        let audio_box = gtk4::Box::new(gtk4::Orientation::Vertical, 16);
        audio_box.set_margin_all(12);

        let audio_title = gtk4::Label::new(Some("音频设置"));
        audio_title.add_css_class("title-1");
        audio_title.set_halign(gtk4::Align::Start);
        audio_box.append(&audio_title);

        // 音量控制组
        let volume_frame = create_frame("音量控制");
        let volume_content = gtk4::Box::new(gtk4::Orientation::Vertical, 8);
        
        let volume_box = gtk4::Box::new(gtk4::Orientation::Horizontal, 12);
        let volume_label = gtk4::Label::new(Some("默认音量"));
        volume_label.set_hexpand(true);
        volume_label.set_halign(gtk4::Align::Start);
        let volume_scale = gtk4::Scale::with_range(gtk4::Orientation::Horizontal, 0.0, 100.0, 1.0);
        volume_scale.set_hexpand(true);
        volume_box.append(&volume_label);
        volume_box.append(&volume_scale);
        volume_content.append(&volume_box);
        volume_frame.set_child(Some(&volume_content));
        audio_box.append(&volume_frame);

        // 自动静音组
        let automute_frame = create_frame("自动静音");
        let automute_content = gtk4::Box::new(gtk4::Orientation::Vertical, 8);
        
        let automute_box = gtk4::Box::new(gtk4::Orientation::Horizontal, 12);
        let automute_label = gtk4::Label::new(Some("失去焦点时自动静音"));
        automute_label.set_hexpand(true);
        let automute_switch = gtk4::Switch::new();
        automute_box.append(&automute_label);
        automute_box.append(&automute_switch);
        automute_content.append(&automute_box);
        automute_frame.set_child(Some(&automute_content));
        audio_box.append(&automute_frame);

        widgets.content_stack.add_named(&audio_box, Some("audio"));

        // ========== Advanced 子页面 ==========
        let advanced_box = gtk4::Box::new(gtk4::Orientation::Vertical, 16);
        advanced_box.set_margin_all(12);

        let advanced_title = gtk4::Label::new(Some("高级设置"));
        advanced_title.add_css_class("title-1");
        advanced_title.set_halign(gtk4::Align::Start);
        advanced_box.append(&advanced_title);

        // 显示效果组
        let display_frame = create_frame("显示效果");
        let display_content = gtk4::Box::new(gtk4::Orientation::Vertical, 8);
        
        // 禁用鼠标交互
        let disable_mouse_box = gtk4::Box::new(gtk4::Orientation::Horizontal, 12);
        let disable_mouse_label = gtk4::Label::new(Some("禁用鼠标交互"));
        disable_mouse_label.set_hexpand(true);
        let disable_mouse_switch = gtk4::Switch::new();
        disable_mouse_box.append(&disable_mouse_label);
        disable_mouse_box.append(&disable_mouse_switch);
        display_content.append(&disable_mouse_box);
        
        // 禁用视差效果
        let disable_parallax_box = gtk4::Box::new(gtk4::Orientation::Horizontal, 12);
        let disable_parallax_label = gtk4::Label::new(Some("禁用视差效果"));
        disable_parallax_label.set_hexpand(true);
        let disable_parallax_switch = gtk4::Switch::new();
        disable_parallax_box.append(&disable_parallax_label);
        disable_parallax_box.append(&disable_parallax_switch);
        display_content.append(&disable_parallax_box);
        
        // 禁用粒子系统
        let disable_particles_box = gtk4::Box::new(gtk4::Orientation::Horizontal, 12);
        let disable_particles_label = gtk4::Label::new(Some("禁用粒子系统"));
        disable_particles_label.set_hexpand(true);
        let disable_particles_switch = gtk4::Switch::new();
        disable_particles_box.append(&disable_particles_label);
        disable_particles_box.append(&disable_particles_switch);
        display_content.append(&disable_particles_box);
        
        display_frame.set_child(Some(&display_content));
        advanced_box.append(&display_frame);

        // Wayland 设置组
        let wayland_frame = create_frame("Wayland");
        let wayland_content = gtk4::Box::new(gtk4::Orientation::Vertical, 8);
        
        let wayland_pause_box = gtk4::Box::new(gtk4::Orientation::Horizontal, 12);
        let wayland_pause_label = gtk4::Label::new(Some("全屏暂停仅限活动显示器"));
        wayland_pause_label.set_hexpand(true);
        let wayland_pause_switch = gtk4::Switch::new();
        wayland_pause_box.append(&wayland_pause_label);
        wayland_pause_box.append(&wayland_pause_switch);
        wayland_content.append(&wayland_pause_box);
        wayland_frame.set_child(Some(&wayland_content));
        advanced_box.append(&wayland_frame);

        widgets.content_stack.add_named(&advanced_box, Some("advanced"));

        // ========== Logs 子页面 ==========
        let logs_box = gtk4::Box::new(gtk4::Orientation::Vertical, 16);
        logs_box.set_margin_all(12);

        let logs_title = gtk4::Label::new(Some("日志"));
        logs_title.add_css_class("title-1");
        logs_title.set_halign(gtk4::Align::Start);
        logs_box.append(&logs_title);

        // 日志查看器
        let logs_frame = create_frame("日志查看器");
        let logs_content = gtk4::Box::new(gtk4::Orientation::Vertical, 8);
        
        let log_textview = gtk4::TextView::new();
        log_textview.set_editable(false);
        log_textview.set_monospace(true);
        log_textview.set_wrap_mode(gtk4::WrapMode::WordChar);
        log_textview.set_vexpand(true);
        // log_textview.set_min_content_height(200);
        logs_content.append(&log_textview);
        
        let logs_button_box = gtk4::Box::new(gtk4::Orientation::Horizontal, 12);
        logs_button_box.set_halign(gtk4::Align::End);
        
        let copy_button = gtk4::Button::with_label("复制");
        copy_button.add_css_class("pill");
        logs_button_box.append(&copy_button);
        
        let clear_button = gtk4::Button::with_label("清空");
        clear_button.add_css_class("destructive-action");
        logs_button_box.append(&clear_button);
        logs_content.append(&logs_button_box);
        
        logs_frame.set_child(Some(&logs_content));
        logs_box.append(&logs_frame);

        widgets.content_stack.add_named(&logs_box, Some("logs"));

        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, _sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {}
    }
}

fn create_frame(title: &str) -> gtk4::Frame {
    let frame = gtk4::Frame::new(Some(title));
    frame.set_margin_bottom(12);
    frame
}
