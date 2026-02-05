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

class PerformanceMonitor:
    def __init__(self):
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._callbacks: List[Callable[[Dict], None]] = []
        self._interval = 1.0
        
        self._processes: Dict[str, psutil.Process] = {}
        self._history: Dict[str, Dict[str, deque]] = {}
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
        proc = self._find_real_process(pid) if category == "backend" else None
        if proc is None:
            try:
                proc = psutil.Process(pid)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                return False
        proc.cpu_percent()
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
        keys = [k for k in self._processes.keys() if k != "frontend"]
        for k in keys:
            del self._processes[k]
            self._history.pop(k, None)

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
                    with proc.oneshot():
                        cpu = proc.cpu_percent(interval=None)
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
