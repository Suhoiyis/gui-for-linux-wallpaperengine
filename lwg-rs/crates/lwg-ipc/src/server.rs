use crate::protocol::{IpcCommand, IpcResponse};
use lwg_core::error::LwgResult;
use std::os::linux::net::SocketAddrExt;
use std::os::unix::net::SocketAddr;
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};
use tokio::net::{UnixListener, UnixStream};
use tracing::{debug, error, info, warn};

pub struct IpcServer {
    socket_name: String,
    listener: UnixListener,
}

impl IpcServer {
    pub async fn bind(socket_name: impl Into<String>) -> LwgResult<Self> {
        let socket_name = socket_name.into();
        
        let addr = SocketAddr::from_abstract_name(socket_name.as_bytes())
            .map_err(|e| lwg_core::error::LwgError::IpcError(format!(
                "Failed to create abstract address: {}", e
            )))?;
        
        let std_listener = std::os::unix::net::UnixListener::bind_addr(&addr)
            .map_err(|e| lwg_core::error::LwgError::IpcError(format!(
                "Failed to bind IPC socket: {}", e
            )))?;
        
        let listener = UnixListener::from_std(std_listener)
            .map_err(|e| lwg_core::error::LwgError::IpcError(format!(
                "Failed to create tokio listener: {}", e
            )))?;
        
        info!("IPC server bound to abstract socket: {}", socket_name);
        
        Ok(Self {
            socket_name,
            listener,
        })
    }
    
    pub async fn bind_default() -> LwgResult<Self> {
        let uid = unsafe { libc::getuid() };
        let socket_name = format!("lwg-ipc-{}", uid);
        Self::bind(socket_name).await
    }
    
    pub async fn accept_loop<H>(self, handler: H) -> LwgResult<()>
    where
        H: Fn(IpcCommand) -> std::pin::Pin<Box<dyn std::future::Future<Output = IpcResponse> + Send>> + Send + Sync + Clone + 'static,
    {
        info!("IPC server started, waiting for connections...");
        
        loop {
            match self.listener.accept().await {
                Ok((stream, _)) => {
                    let h = handler.clone();
                    tokio::spawn(async move {
                        if let Err(e) = Self::handle_connection(stream, h).await {
                            debug!("Connection handler error: {}", e);
                        }
                    });
                }
                Err(e) => {
                    error!("Failed to accept connection: {}", e);
                }
            }
        }
    }
    
    async fn handle_connection<H>(
        stream: UnixStream,
        handler: H,
    ) -> LwgResult<()>
    where
        H: Fn(IpcCommand) -> std::pin::Pin<Box<dyn std::future::Future<Output = IpcResponse> + Send>>,
    {
        let (reader, mut writer) = stream.into_split();
        let mut reader = BufReader::new(reader);
        let mut line = String::new();
        
        match reader.read_line(&mut line).await {
            Ok(0) => return Ok(()),
            Ok(_) => {
                debug!("Received IPC command: {}", line.trim());
                
                match serde_json::from_str::<IpcCommand>(&line) {
                    Ok(cmd) => {
                        let response = Box::pin(handler(cmd)).await;
                        
                        let response_json = serde_json::to_string(&response)?;
                        writer.write_all(response_json.as_bytes()).await?;
                        writer.write_all(b"\n").await?;
                        writer.flush().await?;
                    }
                    Err(e) => {
                        warn!("Failed to parse IPC command: {}", e);
                        
                        let response = IpcResponse::Error(format!("Parse error: {}", e));
                        let response_json = serde_json::to_string(&response)?;
                        writer.write_all(response_json.as_bytes()).await?;
                        writer.write_all(b"\n").await?;
                        writer.flush().await?;
                    }
                }
            }
            Err(e) => {
                return Err(lwg_core::error::LwgError::IpcError(format!(
                    "Read error: {}", e
                )));
            }
        }
        
        Ok(())
    }
    
    pub fn socket_name(&self) -> &str {
        &self.socket_name
    }
}