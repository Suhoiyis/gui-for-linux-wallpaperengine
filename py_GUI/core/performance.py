import psutil
import time
import threading
import os
from collections import deque
from typing import Dict, List, Optional, Callable

HISTORY_SIZE = 60

def _format_cpu(val: float) -> str:
    return f"{int(val)}%" if val == int(val) else f"{val:.1f}%"

def _format_mem(val: float) -> str:
    return f"{int(val)} MB" if val == int(val) else f"{val:.1f} MB"

def _get_thread_names(pid: int) -> List[str]:
    names = []
    task_dir = f"/proc/{pid}/task"
    try:
        for tid in os.listdir(task_dir):
            try:
                with open(f"{task_dir}/{tid}/comm") as f:
                    names.append(f.read().strip())
            except (IOError, OSError):
                pass
    except (IOError, OSError):
        pass
    return names

SCREENSHOT_HISTORY_LIMIT = 10


class PerformanceMonitor:
    def __init__(self, config=None):
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._callbacks: List[Callable[[Dict], None]] = []
        self._interval = 1.0
        
        self._processes: Dict[str, psutil.Process] = {}
        self._history: Dict[str, Dict[str, deque]] = {}
        self._cpu_count = psutil.cpu_count() or 1
        self._config = config
        self._add_process("frontend", psutil.Process().pid)

    def _init_history(self, category: str):
        self._history[category] = {
            "cpu": deque(maxlen=HISTORY_SIZE),
            "memory_mb": deque(maxlen=HISTORY_SIZE)
        }

    def _find_real_process(self, pid: int) -> Optional[psutil.Process]:
        try:
            proc = psutil.Process(pid)
            children = proc.children(recursive=True)
            for child in children:
                if child.name() == "linux-wallpaperengine":
                    return child
            return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None

    def _add_process(self, category: str, pid: int) -> bool:
        # For backend and screenshot, find the real linux-wallpaperengine process
        proc = self._find_real_process(pid) if category in ("backend", "screenshot") else None
        if proc is None:
            try:
                proc = psutil.Process(pid)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                return False
        # Initialize CPU usage counter
        try:
            proc.cpu_percent(interval=None)
        except Exception:
            pass
            
        self._processes[category] = proc
        self._init_history(category)
        return True

    def start_monitoring(self, category: str, pid: int):
        if self._add_process(category, pid):
            self._ensure_thread_running()

    def stop_monitoring(self, category: str):
        self._processes.pop(category, None)
        self._history.pop(category, None)

    def stop_all_backends(self):
        keys = [k for k in self._processes.keys() if k not in ("frontend", "tray")]
        for k in keys:
            del self._processes[k]
            self._history.pop(k, None)

    def start_task(self, category: str, pid: int) -> Dict:
        """Start tracking a specific task. Returns a tracker object (dict)."""
        self.start_monitoring(category, pid)
        return {
            "category": category,
            "start_time": time.time(),
            "pid": pid
        }

    def stop_task(self, tracker: Dict) -> Dict:
        """Stop tracking a task and return stats."""
        category = tracker["category"]
        start_time = tracker["start_time"]
        duration = time.time() - start_time
        
        # Force a final sample if task was short
        if category in self._processes:
            try:
                proc = self._processes[category]
                with proc.oneshot():
                    cpu = proc.cpu_percent(interval=None) / self._cpu_count
                    mem_mb = proc.memory_info().rss / (1024 * 1024)
                    
                if category in self._history:
                    self._history[category]["cpu"].append(cpu)
                    self._history[category]["memory_mb"].append(mem_mb)
            except Exception:
                pass

        stats = {
            "duration": duration,
            "max_cpu": 0.0,
            "max_mem": 0.0,
            "avg_cpu": 0.0,
            "avg_mem": 0.0
        }
        
        if category in self._history:
            # Filter history by time if possible, but for now take recent history
            # Ideally we check timestamps, but deque doesn't store them.
            # Since we start a new category for this task, the whole history is relevant.
            cpu_hist = list(self._history[category]["cpu"])
            mem_hist = list(self._history[category]["memory_mb"])
            
            if cpu_hist:
                stats["max_cpu"] = max(cpu_hist)
                stats["avg_cpu"] = sum(cpu_hist) / len(cpu_hist)
            
            if mem_hist:
                stats["max_mem"] = max(mem_hist)
                stats["avg_mem"] = sum(mem_hist) / len(mem_hist)
                
        self.stop_monitoring(category)
        return stats

    def add_screenshot_history(self, wp_id: str, output_path: str, stats: Dict):
        if not self._config:
            return
        history = self._config.get("screenshot_history", [])
        record = {
            "timestamp": time.time(),
            "wp_id": wp_id,
            "output_path": output_path,
            "duration": stats.get("duration", 0),
            "max_cpu": stats.get("max_cpu", 0),
            "max_mem": stats.get("max_mem", 0),
            "avg_cpu": stats.get("avg_cpu", 0),
            "avg_mem": stats.get("avg_mem", 0),
        }
        history.append(record)
        if len(history) > SCREENSHOT_HISTORY_LIMIT:
            history = history[-SCREENSHOT_HISTORY_LIMIT:]
        self._config.set("screenshot_history", history)

    def get_screenshot_history(self) -> List[Dict]:
        if not self._config:
            return []
        return self._config.get("screenshot_history", [])

    def _ensure_thread_running(self):
        if not self._thread or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self._thread.start()

    def add_callback(self, callback: Callable[[Dict], None]):
        self._callbacks.append(callback)
        self._ensure_thread_running()

    def _monitor_loop(self):
        while not self._stop_event.is_set():
            stats = {
                "total": {"cpu": 0.0, "memory_mb": 0.0, "threads": 0},
                "details": {}
            }
            
            if "total" not in self._history:
                self._init_history("total")

            for category, proc in list(self._processes.items()):
                try:
                    # Upgrade wrapper process to real engine if available
                    if category in ("backend", "screenshot") and proc.name() != "linux-wallpaperengine":
                        real = self._find_real_process(proc.pid)
                        if real and real.name() == "linux-wallpaperengine":
                            real.cpu_percent(interval=None)
                            self._processes[category] = real
                            proc = real
                    
                    with proc.oneshot():
                        cpu = proc.cpu_percent(interval=None) / self._cpu_count
                        mem_mb = proc.memory_info().rss / (1024 * 1024)
                        threads = proc.num_threads()
                        status = proc.status()
                        name = proc.name()

                    if category not in self._history:
                        self._init_history(category)
                    
                    self._history[category]["cpu"].append(cpu)
                    self._history[category]["memory_mb"].append(mem_mb)

                    stats["details"][category] = {
                        "pid": proc.pid,
                        "name": name,
                        "cpu": round(cpu, 1),
                        "cpu_fmt": _format_cpu(round(cpu, 1)),
                        "memory_mb": round(mem_mb, 1),
                        "memory_fmt": _format_mem(round(mem_mb, 1)),
                        "threads": threads,
                        "status": status,
                        "history": {
                            "cpu": list(self._history[category]["cpu"]),
                            "memory_mb": list(self._history[category]["memory_mb"])
                        }
                    }
                    
                    stats["total"]["cpu"] += cpu
                    stats["total"]["memory_mb"] += mem_mb
                    stats["total"]["threads"] += threads

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    if category != "frontend":
                        self._processes.pop(category, None)
            
            total_cpu = round(stats["total"]["cpu"], 1)
            total_mem = round(stats["total"]["memory_mb"], 1)
            
            self._history["total"]["cpu"].append(total_cpu)
            self._history["total"]["memory_mb"].append(total_mem)
            
            stats["total"]["cpu"] = total_cpu
            stats["total"]["cpu_fmt"] = _format_cpu(total_cpu)
            stats["total"]["memory_mb"] = total_mem
            stats["total"]["memory_fmt"] = _format_mem(total_mem)
            stats["total"]["history"] = {
                "cpu": list(self._history["total"]["cpu"]),
                "memory_mb": list(self._history["total"]["memory_mb"])
            }
            
            all_thread_names = {}
            for category, proc in list(self._processes.items()):
                try:
                    names = _get_thread_names(proc.pid)
                    all_thread_names[category] = names
                except Exception:
                    all_thread_names[category] = []
            stats["total"]["thread_names"] = all_thread_names

            self._notify(stats)
            time.sleep(self._interval)

    def _notify(self, stats: Dict):
        for cb in self._callbacks:
            try:
                cb(stats)
            except Exception as e:
                print(f"[PerformanceMonitor] Callback error: {e}")
