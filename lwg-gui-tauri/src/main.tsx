import React from "react";
import ReactDOM from "react-dom/client";
import { App } from "./App";
import "./index.css";
// 1. 引入 Provider
import { ThemeProvider } from "./components/providers/ThemeProvider";
import { Toaster } from "./components/ui/sonner";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    {/* 2. 包裹 App，默认设为 dark (这样第一次打开就是好看的深色) */}
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <App />
      <Toaster />
    </ThemeProvider>
  </React.StrictMode>,
);
