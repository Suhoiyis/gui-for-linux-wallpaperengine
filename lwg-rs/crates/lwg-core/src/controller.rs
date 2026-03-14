use crate::config::AppConfig;
use crate::logger::{LogManager, LogLevel, LogSource};
use crate::error::{LwgError, LwgResult};
use crate::performance::PerformanceMonitor;
use crate::state::{ActiveWallpaper, AppState, StateManager};
use std::collections::HashMap;
use std::process::{Child, Command, Stdio};
#[cfg(target_os = "linux")]
use std::os::unix::process::CommandExt;
use std::sync::Arc;
use std::time::Duration;
use tokio::sync::Mutex;
use tracing::{debug, error, info};

pub struct WallpaperController {
    config: Arc<Mutex<AppConfig>>,
    state: Arc<Mutex<AppState>>,
    current_proc: Option<Child>,
    detected_pids: HashMap<String, u32>,  // 检测到的进程 PID (屏幕 → PID)
    last_command: Vec<String>,
    performance_monitor: Option<Arc<std::sync::Mutex<PerformanceMonitor>>>,
    log_manager: Option<Arc<std::sync::Mutex<LogManager>>>,
}

impl WallpaperController {
    /// 创建新的控制器
    pub fn new(config: Arc<Mutex<AppConfig>>, state: Arc<Mutex<AppState>>) -> Self {
        Self {
            config,
            state,
            current_proc: None,
            detected_pids: HashMap::new(),
            last_command: Vec::new(),
            performance_monitor: None,
            log_manager: None,
        }
    }

    fn save_state(state: &AppState) -> LwgResult<()> {
        let mut state_manager = StateManager::new()?;
        state_manager.state = state.clone();
        state_manager.save()
    }



    pub fn set_state(&mut self, state: Arc<Mutex<AppState>>) {
        self.state = state;
    }

    pub fn set_performance_monitor(&mut self, monitor: Arc<std::sync::Mutex<PerformanceMonitor>>) {
        self.performance_monitor = Some(monitor);
    }

    pub fn set_log_manager(&mut self, manager: Arc<std::sync::Mutex<LogManager>>) {
        self.log_manager = Some(manager);
    }
    
    /// Set detected process PIDs (called on startup when接管 existing processes)
    pub fn set_detected_pids(&mut self, pids: HashMap<String, u32>) {
        self.detected_pids = pids;
    }
    /// 应用壁纸到指定显示器
    pub async fn apply(&mut self, wallpaper_id: &str, screen: Option<&str>) -> LwgResult<()> {
        let mut state = self.state.lock().await;
        
        let target_screens = match screen {
            Some(s) => vec![s.to_string()],
            None => vec!["eDP-1".to_string()],
        };
        
        for s in &target_screens {
            state.insert(s.clone(), ActiveWallpaper::new(wallpaper_id));
        }
        
        // Clone state for I/O, then release lock before blocking operation
        let state_clone = state.clone();
        drop(state);
        
        Self::save_state(&state_clone)?;
        
        info!(
            "Applying wallpaper {} to {:?}",
            wallpaper_id, target_screens
        );
        
        self.restart_wallpapers().await
    }


