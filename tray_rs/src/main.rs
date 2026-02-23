use ksni::{menu::*, Icon, Tray, TrayService, ToolTip};
use std::env;
use std::fs;
use std::path::Path;
use std::process::Command;
use std::sync::atomic::{AtomicBool, Ordering};
use std::thread;
use std::time::Duration;

static SHOULD_EXIT: AtomicBool = AtomicBool::new(false);

extern "C" fn handle_sigterm(_: libc::c_int) {
    SHOULD_EXIT.store(true, Ordering::Relaxed);
}

fn get_uid() -> u32 { unsafe { libc::getuid() } }

struct WallpaperTray {
    icon_path: String,
    socket_path: String,
}

impl Tray for WallpaperTray {
    fn title(&self) -> String { "Wallpaper Engine GUI".into() }

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
        vec![
            MenuItem::Standard(StandardItem {
                label: "Show Window".into(),
                activate: Box::new(|tray: &mut Self| tray.exec("--show")),
                ..Default::default()
            }),
            MenuItem::Separator,
            MenuItem::Standard(StandardItem {
                label: "Play/Stop".into(),
                activate: Box::new(move |tray: &mut Self| {
                    if is_engine_running() {
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
        let socket_path = self.socket_path.clone();
        let cmd_str = arg.to_string();
        log(&format!("Exec clicked: {}", cmd_str));
        
        thread::spawn(move || {
            use std::os::unix::net::UnixStream;
            use std::io::Write;
            if let Ok(mut stream) = UnixStream::connect(&socket_path) {
                let _ = stream.write_all(format!("{}\n", cmd_str).as_bytes());
            }
        });
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let icon_path = args.get(1).cloned().unwrap_or_default();
    let parent_pid: u32 = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(0);

    let socket_path = std::env::var("LWG_IPC_SOCKET").unwrap_or_else(|_| {
        format!("/tmp/lwg-ipc-{}.sock", get_uid())
    });

    log(&format!("Starting. icon={icon_path} parent_pid={parent_pid} socket={socket_path}"));

    unsafe {
        libc::signal(libc::SIGTERM, handle_sigterm as libc::sighandler_t);
    }
    SHOULD_EXIT.store(false, Ordering::Relaxed);

    let service = TrayService::new(WallpaperTray {
        icon_path,
        socket_path,
    });
    
    let handle = service.spawn();

    loop {
        // 监控频率加快到 0.5 秒，保证退出响应足够迅速
        thread::sleep(Duration::from_millis(500));

        if SHOULD_EXIT.load(Ordering::Relaxed) {
            log("Received SIGTERM. Unregistering DBus...");
            drop(handle);
            thread::sleep(Duration::from_millis(500)); // ⏳ 核心绝杀：给后台发包留足 500ms！
            log("Graceful exit complete.");
            std::process::exit(0);
        }

        if parent_pid > 0 && !pid_exists(parent_pid) {
            log("Parent process died. Unregistering DBus...");
            drop(handle);
            thread::sleep(Duration::from_millis(500)); // ⏳ 核心绝杀：给后台发包留足 500ms！
            std::process::exit(0);
        }
    }
}

// 工具函数保持不变
fn pid_exists(pid: u32) -> bool { Path::new(&format!("/proc/{pid}")).exists() }

fn is_engine_running() -> bool {
    let Ok(entries) = fs::read_dir("/proc") else { return false; };
    for entry in entries.flatten() {
        let name = entry.file_name();
        let name = name.to_string_lossy();
        if !name.chars().all(|c| c.is_ascii_digit()) { continue; }
        let cmdline_path = entry.path().join("cmdline");
        if let Ok(bytes) = fs::read(&cmdline_path) {
            if let Some(pos) = bytes.iter().position(|&b| b == 0) {
                let exec_path = String::from_utf8_lossy(&bytes[..pos]);
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
    env::var("HOME").unwrap_or_else(|_| "/tmp".into()) + "/.cache/linux-wallpaperengine-gui"
}

fn chrono_now() -> String {
    std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap_or_default().as_secs().to_string()
}