use ksni::{menu::*, Icon, Tray, TrayService, ToolTip};
use std::env;
use std::fs;
use std::path::Path;
use std::process::Command;
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;

// ── 共享状态 ──────────────────────────────────────────────
#[derive(Clone)]
struct State {
    is_engine_running: bool,
}

// ── Tray 定义 ─────────────────────────────────────────────
struct WallpaperTray {
    icon_path: String,
    run_gui_path: String,
    state: Arc<Mutex<State>>,
}

impl Tray for WallpaperTray {
    fn title(&self) -> String {
        "Wallpaper Engine GUI".into()
    }

    // 🌟 修复 1：加上完美的鼠标悬浮提示 Tooltip
    fn tool_tip(&self) -> ToolTip {
        ToolTip {
            title: "Linux Wallpaper Engine GUI".into(),
            description: "".into(),
            icon_name: "".into(),
            icon_pixmap: vec![],
        }
    }

    fn icon_pixmap(&self) -> Vec<Icon> { vec![] } 

    fn icon_name(&self) -> String {
        if self.icon_path.starts_with('/') {
            self.icon_path.clone()
        } else {
            "preferences-desktop-wallpaper".into()
        }
    }

    fn menu(&self) -> Vec<MenuItem<Self>> {
        // 动态获取当前状态，供闭包内部使用
        let is_running = self.state.lock().unwrap().is_engine_running;

        vec![
            MenuItem::Standard(StandardItem {
                label: "Show Window".into(),
                activate: Box::new(|tray: &mut Self| tray.exec("--show")),
                ..Default::default()
            }),
            MenuItem::Separator,
            // 🌟 修复 2：恢复为你熟悉的 Play/Stop 单一菜单项
            MenuItem::Standard(StandardItem {
                label: "Play/Stop".into(),
                activate: Box::new(move |tray: &mut Self| {
                    // 点击时根据真实状态下发不同命令
                    if is_running {
                        tray.exec("--stop");
                    } else {
                        tray.exec("--apply-last");
                    }
                }),
                ..Default::default()
            }),
            MenuItem::Standard(StandardItem {
                label: "Random Wallpaper".into(),
                activate: Box::new(|tray: &mut Self| tray.exec("--random")),
                ..Default::default()
            }),
            MenuItem::Separator,
            MenuItem::Standard(StandardItem {
                label: "Quit Application".into(),
                activate: Box::new(|tray: &mut Self| tray.exec("--quit")),
                ..Default::default()
            }),
        ]
    }
}

impl WallpaperTray {
    fn exec(&self, arg: &str) {
        let path = self.run_gui_path.clone();
        let arg = arg.to_string();
        
        thread::spawn(move || {
            let mut cmd = if path.ends_with(".py") {
                let mut c = Command::new("python3");
                c.arg(&path).arg(&arg);
                c
            } else {
                let mut c = Command::new(&path);
                c.arg(&arg);
                c
            };

            cmd.env_remove("DESKTOP_STARTUP_ID")
               .env_remove("GIO_LAUNCHED_DESKTOP_FILE")
               .env_remove("LD_LIBRARY_PATH")
               .env_remove("PYTHONPATH")
               .env_remove("APPDIR")
               .env_remove("APPIMAGE")
               .env_remove("GTK_PATH")
               .env_remove("GTK_EXE_PREFIX")
               .env_remove("GTK_DATA_PREFIX")
               .env_remove("GDK_BACKEND")
               .env_remove("GDK_PIXBUF_MODULE_FILE")
               .env_remove("GI_TYPELIB_PATH");

            if let Err(e) = cmd.spawn() {
                log(&format!("Exec error: {e}"));
            }
        });
    }
}

// ── 入口 ──────────────────────────────────────────────────
fn main() {
    let args: Vec<String> = env::args().collect();
    let icon_path = args.get(1).cloned().unwrap_or_default();
    let parent_pid: u32 = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(0);
    let run_gui_path = args.get(3).cloned().unwrap_or_else(|| "run_gui.py".into());

    log(&format!("Starting. icon={icon_path} parent_pid={parent_pid} run_gui={run_gui_path}"));

    let state = Arc::new(Mutex::new(State {
        is_engine_running: false,
    }));

    let service = TrayService::new(WallpaperTray {
        icon_path,
        run_gui_path,
        state: state.clone(),
    });
    
    let handle = service.handle();
    service.spawn();

    let state_bg = state.clone();
    let handle_bg = handle.clone();
    
    thread::spawn(move || loop {
        thread::sleep(Duration::from_secs(2));

        if parent_pid > 0 && !pid_exists(parent_pid) {
            log("Parent process died. Exiting.");
            std::process::exit(0);
        }

        let running = is_engine_running();
        let mut s = state_bg.lock().unwrap();
        
        if s.is_engine_running != running {
            s.is_engine_running = running;
            drop(s);
            handle_bg.update(|_| {}); 
        }
    });

    loop {
        thread::sleep(Duration::from_secs(3600));
    }
}

// ── 工具函数 ──────────────────────────────────────────────

fn pid_exists(pid: u32) -> bool {
    Path::new(&format!("/proc/{pid}")).exists()
}

// 🌟 修复 3：硬核且精准的进程甄别器
fn is_engine_running() -> bool {
    let Ok(entries) = fs::read_dir("/proc") else { return false; };
    for entry in entries.flatten() {
        let name = entry.file_name();
        let name = name.to_string_lossy();
        if !name.chars().all(|c| c.is_ascii_digit()) { continue; }
        
        let cmdline_path = entry.path().join("cmdline");
        if let Ok(bytes) = fs::read(&cmdline_path) {
            // 解析出 cmdline 中的第一个参数（即可执行文件路径）
            if let Some(first_null_pos) = bytes.iter().position(|&b| b == 0) {
                let exec_path = String::from_utf8_lossy(&bytes[..first_null_pos]);
                // 只有当真正的执行文件是 linux-wallpaperengine 时，才算作引擎运行
                // 这样能完美避开目录名包含该字符串造成的误伤
                if exec_path.ends_with("/linux-wallpaperengine") || exec_path == "linux-wallpaperengine" {
                    return true;
                }
            }
        }
    }
    false
}

fn log(msg: &str) {
    use std::io::Write;
    let dir = dirs_next();
    let _ = fs::create_dir_all(&dir);
    let path = format!("{dir}/tray_crash.log");
    if let Ok(mut f) = fs::OpenOptions::new().append(true).create(true).open(&path) {
        let ts = chrono_now();
        let _ = writeln!(f, "[{ts}] [TRAY-RS] {msg}");
    }
}

fn dirs_next() -> String {
    env::var("HOME").unwrap_or_else(|_| "/tmp".into())
        + "/.cache/linux-wallpaperengine-gui"
}

fn chrono_now() -> String {
    std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap_or_default()
        .as_secs()
        .to_string()
}