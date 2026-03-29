import {
  enable as autostartEnable,
  disable as autostartDisable,
  isEnabled as autostartIsEnabled,
} from "@tauri-apps/plugin-autostart";

import {
  isPermissionGranted as notificationIsPermissionGranted,
  requestPermission as notificationRequestPermission,
  sendNotification as notificationSendNotification,
} from "@tauri-apps/plugin-notification";

// ================= Autostart API =================

export async function setAutostart(enabled: boolean): Promise<void> {
  if (enabled) {
    await autostartEnable();
  } else {
    await autostartDisable();
  }
}

export async function getAutostartStatus(): Promise<boolean> {
  return await autostartIsEnabled();
}

// ================= Notification API =================

export async function notify(title: string, body: string): Promise<boolean> {
  let granted = await notificationIsPermissionGranted();

  if (!granted) {
    const permission = await notificationRequestPermission();
    granted = permission === "granted";
  }

  if (granted) {
    notificationSendNotification({ title, body });
    return true;
  }

  return false;
}

export async function isNotificationPermissionGranted(): Promise<boolean> {
  return await notificationIsPermissionGranted();
}

export async function requestNotificationPermission(): Promise<boolean> {
  const permission = await notificationRequestPermission();
  return permission === "granted";
}