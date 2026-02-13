import psutil
import time
import threading
import os
from collections import deque
from typing import Callable, Protocol, TypedDict, cast

HISTORY_SIZE = 60

def _format_cpu(val: float) -> str:
    return f"{int(val)}%" if val == int(val) else f"{val:.1f}%"

def _format_mem(val: float) -> str:
    return f"{int(val)} MB" if val == int(val) else f"{val:.1f} MB"

def _get_thread_names(pid: int) -> list[str]:
    names: list[str] = []
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


class _Config(Protocol):
    def get(self, key: str, default: object = ...) -> object:
        ...

    def set(self, key: str, value: object) -> None:
        ...


class TaskTracker(TypedDict):
    category: str
    start_time: float
    pid: int
    initial_cpu_time: float


class _HistoryPayload(TypedDict):
    cpu: list[float]
    memory_mb: list[float]


class _DetailPayload(TypedDict):
    pid: int
    name: str
    cpu: float
    cpu_fmt: str
    memory_mb: float
    memory_fmt: str
    threads: int
    status: str
    history: _HistoryPayload


class _TotalPayload(TypedDict):
    cpu: float
    cpu_fmt: str
    memory_mb: float
    memory_fmt: str
    threads: int
    history: _HistoryPayload
    thread_names: dict[str, list[str]]


class _StatsPayload(TypedDict):
    total: _TotalPayload
    details: dict[str, _DetailPayload]


