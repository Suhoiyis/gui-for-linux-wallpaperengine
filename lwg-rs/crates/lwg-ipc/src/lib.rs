use serde::{Deserialize, Serialize};

/// IPC 消息枚举
/// 对应 Python 中的 CLI 命令和 Tray 通信
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum Command {
    /// 显示窗口
    Show,
    /// 隐藏窗口
    Hide,
    /// 切换显示/隐藏
    Toggle,
    /// 随机切换壁纸
    Random,
    /// 停止壁纸
    Stop,
    /// 应用上一个壁纸
    ApplyLast,
    /// 刷新壁纸库
    Refresh,
    /// 退出程序
    Quit,
    // 未来扩展：ApplySpecific(u64) 等
}

/// Abstract Socket 路径常量
/// Python 版本可能用了动态路径，这里我们固定下来
pub const SOCKET_PATH: &str = "linux-wallpaperengine-gui.sock";

// 简单的测试
#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_serialize() {
        let cmd = Command::Random;
        let encoded = bincode::serialize(&cmd).unwrap();
        let decoded: Command = bincode::deserialize(&encoded).unwrap();
        assert_eq!(cmd, decoded);
    }
}
