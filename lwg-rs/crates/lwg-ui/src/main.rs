use relm4::prelude::*;
use gtk4::prelude::*;
use gtk4::ApplicationWindow; // 移除了 Label，因为在 view! 里用的是 gtk::Label
use lwg_core::AppConfig;

// 1. 定义消息枚举
#[derive(Debug)]
enum AppInput {
    ConfigLoaded(Result<AppConfig, String>),
}

struct AppModel {
    config: Option<AppConfig>,
    error: Option<String>,
}

#[relm4::component]
impl SimpleComponent for AppModel {
    type Init = ();
    type Input = AppInput;
    type Output = ();

    view! {
        ApplicationWindow {
            set_title: Some("Linux Wallpaper Engine GUI (Rust)"),
            set_default_size: (800, 600),

            gtk::Box {
                set_orientation: gtk4::Orientation::Vertical,
                set_spacing: 5,
                set_margin_all: 10,

                gtk::Label {
                    // 2. 动态显示文本
                    #[watch]
                    set_text: &match (&model.config, &model.error) {
                        (Some(cfg), None) => {
                            format!("配置加载成功！\nWorkshop路径: {:?}", cfg.workshop_path)
                        },
                        (None, Some(err)) => {
                            format!("错误: {}", err)
                        },
                        _ => "正在加载配置...".to_string()
                    },
                }
            }
        }
    }

    fn init(_init: Self::Init, root: Self::Root, sender: ComponentSender<Self>) -> ComponentParts<Self> {
        let model = Self { 
            config: None, 
            error: None 
        };

        // 修正：加上 ||，表示这是一个闭包，该闭包返回 async 块
        sender.spawn_oneshot_command(|| async move {
            let result = AppConfig::load().await;
            
            match result {
                Ok(cfg) => AppInput::ConfigLoaded(Ok(cfg)),
                Err(e) => AppInput::ConfigLoaded(Err(e.to_string())),
            }
        });

        let widgets = view_output!();
        ComponentParts { model, widgets }
    }


    fn update(&mut self, message: Self::Input, _sender: ComponentSender<Self>) {
        match message {
            AppInput::ConfigLoaded(result) => {
                match result {
                    Ok(cfg) => {
                        println!("配置加载完成: {:?}", cfg);
                        self.config = Some(cfg);
                        self.error = None;
                    }
                    Err(e) => {
                        eprintln!("加载失败: {}", e);
                        self.error = Some(e);
                        self.config = None;
                    }
                }
            }
        }
    }
}

fn main() {
    tracing_subscriber::fmt::init();
    let app = RelmApp::new("com.github.Suhoiyis.lwg-ui");
    app.run::<AppModel>(());
}
