use gtk4::prelude::*;
use relm4::prelude::*;
use std::process::{Command, Stdio};
use std::env;
use std::path::Path;

/// 托盘管理器
pub struct TrayManager {
    process: Option<std::process::Child>,
    icon_path: String,
    parent_pid: u32,
}

#[derive(Debug)]
pub enum TrayManagerInput {
    Start,
    Stop,
    UpdateTooltip(String),
}

#[derive(Debug)]
pub enum TrayManagerOutput {
    Started,
    Stopped,
    Error(String),
}

#[relm4::component(pub)]
impl Component for TrayManager {
    type Init = ();
    type Input = TrayManagerInput;
    type Output = TrayManagerOutput;
    type CommandOutput = ();

    view! {
        gtk4::Box {
            set_visible: false,
        }
    }

    fn init(
        _init: Self::Init,
        _root: Self::Root,
        sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        let parent_pid = std::process::id();
        
        let model = Self {
            process: None,
            icon_path: Self::install_tray_icons(),
            parent_pid,
        };

        let widgets = view_output!();
        sender.input(TrayManagerInput::Start);

        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            TrayManagerInput::Start => {
                if let Err(e) = self.start_tray_process() {
                    eprintln!("Failed to start tray: {}", e);
                    sender.output(TrayManagerOutput::Error(format!("Failed to start tray: {}", e))).ok();
                } else {
                    sender.output(TrayManagerOutput::Started).ok();
                }
            }
            TrayManagerInput::Stop => {
                self.stop_tray_process();
                sender.output(TrayManagerOutput::Stopped).ok();
            }
            TrayManagerInput::UpdateTooltip(tooltip) => {
                eprintln!("Tooltip: {}", tooltip);
            }
        }
    }
}

impl TrayManager {
    fn install_tray_icons() -> String {
        use std::fs;
        
        let local_icon_dir = dirs::home_dir()
            .map(|d| d.join(".local/share/icons/hicolor/512x512/apps"))
            .unwrap_or_else(|| Path::new(".").to_path_buf());
        
        let _ = fs::create_dir_all(&local_icon_dir);
        
        let icon_sources = [
            "pic/icons/gui_tray_rounded.png",
            "pic/icons/GUI_rounded.png",
        ];
        
        let target_normal = local_icon_dir.join("com.wallpaperengine.tray.png");
        let target_stopped = local_icon_dir.join("com.wallpaperengine.tray-stopped.png");
        
        for src in &icon_sources {
            if Path::new(src).exists() {
                let _ = fs::copy(src, &target_normal);
                break;
            }
        }
        
        let _ = fs::copy(&target_normal, &target_stopped);
        
        "com.wallpaperengine.tray".to_string()
    }
    
    fn start_tray_process(&mut self) -> Result<(), String> {
        if let Some(ref mut process) = self.process {
            match process.try_wait() {
                Ok(Some(status)) => {
                    eprintln!("Tray exited: {:?}", status);
                    self.process = None;
                }
                Ok(None) => return Ok(()),
                Err(e) => {
                    eprintln!("Tray check error: {}", e);
                    self.process = None;
                }
            }
        }
        
        let tray_bin = self.find_tray_binary();
        eprintln!("Starting tray: {:?}", tray_bin);
        
        let mut cmd = Command::new(&tray_bin);
        cmd.env("LWG_TRAY_ICON", &self.icon_path)
            .env("LWG_IPC_SOCKET", &format!("lwg-ipc-{}", self.parent_pid))
            .env("LWG_TRAY_RX_SOCKET", &format!("lwg-tray-rx-{}", self.parent_pid))
            .env("LWG_PARENT_PID", self.parent_pid.to_string())
            .stdin(Stdio::null())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped());
        
        match cmd.spawn() {
            Ok(process) => {
                eprintln!("Tray started (PID: {})", process.id());
                self.process = Some(process);
                Ok(())
            }
            Err(e) => {
                eprintln!("Failed to start tray: {}", e);
                Err(format!("Failed to start tray: {}", e))
            }
        }
    }
    
    fn find_tray_binary(&self) -> String {
        if let Ok(path) = env::var("LWG_TRAY_BIN") {
            if Path::new(&path).exists() {
                return path;
            }
        }
        
        let current_dir = env::current_dir().unwrap_or_else(|_| Path::new(".").to_path_buf());
        let local_tray = current_dir.join("target/release/tray-rs");
        if local_tray.exists() {
            return local_tray.to_string_lossy().to_string();
        }
        
        if let Ok(path) = which::which("tray-rs") {
            return path.to_string_lossy().to_string();
        }
        
        "tray-rs".to_string()
    }
    
    fn stop_tray_process(&mut self) {
        if let Some(mut process) = self.process.take() {
            let _ = process.kill();
            let timeout = std::time::Duration::from_secs(3);
            let start = std::time::Instant::now();
            
            while start.elapsed() < timeout {
                match process.try_wait() {
                    Ok(Some(_)) => return,
                    Ok(None) => std::thread::sleep(std::time::Duration::from_millis(100)),
                    Err(_) => return,
                }
            }
            
            let _ = process.kill();
        }
    }
}

impl Drop for TrayManager {
    fn drop(&mut self) {
        self.stop_tray_process();
    }
}
