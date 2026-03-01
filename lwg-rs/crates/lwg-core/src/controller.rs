use crate::config::AppConfig;
use crate::error::{LwgError, LwgResult};
use std::collections::HashMap;
use std::fs::File;
use std::io::Write;
use std::path::PathBuf;
use std::process::{Child, Command, Stdio};
use std::sync::Arc;
use std::time::Duration;
use tokio::sync::Mutex;
use tracing::{debug, error, info, warn};

pub struct WallpaperController {
    config: Arc<Mutex<AppConfig>>,
    current_proc: Option<Child>,
    last_command: Vec<String>,
    engine_log: Option<File>,
    log_path: PathBuf,
}

impl WallpaperController {
    /// 创建新的控制器
    pub fn new(config: Arc<Mutex<AppConfig>>) -> Self {
        // 获取日志文件路径
        let config_dir = dirs::config_dir()
            .unwrap_or_else(|| std::path::PathBuf::from("."))
            .join("linux-wallpaperengine-gui");
        let log_path = config_dir.join("engine_last.log");
        
        Self {
            config,
            current_proc: None,
            last_command: Vec::new(),
            engine_log: None,
            log_path,
        }
    }
    
    /// 应用壁纸到指定显示器
    pub async fn apply(&mut self, wallpaper_id: &str, screen: Option<&str>) -> LwgResult<()> {
        let mut config = self.config.lock().await;
        
        let target_screens = if let Some(s) = screen {
            vec![s.to_string()]
        } else if let Some(last) = &config.last_screen {
            vec![last.clone()]
        } else {
            vec!["eDP-1".to_string()]
        };
        
        for s in &target_screens {
            config.active_monitors.insert(s.clone(), wallpaper_id.to_string());
        }
        config.last_wallpaper = Some(wallpaper_id.to_string());
        
        if target_screens.len() == 1 {
            config.last_screen = Some(target_screens[0].clone());
        }
        
        info!(
            "Applying wallpaper {} to {:?}",
            wallpaper_id, target_screens
        );
        
        drop(config);
        self.restart_wallpapers().await
    }
    
    /// 应用壁纸到多个显示器
    pub async fn apply_to_screens(&mut self, wallpaper_id: &str, screens: &[String]) -> LwgResult<()> {
        let mut config = self.config.lock().await;
        
        for s in screens {
            config.active_monitors.insert(s.clone(), wallpaper_id.to_string());
        }
        config.last_wallpaper = Some(wallpaper_id.to_string());
        
        info!(
            "Applying wallpaper {} to screens: {:?}",
            wallpaper_id, screens
        );
        
        drop(config);
        self.restart_wallpapers().await
    }
    
    /// 停止指定显示器的壁纸
    pub async fn stop_screen(&mut self, screen: &str) -> LwgResult<()> {
        let mut config = self.config.lock().await;
        
        if config.active_monitors.remove(screen).is_some() {
            info!("Stopped wallpaper on {}", screen);
            
            if config.active_monitors.is_empty() {
                drop(config);
                self.stop().await;
            } else {
                drop(config);
                self.restart_wallpapers().await?;
            }
        }
        
        Ok(())
    }
    
