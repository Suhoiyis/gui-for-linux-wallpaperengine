import { invoke } from "@tauri-apps/api/core";
import { isTauriEnv } from "@/lib/utils";

export async function startCycleTimer(): Promise<void> {
  if (!isTauriEnv()) return;
  await invoke("start_cycle_timer");
}

export async function stopCycleTimer(): Promise<void> {
  if (!isTauriEnv()) return;
  await invoke("stop_cycle_timer");
}

export async function setCycleScreen(screen: string): Promise<void> {
  if (!isTauriEnv()) return;
  await invoke("set_cycle_screen", { screen });
}