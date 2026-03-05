use crate::protocol::{IpcCommand, IpcResponse};
use lwg_core::error::LwgResult;
use std::os::linux::net::SocketAddrExt;
use std::os::unix::net::SocketAddr;
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};
use tokio::net::UnixStream;
use tracing::debug;

/// IPC 客户端
pub struct IpcClient;

impl IpcClient {
    /// 发送命令到 IPC 服务端
    pub async fn send(
        socket_name: impl AsRef<str>,
        command: IpcCommand,
    ) -> LwgResult<IpcResponse> {
        let socket_name = socket_name.as_ref();
        
        // 创建抽象地址
        let addr = SocketAddr::from_abstract_name(socket_name.as_bytes())
            .map_err(|e| lwg_core::error::LwgError::IpcError(format!(
                "Failed to create abstract address: {}", e
            )))?;
        
        let std_stream: std::os::unix::net::UnixStream = std::os::unix::net::UnixStream::connect_addr(&addr)
            .map_err(|e| lwg_core::error::LwgError::IpcError(format!(
                "Failed to connect to IPC server: {}", e
            )))?;
        
        let stream = UnixStream::from_std(std_stream)
            .map_err(|e| lwg_core::error::LwgError::IpcError(format!(
                "Failed to create tokio stream: {}", e
            )))?;
        
        debug!("Connected to IPC server at {}", socket_name);
        
        // 发送命令
        let (reader, mut writer) = stream.into_split();
        let command_json = serde_json::to_string(&command)?;
        writer.write_all(command_json.as_bytes()).await?;
        writer.write_all(b"\n").await?;
        writer.flush().await?;
        
        // 读取响应
        let mut reader = BufReader::new(reader);
        let mut line = String::new();
        
        match reader.read_line(&mut line).await {
            Ok(0) => Err(lwg_core::error::LwgError::IpcError(
                "Server closed connection".to_string()
            )),
            Ok(_) => {
                debug!("Received IPC response: {}", line.trim());
                
                match serde_json::from_str::<IpcResponse>(&line) {
                    Ok(response) => Ok(response),
                    Err(e) => Err(lwg_core::error::LwgError::IpcError(format!(
                        "Failed to parse response: {}", e
                    ))),
                }
            }
            Err(e) => Err(lwg_core::error::LwgError::IpcError(format!(
                "Read error: {}", e
            ))),
        }
    }
    
    /// 使用默认 socket 名称发送命令
    pub async fn send_default(command: IpcCommand) -> LwgResult<IpcResponse> {
        let uid = unsafe { libc::getuid() };
        let socket_name = format!("lwg-ipc-{}", uid);
        Self::send(&socket_name, command).await
    }
}
