use thiserror::Error;

/// 统一错误类型
#[derive(Debug, Error)]
pub enum LwgError {
    #[error("配置文件不存在：{0}")]
    ConfigNotFound(String),

    #[error("JSON 解析失败：{0}")]
    JsonParseError(#[from] serde_json::Error),

    #[error("目录不存在：{0}")]
    DirectoryNotFound(String),

    #[error("IO 错误：{0}")]
    IoError(#[from] std::io::Error),

    #[error("进程启动失败：{0}")]
    ProcessError(String),

    #[error("未找到可用显示器")]
    NoDisplayFound,

    #[error("壁纸未找到：{0}")]
    WallpaperNotFound(String),

    #[error("无效的配置项：{0}")]
    InvalidConfig(String),

    #[error("截图失败：{0}")]
    ScreenshotError(String),

    #[error("IPC 通信错误：{0}")]
    IpcError(String),
}

/// 统一结果类型
pub type LwgResult<T> = Result<T, LwgError>;
