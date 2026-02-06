# Process Monitoring - Quick Reference

## File Locations

| Component | File | Lines | Purpose |
|-----------|------|-------|---------|
| Tray Detection | `py_GUI/ui/tray_process.py` | 88-108 | Polls `/proc` every 2s for engine |
| Performance Monitor | `py_GUI/core/performance.py` | 47-167 | Tracks CPU/memory with 1s interval |
| Wallpaper Controller | `py_GUI/core/controller.py` | 74-199 | Manages process lifecycle |

## How Tray Detects Process

```python
# File: py_GUI/ui/tray_process.py:88-108
_poll_state():
  - Polls every 2 seconds (GLib.timeout_add_seconds(2))
  - Reads /proc/{pid}/cmdline for all processes
  - Searches for string: 'linux-wallpaperengine'
  - Filters out 'python' and 'grep' in cmdline
  - Sets self.is_running = True/False
```

**Key point**: Simple string matching, 2-second lag

## How Process List is Updated

```
User applies wallpaper
  ↓
WallpapersPage.apply_wallpaper() [wallpapers.py:769]
  ↓
WallpaperController.apply() [controller.py:33]
  └─ Updates config
  ↓
WallpaperController.restart_wallpapers() [controller.py:74]
  ├─ stop() [line 76]
  │  └─ perf_monitor.stop_all_backends() [controller.py:274]
  │
  ├─ subprocess.Popen() [line 175]
  │  └─ Creates new process
  │
  └─ start_monitoring() [line 198]
     └─ perf_monitor.start_monitoring("backend", new_pid)
        └─ _find_real_process() searches children
        └─ Registers in _processes["backend"]
```

## Process Monitor Data Structure

```python
# File: py_GUI/core/performance.py

_processes: Dict[str, psutil.Process]
  {
    "frontend": psutil.Process(gui_pid),
    "backend": psutil.Process(engine_pid)
  }

_history: Dict[str, Dict[str, deque]]
  {
    "frontend": {"cpu": deque[60], "memory_mb": deque[60]},
    "backend": {"cpu": deque[60], "memory_mb": deque[60]},
    "total": {"cpu": deque[60], "memory_mb": deque[60]}
  }
```

**Storage**: Last 60 samples (HISTORY_SIZE = 60)
**Update**: Every 1 second via `_monitor_loop()`

## Critical Timing During Wallpaper Change

```
T=0ms       User clicks Apply
T=25ms      stop_all_backends() called → removes "backend" from dict
T=100ms     subprocess.Popen() creates new process
            ⚠️ MONITORING GAP: Process exists but not tracked!
T=700ms     start_monitoring("backend", new_pid) called
            ✓ Process now registered in _processes
T=1000ms    Monitor loop wakes up → Collects metrics
T=2000ms    Tray poll runs → Detects via /proc (1900ms lag!)
```

**Monitoring gap**: 600ms (T=100-700ms)
**Tray lag**: Up to 1900ms (T=100 to T=2000)

## Process Cleanup

### Auto-cleanup (Monitor Loop)
```python
# File: py_GUI/core/performance.py:138-140
except (psutil.NoSuchProcess, psutil.AccessDenied):
    if category != "frontend":
        self._processes.pop(category, None)
```

- Triggered when monitoring exception occurs
- Only removes backend processes (frontend never removed)
- Cleanup lag: Up to 1 second (next monitor cycle)

### Manual Cleanup
```python
# File: py_GUI/core/controller.py:274
self.perf_monitor.stop_all_backends()
```

- Called explicitly in stop() method
- Removes all "backend*" entries immediately
- Called twice during restart (line 274 and 197)

## Backend Search Strategy

```python
# File: py_GUI/core/performance.py:47-56
def _find_real_process(self, pid: int):
    proc = psutil.Process(pid)
    children = proc.children(recursive=True)
    for child in children:
        if child.name() == "linux-wallpaperengine":
            return child  # Found!
    return proc  # Fallback: return parent
```

**Logic**:
1. Search all child processes recursively
2. Find one with name == "linux-wallpaperengine"
3. If found: track that child
4. If not found: track parent process

## Monitoring Loop (Every 1 Second)

```python
# File: py_GUI/core/performance.py:94-167
def _monitor_loop(self):
    while not self._stop_event.is_set():
        stats = {"total": {...}, "details": {}}
        
        for category, proc in list(self._processes.items()):  # Snapshot!
            try:
                cpu = proc.cpu_percent(interval=None)
                mem_mb = proc.memory_info().rss / (1024 * 1024)
                threads = proc.num_threads()
                status = proc.status()
                
                # Update history
                self._history[category]["cpu"].append(cpu)
                self._history[category]["memory_mb"].append(mem_mb)
                
                # Build stats
                stats["details"][category] = {
                    "pid": proc.pid,
                    "name": proc.name(),
                    "cpu": round(cpu, 1),
                    "cpu_fmt": _format_cpu(...),
                    "memory_mb": round(mem_mb, 1),
                    "memory_fmt": _format_mem(...),
                    "threads": threads,
                    "status": status,
                    "history": {...}
                }
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                if category != "frontend":
                    self._processes.pop(category, None)  # Auto-cleanup
        
        self._notify(stats)  # Fire callbacks
        time.sleep(self._interval)  # 1 second
```

## Critical Issues

### Issue 1: Monitoring Gap (600ms)
- Process created but not yet registered
- If crashes during gap: no monitoring data
- Performance graph shows gap

### Issue 2: Tray Lag (1900ms)
- Process change invisible to tray for up to 2 seconds
- User applies wallpaper but tray shows old state
- Toggle button unreliable

### Issue 3: Double Cleanup
- `stop_all_backends()` called at lines 274 and 197
- 2nd call redundant but harmless

### Issue 4: No Thread Safety
- `_processes` dict modified from multiple sources
- Only partial protection via `list()` snapshot
- Risk: Race condition if timing changes

## Integration Points

```
Controller → PerformanceMonitor:
  start_monitoring("backend", pid)
  stop_all_backends()

PerformanceMonitor → UI:
  Callback _notify(stats) every 1 second
  Updates: CPU%, Memory, History graphs

Tray → Controller:
  apply(), stop()

Config → Controller:
  active_monitors, lastWallpaper
```

## Quick Debug Tips

1. **Watch monitoring gaps**: Add logging at controller.py:76, 175, 198
2. **Track process list changes**: Log _add_process() and stop_all_backends()
3. **Measure timing**: Record timestamps for each step
4. **Check cleanup lag**: Monitor when dead processes removed vs detected
5. **Verify tray sync**: Log tray _poll_state() vs controller lifecycle

## Files to Remember

- **Process monitoring**: `py_GUI/core/performance.py`
- **Wallpaper lifecycle**: `py_GUI/core/controller.py`
- **Tray detection**: `py_GUI/ui/tray_process.py`
- **Frontend lifecycle**: `py_GUI/ui/pages/wallpapers.py`
