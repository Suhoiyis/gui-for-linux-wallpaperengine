import psutil
import time
import threading
from typing import Dict, List, Optional, Callable

class PerformanceMonitor:
    def __init__(self):
        # Map: category -> pid
        self._monitored_pids: Dict[str, int] = {}
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._callbacks: List[Callable[[Dict], None]] = []
        self._interval = 1.0  # Faster updates (1s)

        # Always monitor self (GUI)
        self._monitored_pids["frontend"] = psutil.Process().pid

    def start_monitoring(self, category: str, pid: int):
        """Start tracking a specific process (backend, tray, etc)"""
        self._monitored_pids[category] = pid
        self._ensure_thread_running()

    def stop_monitoring(self, category: str):
        """Stop tracking a specific category"""
        if category in self._monitored_pids:
            del self._monitored_pids[category]

    def stop_all_backends(self):
        """Stop monitoring backend/tray but keep frontend"""
        keys = list(self._monitored_pids.keys())
        for k in keys:
            if k != "frontend":
                del self._monitored_pids[k]

    def _ensure_thread_running(self):
        if not self._thread or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self._thread.start()

    def add_callback(self, callback: Callable[[Dict], None]):
        """Register a callback to receive stats updates"""
        self._callbacks.append(callback)
        self._ensure_thread_running() # Ensure loop is running if UI requests it

    def _monitor_loop(self):
        while not self._stop_event.is_set():
            stats = {
                "total": {"cpu": 0.0, "memory_mb": 0.0, "threads": 0},
                "details": {}
            }
            
            # Snapshot of keys to avoid modification during iteration
            active_items = list(self._monitored_pids.items())
            
            for category, pid in active_items:
                try:
                    proc = psutil.Process(pid)
                    with proc.oneshot():
                        cpu = proc.cpu_percent(interval=None)
                        mem_info = proc.memory_info()
                        mem_mb = mem_info.rss / (1024 * 1024)
                        threads = proc.num_threads()
                        status = proc.status()
                        name = proc.name()

                    data = {
                        "pid": pid,
                        "name": name,
                        "cpu": cpu,
                        "memory_mb": round(mem_mb, 1),
                        "threads": threads,
                        "status": status
                    }
                    stats["details"][category] = data
                    
                    # Aggregate total
                    stats["total"]["cpu"] += cpu
                    stats["total"]["memory_mb"] += mem_mb
                    stats["total"]["threads"] += threads

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    if category != "frontend":
                        self.stop_monitoring(category)
            
            stats["total"]["memory_mb"] = round(stats["total"]["memory_mb"], 1)
            stats["total"]["cpu"] = round(stats["total"]["cpu"], 1)

            self._notify(stats)
            time.sleep(self._interval)

    def _notify(self, stats: Dict):
        for cb in self._callbacks:
            try:
                cb(stats)
            except Exception as e:
                print(f"[PerformanceMonitor] Callback error: {e}")