    /// 重启所有活动的壁纸
    pub async fn restart_wallpapers(&mut self) -> LwgResult<()> {
        self.stop().await;
        
        let config = self.config.lock().await;
        let active_monitors: HashMap<_, _> = config.active_monitors.clone();
        
        if active_monitors.is_empty() {
            info!("No active wallpapers");
            return Ok(());
        }
        
        let mut cmd = Command::new("linux-wallpaperengine");
        
        // 添加显示器参数
        for (screen, wp_id) in &active_monitors {
            cmd.arg("--screen-root").arg(screen);
            cmd.arg("--bg").arg(wp_id);
        }
        
        // 全局参数
        cmd.arg("-f").arg(config.fps.to_string());
        
        // 音频相关
        if config.silence {
            cmd.arg("--silent");
        } else {
            cmd.arg("--volume").arg(config.volume.to_string());
        }
        
        // 缩放模式
        if config.scaling != "default" {
            cmd.arg("--scaling").arg(&config.scaling);
        }
        
        // 其他选项
        if config.no_fullscreen_pause {
            cmd.arg("--no-fullscreen-pause");
        }
        if config.disable_mouse {
            cmd.arg("--disable-mouse");
        }
        if config.no_auto_mute {
            cmd.arg("--noautomute");
        }
        if config.no_audio_processing {
            cmd.arg("--no-audio-processing");
        }
        if config.disable_parallax {
            cmd.arg("--disable-parallax");
        }
        if config.disable_particles {
            cmd.arg("--disable-particles");
        }
        if config.clamping != "clamp" {
            cmd.arg("--clamp").arg(&config.clamping);
        }
        if config.wayland_only_active {
            cmd.arg("--fullscreen-pause-only-active");
        }
        
        // 忽略的应用 ID
        if !config.wayland_ignore_appids.is_empty() {
            for appid in config.wayland_ignore_appids.split(',') {
                let appid = appid.trim();
                if !appid.is_empty() {
                    cmd.arg("--fullscreen-pause-ignore-appid").arg(appid);
                }
            }
        }
        
        // 资源路径
        if let Some(assets) = &config.assets_path {
            cmd.arg("--assets-dir").arg(assets);
        }
        
        // 属性设置
        let is_silent = config.silence;
        let audio_props: std::collections::HashSet<_> = [
            "musicvolume", "music", "bellvolume", "sound", "soundsettings", "volume"
        ].iter().cloned().collect();
        
        for (_wp_id, props) in &config.wallpaper_properties {
            if let serde_json::Value::Object(map) = props {
                for (prop_name, prop_value) in map {
                    // 静音模式下跳过音频属性
                    if is_silent && audio_props.contains(prop_name.as_str()) {
                        continue;
                    }
                    
                    let formatted = match prop_value {
                        serde_json::Value::Bool(b) => b.to_string(),
                        serde_json::Value::Number(n) => n.to_string(),
                        serde_json::Value::String(s) => s.clone(),
                        _ => prop_value.to_string(),
                    };
                    
                    cmd.arg("--set-property")
                        .arg(format!("{}={}", prop_name, formatted));
                }
            }
        }
        
        let command_vec: Vec<String> = cmd
            .get_args()
            .map(|s| s.to_string_lossy().to_string())
            .collect();
        
        debug!("Executing: linux-wallpaperengine {:?}", command_vec);
        
        // 创建日志目录
        if let Some(parent) = self.log_path.parent() {
            let _ = std::fs::create_dir_all(parent);
        }
        
        // 打开日志文件
        let engine_log = match File::create(&self.log_path) {
            Ok(f) => f,
            Err(e) => {
                error!("Failed to create log file: {}", e);
                return Err(LwgError::ProcessError(format!("Failed to create log file: {}", e)));
            }
        };
        
        // 启动进程，将 stdout/stderr 重定向到日志文件
        // 设置 LD_LIBRARY_PATH 以找到 libcef.so 等库
        let child = cmd
            .env("LD_LIBRARY_PATH", "/opt/linux-wallpaperengine:/opt/linux-wallpaperengine/lib")
            .stdout(engine_log.try_clone().unwrap_or_else(|_| File::create(&self.log_path).unwrap()))
            .stderr(engine_log.try_clone().unwrap_or_else(|_| File::create(&self.log_path).unwrap()))
            .stdin(Stdio::null())
            .spawn();
        
        match child {
            Ok(mut child) => {
                let pid = child.id();
                info!("Engine started (PID: {:?}), checking if process stays alive...", pid);
                
                // 保存进程和日志文件句柄
                self.current_proc = Some(child);
                self.engine_log = Some(engine_log);
                self.last_command = command_vec;
                
                // 等待 0.5 秒检查进程是否存活
                std::thread::sleep(Duration::from_millis(500));
                
                // 检查进程是否已退出
                if let Some(ref mut proc) = self.current_proc {
                    match proc.try_wait() {
                        Ok(Some(status)) => {
                            // 进程已退出，读取日志内容报告错误
                            error!("Engine process exited immediately with status: {}", status);
                            
                            let log_content = std::fs::read_to_string(&self.log_path)
                                .unwrap_or_else(|_| "Unable to read log file".to_string());
                            
                            // 关闭日志文件句柄
                            self.engine_log = None;
                            self.current_proc = None;
                            
                            Err(LwgError::ProcessError(format!(
                                "Engine exited immediately!\nStatus: {}\nLog:\n{}", 
                                status, log_content
                            )))
                        }
                        Ok(None) => {
                            // 进程仍在运行
                            info!("Engine is running successfully (PID: {:?})", pid);
                            Ok(())
                        }
                        Err(e) => {
                            error!("Failed to check process status: {}", e);
                            Err(LwgError::ProcessError(format!("Failed to check process status: {}", e)))
                        }
                    }
                } else {
                    Ok(())
                }
            }
            Err(e) => {
                error!("Failed to start engine: {}", e);
                Err(LwgError::ProcessError(e.to_string()))
            }
        }
    }
    
