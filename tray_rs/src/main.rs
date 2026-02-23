use ksni::{menu::*, Icon, Tray, TrayService, ToolTip};
use std::env;
use std::fs;
use std::path::Path;
use std::sync::atomic::{AtomicBool, Ordering};
use std::thread;
use std::time::Duration;
use std::os::unix::net::{UnixStream, UnixListener};
use std::io::{Write, BufRead, BufReader};
use std::os::unix::fs::PermissionsExt;

static SHOULD_EXIT: AtomicBool = AtomicBool::new(false);

extern "C" fn handle_sigterm(_: libc::c_int) {
    SHOULD_EXIT.store(true, Ordering::Relaxed);
}

fn get_uid() -> u32 { unsafe { libc::getuid() } }

struct WallpaperTray {
    icon_path: String,
    socket_path: String,
    current_tooltip: String, // ✅ 新增：用于存储动态显示的文本
}

impl Tray for WallpaperTray {
    fn title(&self) -> String { "Wallpaper Engine GUI".into() }

    // fn tool_tip(&self) -> ToolTip {
    //     ToolTip {
    //         title: "Linux Wallpaper Engine GUI".into(),
    //         // ✅ 动态读取当前的壁纸状态
    //         description: self.current_tooltip.clone(),
    //         icon_name: "".into(),
    //         icon_pixmap: vec![],
    //     }
    // }

    fn tool_tip(&self) -> ToolTip {
        ToolTip {
            // 💡 绝杀：直接把动态状态拼接到主标题里，利用 \n 强制换行！
            // 这样不管什么桌面环境，都绝对拦截不了我们的状态显示！
            title: format!("<b>Wallpaper Engine GUI</b>\n{}", self.current_tooltip),
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

    // ✨ 捕获左键单击（Activate）事件
    fn activate(&mut self, _x: i32, _y: i32) {
        // 左键点击时，直接向 Python 发送 --toggle 指令！
        self.exec("--toggle");
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
            match UnixStream::connect(&socket_path) {
                Ok(mut stream) => {
                    if let Err(e) = stream.write_all(format!("{}\n", cmd_str).as_bytes()) {
                        log(&format!("Failed to write to IPC socket {}: {}", socket_path, e));
                    }
                }
                Err(e) => {
                    log(&format!("Failed to connect to IPC socket {}: {}", socket_path, e));
                }
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
        libc::signal(libc::SIGTERM, handle_sigterm as *const () as usize);
    }
    SHOULD_EXIT.store(false, Ordering::Relaxed);

    // ✅ 建立第二根 Socket 管道：专门用于接收 Python 发来的 Tooltip
    let rx_socket_path = format!("/tmp/lwg-tray-rx-{}.sock", get_uid());
    let _ = fs::remove_file(&rx_socket_path); 
    
    // 【核心修复】：防止 Socket 被占用时引发脏崩溃
    let listener = match UnixListener::bind(&rx_socket_path) {
        Ok(l) => l,
        Err(e) => {
            log(&format!("Failed to bind RX socket at {}: {}", rx_socket_path, e));
            std::process::exit(1);
        }
    };
    fs::set_permissions(&rx_socket_path, fs::Permissions::from_mode(0o600)).ok();

    let service = TrayService::new(WallpaperTray {
        icon_path,
        socket_path,
        current_tooltip: "Waiting for status...".into(),
    });

    let handle = service.handle();
    service.spawn();

    let handle_clone = handle.clone();
    // ✅ 开启独立后台线程，死循环监听 Python 的汇报
    thread::spawn(move || {
        for stream in listener.incoming() {
            match stream {
                Ok(stream) => {
                    let reader = BufReader::new(stream);
                    for line in reader.lines() {
                        if let Ok(text) = line {
                            // 收到新文本，通过 handle 安全地跨线程更新托盘状态！
                            handle_clone.update(|tray: &mut WallpaperTray| {
                                tray.current_tooltip = text;
                            });
                        }
                    }
                }
                Err(e) => log(&format!("RX socket accept error: {}", e)),
            }
        }
    });

    loop {
        thread::sleep(Duration::from_millis(500));

        if SHOULD_EXIT.load(Ordering::Relaxed) {
            log("Received SIGTERM. Exiting gracefully...");
            let _ = fs::remove_file(&rx_socket_path);
            thread::sleep(Duration::from_millis(500));
            log("Graceful exit complete.");
            std::process::exit(0);
        }

        if parent_pid > 0 && !pid_exists(parent_pid) {
            log("Parent process died. Exiting gracefully...");
            let _ = fs::remove_file(&rx_socket_path);
            thread::sleep(Duration::from_millis(500)); 
            std::process::exit(0);
        }
    }
}

fn pid_exists(pid: u32) -> bool { Path::new(&format!("/proc/{pid}")).exists() }

fn is_engine_running() -> bool {
    let Ok(entries) = fs::read_dir("/proc") else { return false; };
    for entry in entries.flatten() {
        let name = entry.file_name();
        let name = name.to_string_lossy();
        if !name.chars().all(|c| c.is_ascii_digit()) { continue; }
        
        let exe_path = entry.path().join("exe");
        if let Ok(target) = fs::read_link(&exe_path) {
            if let Some(fname) = target.file_name().and_then(|s| s.to_str()) {
                if fname == "linux-wallpaperengine" { return true; }
            }
        } else {
            let cmdline_path = entry.path().join("cmdline");
            if let Ok(bytes) = fs::read(&cmdline_path) {
                if let Some(pos) = bytes.iter().position(|&b| b == 0) {
                    let exec_path = String::from_utf8_lossy(&bytes[..pos]);
                    let exec_name = Path::new(exec_path.as_ref())
                        .file_name()
                        .and_then(|s| s.to_str())
                        .unwrap_or("");
                    if exec_name == "linux-wallpaperengine" { return true; }
                }
            }
        }
    }
    false
}

fn log(msg: &str) {
    if std::env::var("LWG_DEBUG").unwrap_or_default() != "1" {
        return;
    }
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