class PerformanceMonitor:
    def __init__(self, config: _Config | None = None):
        self._stop_event: threading.Event = threading.Event()
        self._thread: threading.Thread | None = None
        self._callbacks: list[Callable[[_StatsPayload], None]] = []
        self._interval: float = 1.0
        
        self._processes: dict[str, psutil.Process] = {}
        self._history: dict[str, dict[str, deque[float]]] = {}
        self._cpu_count: int = psutil.cpu_count() or 1
        self._config: _Config | None = config
        _ = self._add_process("frontend", psutil.Process().pid)

    def _init_history(self, category: str) -> None:
        self._history[category] = {
            "cpu": deque(maxlen=HISTORY_SIZE),
            "memory_mb": deque(maxlen=HISTORY_SIZE)
        }

    def _find_real_process(self, pid: int, timeout: float = 0.0) -> psutil.Process | None:

        def _try_find_child(proc: psutil.Process) -> psutil.Process | None:
            try:
                children = proc.children(recursive=True)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                return None

            for child in children:
                try:
                    if child.name() == "linux-wallpaperengine":
                        return child
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return None

        try:
            proc = psutil.Process(pid)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None

        try:
            if proc.name() == "linux-wallpaperengine":
                return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None

        real = _try_find_child(proc)
        if real is not None:
            return real

        if timeout and timeout > 0:
            poll_interval = 0.1
            deadline = time.monotonic() + timeout
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    break
                time.sleep(min(poll_interval, remaining))

                try:
                    proc = psutil.Process(pid)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    return None

                try:
                    if proc.name() == "linux-wallpaperengine":
                        return proc
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    return None

                real = _try_find_child(proc)
                if real is not None:
                    return real

        return proc

    def _add_process(self, category: str, pid: int) -> bool:
        # For backend and screenshot, find the real linux-wallpaperengine process
        proc = None
        if category in ("backend", "screenshot"):
            poll_timeout = 0.2 if threading.current_thread() is threading.main_thread() else 1.0
            proc = self._find_real_process(pid, timeout=poll_timeout)
        if proc is None:
            try:
                proc = psutil.Process(pid)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                return False
        # Initialize CPU usage counter
        try:
            _ = proc.cpu_percent(interval=None)
        except Exception:
            pass
            
        self._processes[category] = proc
        self._init_history(category)
        return True

    def start_monitoring(self, category: str, pid: int):
        if self._add_process(category, pid):
            self._ensure_thread_running()

    def stop_monitoring(self, category: str):
        _ = self._processes.pop(category, None)
        _ = self._history.pop(category, None)

    def stop_all_backends(self):
        keys = [k for k in self._processes.keys() if k not in ("frontend", "tray")]
        for k in keys:
            del self._processes[k]
            _ = self._history.pop(k, None)

    def start_task(self, category: str, pid: int) -> TaskTracker:
        """Start tracking a specific task. Returns a tracker object (dict)."""
        self.start_monitoring(category, pid)
        
        initial_cpu_time = 0.0
        if category in self._processes:
            try:
                proc = self._processes[category]
                cpu_times = proc.cpu_times()
                initial_cpu_time = cpu_times.user + cpu_times.system
            except Exception:
                pass

        return {
            "category": category,
            "start_time": time.time(),
            "pid": pid,
            "initial_cpu_time": initial_cpu_time
        }

    def stop_task(self, tracker: TaskTracker) -> dict[str, float]:
        """Stop tracking a task and return stats."""
        category = tracker["category"]
        start_time = tracker["start_time"]
        initial_cpu_time = tracker["initial_cpu_time"]
        duration = time.time() - start_time
        
        if category in self._processes:
            try:
                proc = self._processes[category]
                with proc.oneshot():
                    cpu = proc.cpu_percent(interval=None) / self._cpu_count
                    
                    if initial_cpu_time > 0:
                        try:
                            curr_times = proc.cpu_times()
                            delta_cpu = (curr_times.user + curr_times.system) - initial_cpu_time
                            if delta_cpu > 0 and duration > 0:
                                avg_cpu = min((delta_cpu / duration) * 100 / self._cpu_count, 100.0)
                                if cpu == 0:
                                    cpu = avg_cpu
                        except Exception:
                            pass

                    rss = cast(int, proc.memory_info().rss)
                    mem_mb = rss / (1024 * 1024)
                    
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
            cpu_hist = list(self._history[category]["cpu"])
            mem_hist = list(self._history[category]["memory_mb"])
            
            if cpu_hist:
                stats["max_cpu"] = min(max(cpu_hist), 100.0)
                stats["avg_cpu"] = min(sum(cpu_hist) / len(cpu_hist), 100.0)
            
            if mem_hist:
                stats["max_mem"] = max(mem_hist)
                stats["avg_mem"] = sum(mem_hist) / len(mem_hist)
                
        self.stop_monitoring(category)
        return stats


    def add_screenshot_history(self, wp_id: str, output_path: str, stats: dict[str, float]) -> None:
        if not self._config:
            return
        raw_existing = self._config.get("screenshot_history", [])
        if isinstance(raw_existing, list):
            history: list[dict[str, object]] = []
            for item in cast(list[object], raw_existing):
                if isinstance(item, dict):
                    history.append(cast(dict[str, object], item))
        else:
            history = []
        record: dict[str, object] = {
            "timestamp": time.time(),
            "wp_id": str(wp_id),
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

    def get_screenshot_history(self) -> list[dict[str, object]]:
        if not self._config:
            return []
        # Return a copy to prevent modification during iteration
        raw_history = self._config.get("screenshot_history", [])
        if not isinstance(raw_history, list):
            return []
        out: list[dict[str, object]] = []
        for item in cast(list[object], raw_history):
            if isinstance(item, dict):
                out.append(dict(cast(dict[str, object], item)))
        return out

    def clear_screenshot_history(self):
        if self._config:
            self._config.set("screenshot_history", [])

    def _ensure_thread_running(self):
        if not self._thread or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._monitor_loop, name="PerfMonitor", daemon=True)
            self._thread.start()

    def add_callback(self, callback: Callable[[_StatsPayload], None]) -> None:
        self._callbacks.append(callback)
        self._ensure_thread_running()

    def _monitor_loop(self):
        while not self._stop_event.is_set():
            stats: _StatsPayload = {
                "total": {
                    "cpu": 0.0,
                    "cpu_fmt": _format_cpu(0.0),
                    "memory_mb": 0.0,
                    "memory_fmt": _format_mem(0.0),
                    "threads": 0,
                    "history": {"cpu": [], "memory_mb": []},
                    "thread_names": {},
                },
                "details": {},
            }
            
            if "total" not in self._history:
                self._init_history("total")

            for category, proc in list(self._processes.items()):
                try:
                    # Upgrade wrapper process to real engine if available
                    if category in ("backend", "screenshot") and proc.name() != "linux-wallpaperengine":
                        real = self._find_real_process(proc.pid)
                        if real and real.name() == "linux-wallpaperengine":
                            _ = real.cpu_percent(interval=None)
                            self._processes[category] = real
                            proc = real
                    
                    with proc.oneshot():
                        cpu = proc.cpu_percent(interval=None) / self._cpu_count
                        rss = cast(int, proc.memory_info().rss)
                        mem_mb = rss / (1024 * 1024)
                        threads = int(proc.num_threads())
                        status = str(proc.status())
                        name = str(proc.name())

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
                        _ = self._processes.pop(category, None)
            
            total_cpu = round(float(stats["total"]["cpu"]), 1)
            total_mem = round(float(stats["total"]["memory_mb"]), 1)
            
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
            
            interval = self._interval
            if "screenshot" in self._processes:
                interval = 0.1
            time.sleep(interval)

    def _notify(self, stats: _StatsPayload) -> None:
        for cb in self._callbacks:
            try:
                cb(stats)
            except Exception as e:
                print(f"[PerformanceMonitor] Callback error: {e}")