    /// 停止所有壁纸
    pub async fn stop(&mut self) {
        info!("Stopping wallpaper");
        
        // 关闭日志文件句柄
        if let Some(mut log) = self.engine_log.take() {
            let _ = log.flush();
        }
        
        if let Some(mut child) = self.current_proc.take() {
            let _ = child.kill();
        }
        
        // 确保所有引擎进程都被终止
        let _ = Command::new("pkill")
            .args(["-f", "linux-wallpaperengine"])
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .status();
    }
    pub fn is_running(&self) -> bool {
        if let Some(pid) = self.current_proc.as_ref().map(|c| c.id()) {
            std::path::Path::new(&format!("/proc/{}", pid)).exists()
        } else {
            false
        }
    }
    
    /// 获取最后使用的命令
    pub fn last_command(&self) -> &[String] {
        &self.last_command
    }
    
    /// 获取当前进程 ID
    pub fn current_pid(&self) -> Option<u32> {
        self.current_proc.as_ref().map(|c| c.id())
    }
}

/// 截图管理器
pub struct ScreenshotManager {
    config: Arc<Mutex<AppConfig>>,
}

impl ScreenshotManager {
    /// 创建新的截图管理器
    pub fn new(config: Arc<Mutex<AppConfig>>) -> Self {
        Self { config }
    }
    
    /// 截取壁纸截图
    pub async fn take_screenshot(
        &self,
        wallpaper_id: &str,
        output_path: impl AsRef<std::path::Path>,
    ) -> LwgResult<Child> {
        let config = self.config.lock().await;
        
        let delay = config.screenshot_delay;
        let res = config.screenshot_res.clone();
        let prefer_xvfb = config.prefer_xvfb;
        let assets_path = config.assets_path.clone();
        
        drop(config);
        
        // 检查 Xvfb 可用性
        let has_xvfb = prefer_xvfb && which::which("xvfb-run").is_ok();
        
        // 基础命令
        let mut args = vec![
            "--screenshot".to_string(),
            output_path.as_ref().to_string_lossy().to_string(),
            "--screenshot-delay".to_string(),
            delay.to_string(),
            "--silent".to_string(),
            "-f".to_string(),
            "60".to_string(),
            wallpaper_id.to_string(),
        ];
        
        if let Some(assets) = assets_path {
            args.push("--assets-dir".to_string());
            args.push(assets);
        }
        
        let mut cmd = if has_xvfb {
            // 使用 Xvfb
            let mut cmd = Command::new("xvfb-run");
            cmd.arg("-a")
                .arg("-s")
                .arg(format!("-screen 0 {}x24 +extension GLX", res))
                .arg("linux-wallpaperengine")
                .args(&args)
                .arg("--window")
                .arg(format!("0x0x{}", res));
            
            // 设置 X11 环境变量
            cmd.env_remove("WAYLAND_DISPLAY");
            cmd.env("XDG_SESSION_TYPE", "x11");
            cmd.env("SDL_VIDEODRIVER", "x11");
            cmd.env("GDK_BACKEND", "x11");
            cmd.env("LIBGL_ALWAYS_SOFTWARE", "1");
            
            cmd
        } else {
            // 不使用 Xvfb
            let mut cmd = Command::new("linux-wallpaperengine");
            cmd.args(&args)
                .arg("--window")
                .arg(format!("0x0x{}", res));
            cmd
        };
        
        info!("Starting screenshot for wallpaper {}", wallpaper_id);
        
        match cmd.spawn() {
            Ok(child) => Ok(child),
            Err(e) => Err(LwgError::ScreenshotError(e.to_string())),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    // 这些测试需要实际环境，这里仅作为结构验证
    #[test]
    fn test_controller_creation() {
        let config = Arc::new(Mutex::new(AppConfig::default()));
        let _controller = WallpaperController::new(config);
    }
}