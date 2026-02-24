use serde::{Deserialize, Serialize};

/// IPC 命令枚举
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum IpcCommand {
    Show,
    Hide,
    Toggle,
    Random,
    Stop,
    ApplyLast,
    Refresh,
    Quit,
    Apply { id: String, screen: Option<String> },
}

/// IPC 响应枚举
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum IpcResponse {
    Ok,
    Error(String),
    Status { is_running: bool, tooltip: String },
}
