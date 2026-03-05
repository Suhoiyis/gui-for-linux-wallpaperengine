use lwg_ipc::IpcCommand;
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    let socket_path = env::var("LWG_IPC_SOCKET").unwrap_or_else(|_| {
        let uid = unsafe { libc::getuid() };
        format!("lwg-ipc-{}", uid)
    });

    eprintln!("Rust tray started, socket: {}", socket_path);

    let rt = tokio::runtime::Runtime::new().unwrap();
    rt.block_on(async move {
        eprintln!("Tray ready, waiting for commands...");
        
        if args.len() > 1 && args[1] == "--test" {
            match lwg_ipc::IpcClient::send(&socket_path, IpcCommand::Toggle).await {
                Ok(resp) => eprintln!("Response: {:?}", resp),
                Err(e) => eprintln!("Error: {}", e),
            }
        }
        
        std::future::pending::<()>().await;
    });
}