    /// 应用壁纸到多个显示器
    pub async fn apply_to_screens(&mut self, wallpaper_id: &str, screens: &[String]) -> LwgResult<()> {
        let mut state = self.state.lock().await;
        
        for s in screens {
            state.insert(s.clone(), ActiveWallpaper::new(wallpaper_id));
        }
        
        // Clone state for I/O, then release lock before blocking operation
        let state_clone = state.clone();
        drop(state);
        
        Self::save_state(&state_clone)?;
        
        info!(
            "Applying wallpaper {} to screens: {:?}",
            wallpaper_id, screens
        );
        
        self.restart_wallpapers().await
    }



    
    /// 停止指定显示器的壁纸
    pub async fn stop_screen(&mut self, screen: &str) -> LwgResult<()> {
        let mut state = self.state.lock().await;
        
        // 检查是否有检测到的进程需要杀死
        if let Some(&pid) = self.detected_pids.get(screen) {
            info!("Killing detected process {} for screen {}", pid, screen);
            Self::kill_process_by_pid(pid);
            self.detected_pids.remove(screen);
        }
        
        // 设置该屏幕的壁纸为停止状态
        if let Some(aw) = state.get_mut(screen) {
            aw.is_playing = false;
            info!("Stopped wallpaper on {}", screen);
        }
        
        let state_clone = state.clone();
        drop(state);
        
        Self::save_state(&state_clone)?;
        
        // 检查是否所有壁纸都已停止
        let all_stopped = state_clone.values().all(|aw| !aw.is_playing);
        if all_stopped {
            self.stop().await;
        } else {
            // 只有当我们自己启动的进程存在时才需要重启
            if self.current_proc.is_some() {
                self.restart_wallpapers().await?;
            }
        }
        
        Ok(())
    }


    
    /// 重启所有活动的壁纸
    pub async fn restart_wallpapers(&mut self) -> LwgResult<()> {
        self.kill_all_processes().await;
        
        let state = self.state.lock().await;
        let active_monitors: HashMap<_, _> = state.clone();
        drop(state);

        let config = self.config.lock().await;
        
        if active_monitors.is_empty() {
            info!("No active wallpapers");
            return Ok(());
        }
        
        let mut cmd = Command::new("/opt/linux-wallpaperengine/linux-wallpaperengine");
        
        // 添加显示器参数
        for (screen, aw) in &active_monitors {
            cmd.arg("--screen-root").arg(screen);
            cmd.arg("--bg").arg(&aw.wallpaper_id);
        }
        
        // 全局参数
        cmd.arg("-f").arg(config.fps.to_string());
        
        // 音频相关 - silence 为最高优先级
        if config.silence {
            cmd.arg("--silent");
        } else {
            cmd.arg("--volume").arg(config.volume.to_string());
            if config.no_auto_mute {
                cmd.arg("--noautomute");
            }
            if config.no_audio_processing {
                cmd.arg("--no-audio-processing");
            }
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
        
        
        // 启动进程，使用 piped stdout/stderr 进行实时捕获
        let child = cmd
            .env("LD_LIBRARY_PATH", "/opt/linux-wallpaperengine:/opt/linux-wallpaperengine/lib")
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .stdin(Stdio::null())
            .spawn();
        
        match child {
            Ok(mut child) => {
                let pid = child.id();
                info!("Engine started (PID: {:?}), checking if process stays alive...", pid);
                
                // Log to LogManager
                if let Some(ref lm) = self.log_manager {
                    if let Ok(m) = lm.lock() {
                        m.info(LogSource::Controller, &format!("Engine started with PID: {:?}", pid));
                    }
                }
                
                // 获取 stdout 和 stderr
                let stdout = child.stdout.take();
                let stderr = child.stderr.take();
                
                // 克隆 log_manager 用于线程
                let log_manager = self.log_manager.clone();
                
                // 启动线程读取 stdout
                if let Some(stdout) = stdout {
                    let lm = log_manager.clone();
                    std::thread::spawn(move || {
                        use std::io::{BufRead, BufReader};
                        let reader = BufReader::new(stdout);
                        for line in reader.lines() {
                            if let Ok(line) = line {
                                if let Some(ref manager) = lm {
                                    if let Ok(m) = manager.lock() {
                                        m.log(LogLevel::Info, LogSource::Engine, &line);
                                    }
                                }
                            }
                        }
                    });
                }
                
                // 启动线程读取 stderr
                if let Some(stderr) = stderr {
                    let lm = log_manager.clone();
                    std::thread::spawn(move || {
                        use std::io::{BufRead, BufReader};
                        let reader = BufReader::new(stderr);
                        for line in reader.lines() {
                            if let Ok(line) = line {
                                if let Some(ref manager) = lm {
                                    if let Ok(m) = manager.lock() {
                                        m.log(LogLevel::Error, LogSource::Engine, &line);
                                    }
                                }
                            }
                        }
                    });
                }
                
                // 保存进程
                self.current_proc = Some(child);
                self.last_command = command_vec;
                
                // 等待 0.5 秒检查进程是否存活
                std::thread::sleep(Duration::from_millis(500));
                
                // 检查进程是否已退出
                if let Some(ref mut proc) = self.current_proc {
                    match proc.try_wait() {
                        Ok(Some(status)) => {
                            // 进程已退出，从 LogManager 获取日志
                            error!("Engine process exited immediately with status: {}", status);
                            
                            let log_content = if let Some(ref lm) = self.log_manager {
                                if let Ok(m) = lm.lock() {
                                    m.get_logs()
                                        .iter()
                                        .filter(|l| l.source == LogSource::Engine)
                                        .map(|l| l.message.as_str())
                                        .collect::<Vec<_>>()
                                        .join("\n")
                                } else {
                                    "Unable to read logs".to_string()
                                }
                            } else {
                                "No log manager available".to_string()
                            };
                            
                            self.current_proc = None;
                            
                            Err(LwgError::ProcessError(format!(
                                "Engine exited immediately!\nStatus: {}\nLog:\n{}", 
                                status, log_content
                            )))
                        }
                        Ok(None) => {
                            // 进程仍在运行
                            info!("Engine is running successfully (PID: {:?})", pid);
                            // Register backend process for performance monitoring
                            if let Some(ref monitor) = self.performance_monitor {
                                if let Ok(mut mon) = monitor.lock() {
                                    mon.register_process("backend", pid as usize);
                                }
                            }
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
        
        if let Some(ref lm) = self.log_manager {
            if let Ok(m) = lm.lock() {
                m.info(LogSource::Controller, "Stopping wallpaper engine");
            }
        }
        
        // 更新 state：设置所有 is_playing = false
        {
            let mut state = self.state.lock().await;
            for aw in state.values_mut() {
                aw.is_playing = false;
            }
            // 保存 state
            let state_clone = state.clone();
            drop(state);
            let _ = Self::save_state(&state_clone);
        }
        
        // 杀死所有进程（不修改 state）
        self.kill_all_processes().await;
    }

    /// 仅杀死所有引擎进程，不修改 state
    /// 供 restart_wallpapers() 使用，避免在重启时丢失 is_playing 状态
    async fn kill_all_processes(&mut self) {
        // 杀死所有检测到的进程
        for (screen, &pid) in &self.detected_pids.clone() {
            info!("Killing detected process {} for screen {}", pid, screen);
            Self::kill_process_by_pid(pid);
        }
        self.detected_pids.clear();
        
        // Unregister backend process from performance monitoring
        if let Some(ref monitor) = self.performance_monitor {
            if let Ok(mut mon) = monitor.lock() {
                mon.unregister_process("backend");
            }
        }
        
        
        if let Some(mut child) = self.current_proc.take() {
            let _ = child.kill();
        }
        
        // 确保所有引擎进程都被终止
        let _ = Command::new("pkill")
            .args(["-f", "/opt/linux-wallpaperengine/linux-wallpaperengine"])
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
    
    /// 获取当前活跃壁纸信息
    pub async fn get_active_wallpapers(&self) -> HashMap<String, ActiveWallpaper> {
        let state = self.state.lock().await;
        state.clone()
    }

    /// 检查是否有活跃壁纸
    pub async fn is_wallpaper_running(&self) -> bool {
        let state = self.state.lock().await;
        state.values().any(|wallpaper| wallpaper.is_playing)
    }

    /// 同步状态（从外部状态源更新控制器的内部状态）
    pub async fn sync_state(&mut self, new_state: AppState) {
        let mut state = self.state.lock().await;
        *state = new_state;
        info!("Controller state synced");
    }
    
    // ================= 进程检测与接管 =================
    
    /// 检测已运行的 linux-wallpaperengine 进程
    /// 返回 HashMap<屏幕名, (PID, 壁纸ID)>
    pub fn detect_existing_processes() -> HashMap<String, (u32, String)> {
        let mut result = HashMap::new();
        
        // 遍历 /proc 目录
        if let Ok(entries) = std::fs::read_dir("/proc") {
            for entry in entries.flatten() {
                let name = entry.file_name();
                let name_str = name.to_string_lossy();
                
                // 只处理数字目录（PID）
                if let Ok(pid) = name_str.parse::<u32>() {
                    let cmdline_path = format!("/proc/{}/cmdline", pid);
                    
                    if let Ok(cmdline) = std::fs::read_to_string(&cmdline_path) {
                        if cmdline.contains("linux-wallpaperengine") {
                            // 解析参数
                            if let Some((screen, wp_id)) = Self::parse_screen_and_bg(&cmdline) {
                                result.insert(screen, (pid, wp_id));
                            }
                        }
                    }
                }
            }
        }
        
        result
    }
    
    /// 解析 cmdline 中的 --screen-root 和 --bg 参数
    fn parse_screen_and_bg(cmdline: &str) -> Option<(String, String)> {
        let args: Vec<&str> = cmdline.split('\0').collect();
        
        let mut screen = None;
        let mut wp_id = None;
        
        let mut i = 0;
        while i < args.len() {
            match args[i] {
                "--screen-root" if i + 1 < args.len() => {
                    screen = Some(args[i + 1].to_string());
                    i += 2;
                    continue;
                }
                "--bg" if i + 1 < args.len() => {
                    wp_id = Some(args[i + 1].to_string());
                    i += 2;
                    continue;
                }
                _ => {}
            }
            i += 1;
        }
        
        match (screen, wp_id) {
            (Some(s), Some(w)) => Some((s, w)),
            _ => None,
        }
    }
    
    /// 通过 PID 杀死进程 (SIGTERM)
    pub fn kill_process_by_pid(pid: u32) -> bool {
        Command::new("kill")
            .arg(pid.to_string())
            .output()
            .map(|o| o.status.success())
            .unwrap_or(false)
    }
    
    /// 强制杀死进程 (SIGKILL)
    pub fn kill_process_by_pid_force(pid: u32) -> bool {
        Command::new("kill")
            .arg("-9")
            .arg(pid.to_string())
            .output()
            .map(|o| o.status.success())
            .unwrap_or(false)
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
        
        // 检查 Xvfb 可用性
        let has_xvfb = prefer_xvfb && which::which("xvfb-run").is_ok();
        
        // 创建错误日志文件，对齐 Python 逻辑
        let err_log = std::fs::File::create("/tmp/wallpaper_screenshot_error.log")
            .unwrap_or_else(|_| std::fs::File::create("/dev/null").unwrap());
        
        let mut cmd = if has_xvfb {
            // 使用 Xvfb - 使用绝对路径调用二进制
            let mut cmd = Command::new("xvfb-run");
            cmd.arg("-a")
                .arg("-s")
                .arg(format!("-screen 0 {}x24 +extension GLX", res))
                .arg("/opt/linux-wallpaperengine/linux-wallpaperengine")  // 绝对路径
                .args(&args)
                .arg("--window")
                .arg(format!("0x0x{}", res));
            
            // 设置 X11 环境变量
            cmd.env_remove("WAYLAND_DISPLAY");
            cmd.env("XDG_SESSION_TYPE", "x11");
            cmd.env("SDL_VIDEODRIVER", "x11");
            cmd.env("GDK_BACKEND", "x11");
            cmd.env("LIBGL_ALWAYS_SOFTWARE", "1");
            // 关键：设置动态库路径
            cmd.env("LD_LIBRARY_PATH", "/opt/linux-wallpaperengine:/opt/linux-wallpaperengine/lib");
            // 设置工作目录
            cmd.current_dir("/opt/linux-wallpaperengine");
            
            info!("Starting screenshot: Silent (Xvfb) at {}", res);
            cmd
        } else {
            // Fallback: 窗口模式 - 使用绝对路径
            let mut cmd = Command::new("/opt/linux-wallpaperengine/linux-wallpaperengine");
            cmd.args(&args)
                .arg("--window")
                .arg(format!("0x0x{}", res));
            // 设置动态库路径
            cmd.env("LD_LIBRARY_PATH", "/opt/linux-wallpaperengine:/opt/linux-wallpaperengine/lib");
            cmd.current_dir("/opt/linux-wallpaperengine");
            
            info!("Starting screenshot: Windowed at {} (Xvfb not found)", res);
            cmd
        };
        
        // 静默标准输出，捕获错误输出
        cmd.stdout(std::process::Stdio::null());
        cmd.stderr(std::process::Stdio::from(err_log));
        
        // 创建新进程组，这样可以通过 kill -<pid> 杀死整个进程树
        cmd.process_group(0);
        
        info!("Starting screenshot for wallpaper {}", wallpaper_id);
        
        match cmd.spawn() {
            Ok(child) => Ok(child),
            Err(e) => Err(LwgError::ScreenshotError(e.to_string())),
    }
        }
    
    /// 截取壁纸截图并启动监控
    pub async fn take_screenshot_with_monitor(
        &self,
        wallpaper_id: &str,
        output_path: impl AsRef<std::path::Path>,
        perf_monitor: Arc<std::sync::Mutex<crate::performance::PerformanceMonitor>>,
    ) -> LwgResult<(Child, crate::performance::TaskTracker)> {
        // 启动截图进程
        let child = self.take_screenshot(wallpaper_id, &output_path).await?;
        let pid = child.id() as usize;
        
        // 启动性能监控
        let tracker = {
            let mut monitor = perf_monitor.lock().map_err(|e| LwgError::ProcessError(format!("Lock error: {}", e)))?;
            monitor.start_task("screenshot", pid)
        };
        Ok((child, tracker))
    }
    /// 等待截图完成（基于文件稳定性检测）
    /// linux-wallpaperengine --screenshot 不会自动退出，需要手动终止
    pub async fn wait_for_screenshot(
        child: &mut Child,
        output_path: &str,
        timeout_secs: u64,
        perf_monitor: Option<Arc<std::sync::Mutex<crate::performance::PerformanceMonitor>>>,
        tracker: Option<&crate::performance::TaskTracker>,
    ) -> LwgResult<std::process::ExitStatus> {
        use tokio::time::{timeout, Duration};
        
        let mut last_size: u64 = 0;
        let mut stable_count: u32 = 0;
        
        let result = timeout(
            Duration::from_secs(timeout_secs),
            async {
                loop {
                    // 采样性能数据
                    if let (Some(monitor), Some(tr)) = (&perf_monitor, &tracker) {
                        if let Ok(m) = monitor.lock() {
                            m.sample_task(tr);
                        }
                    }
                    
                    // 1. 先检查进程是否已经退出（崩溃或完成）
                    match child.try_wait() {
                        Ok(Some(status)) => return Ok::<_, std::io::Error>(status),
                        Ok(None) => {}
                        Err(e) => return Err::<std::process::ExitStatus, std::io::Error>(e),
                    }
                    
                    // 2. 检查文件是否存在且大小稳定
                    if let Ok(metadata) = tokio::fs::metadata(output_path).await {
                        let curr_size = metadata.len();
                        if curr_size > 0 {
                            if curr_size == last_size {
                                stable_count += 1;
                            } else {
                                stable_count = 0;
                            }
                            last_size = curr_size;
                            
                            // 文件大小稳定 2 次（约 200ms），截图完成
                            if stable_count >= 2 {
                                // 只杀死我们启动的截图进程组（通过负PID杀死整个进程组）
                                let pgid = child.id() as i32;
                                // kill -<pgid> 会杀死整个进程组
                                let _ = std::process::Command::new("kill")
                                    .arg("-9")
                                    .arg(format!("-{}", pgid))
                                    .status();
                                
                                // 等待进程退出
                                tokio::time::sleep(Duration::from_millis(300)).await;
                                match child.try_wait() {
                                    Ok(Some(status)) => return Ok(status),
                                    Ok(None) => {
                                        // Process still running, force kill and wait
                                        let _ = child.kill();
                                        // Use blocking wait() to ensure process is reaped
                                        match child.wait() {
                                            Ok(status) => return Ok(status),
                                            Err(e) => return Err(e),
                                        }
                                    }
                                    Err(e) => {
                                        return Err(e);
                                    }
                                }
                            }
                        }
                    }
                    
                    // 每 100ms 检查一次
                    tokio::time::sleep(Duration::from_millis(100)).await;
                }
            }
        ).await;
        
        match result {
            Ok(Ok(status)) => Ok(status),
            Ok(Err(e)) => Err(LwgError::ProcessError(format!("Wait error: {}", e))),
            Err(_) => {
                // 超时，强制杀死进程
                let _ = child.kill();
                Err(LwgError::ProcessError(format!("Screenshot timed out after {} seconds", timeout_secs)))
            }
        }
    }
    
    /// 完成截图并保存历史记录
    pub fn finalize_screenshot(
        tracker: crate::performance::TaskTracker,
        wp_id: String,
        output_path: String,
        perf_monitor: Arc<std::sync::Mutex<crate::performance::PerformanceMonitor>>,
    ) -> LwgResult<crate::performance::ScreenshotRecord> {
        let monitor = perf_monitor.lock().map_err(|e| LwgError::ProcessError(format!("Lock error: {}", e)))?;
        
        // 获取统计数据
        let (duration, max_cpu, max_mem, _avg_cpu, _avg_mem) = monitor.stop_task(&tracker);
        
        // 创建记录
        let timestamp = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap_or_default()
            .as_secs();
        
        let record = crate::performance::ScreenshotRecord {
            timestamp,
            wp_id,
            output_path,
            duration,
            max_cpu,
            max_mem,
        };
        
        Ok(record)
    }
}
