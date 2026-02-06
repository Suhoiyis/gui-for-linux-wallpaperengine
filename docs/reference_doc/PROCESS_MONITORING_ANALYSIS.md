# Process Monitoring Analysis - Wallpaper Engine GUI

## Executive Summary

The application uses TWO independent systems to track the `linux-wallpaperengine` process:

1. **Tray Process** (`py_GUI/ui/tray_process.py`): Polls `/proc` every 2 seconds for the engine
2. **Performance Monitor** (`py_GUI/core/performance.py`): Tracks via psutil every 1 second
3. **Controller** (`py_GUI/core/controller.py`): Manages process lifecycle during wallpaper changes

These systems are **not synchronized**, leading to potential race conditions and timing issues during wallpaper changes.

---

## 1. TRAY PROCESS IDENTIFICATION (tray_process.py)

### Detection Mechanism

**File**: `py_GUI/ui/tray_process.py` lines 88-108

```python
def _poll_state(self):
    running = False
    try:
        # Check if linux-wallpaperengine is running
        pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
        for pid in pids:
            try:
                with open(os.path.join('/proc', pid, 'cmdline'), 'rb') as f:
                    cmdline = f.read().decode('utf-8', errors='ignore').replace('\0', ' ')
                    if 'linux-wallpaperengine' in cmdline and 'python' not in cmdline and 'grep' not in cmdline:
                        running = True
                        break
            except (IOError, OSError):
                continue
    except Exception as e:
        print(f"Poll error: {e}")
        running = False
        
    self.is_running = running
    return True # Keep calling
```

### How It Works

1. **Polling Interval**: Every 2 seconds (line 40)
   ```python
   GLib.timeout_add_seconds(2, self._poll_state)
   ```

2. **Process Detection**:
   - Iterates through all `/proc/{pid}/` directories
   - Reads `/proc/{pid}/cmdline` (the process command line)
   - Searches for literal string `'linux-wallpaperengine'`
   - Filters out `'python'` and `'grep'` to avoid false positives

3. **State Storage**: Sets `self.is_running` boolean

4. **Usage** (lines 110-117):
   ```python
   def _on_toggle(self, widget):
       if self.is_running:
           self._cmd("--stop")
       else:
           self._cmd("--apply-last")
   ```

### Limitations

- **Polling delay**: 2-second interval means up to 2 seconds stale data
- **String matching only**: Searches `/proc/{pid}/cmdline`, not process tree structure
- **No PID tracking**: Just knows if *any* instance is running, not which one
- **No metrics**: Only boolean state, no CPU/memory data
- **Independent**: Doesn't communicate with PerformanceMonitor

---

## 2. PERFORMANCE MONITOR SYSTEM (performance.py)

### Process Registration

**File**: `py_GUI/core/performance.py` lines 47-68

```python
def _find_real_process(self, pid: int) -> Optional[psutil.Process]:
    """Find the actual linux-wallpaperengine process in the process tree"""
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
    """Register a process for monitoring"""
    proc = self._find_real_process(pid) if category == "backend" else None
    if proc is None:
        try:
            proc = psutil.Process(pid)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False
    proc.cpu_percent()  # Prime the CPU counter
    self._processes[category] = proc
    self._init_history(category)
    return True
```

### Key Points

1. **For Backend Category**:
   - Searches child processes of the given PID
   - Looks for a child with `.name() == "linux-wallpaperengine"`
   - If found: tracks that child
   - If not found: tracks the parent process

2. **For Frontend Category**:
   - Directly tracks the process by PID

3. **History Initialization**:
   ```python
   def _init_history(self, category: str):
       self._history[category] = {
           "cpu": deque(maxlen=HISTORY_SIZE),      # Last 60 samples
           "memory_mb": deque(maxlen=HISTORY_SIZE)
       }
   ```

### Monitoring Loop

**File**: `py_GUI/core/performance.py` lines 94-167

**Interval**: Every 1 second (line 35: `self._interval = 1.0`)

```python
def _monitor_loop(self):
    while not self._stop_event.is_set():
        stats = {
            "total": {"cpu": 0.0, "memory_mb": 0.0, "threads": 0},
            "details": {}
        }
        
        # Process each registered process
        for category, proc in list(self._processes.items()):  # Snapshot!
            try:
                with proc.oneshot():
                    cpu = proc.cpu_percent(interval=None)
                    mem_mb = proc.memory_info().rss / (1024 * 1024)
                    threads = proc.num_threads()
                    status = proc.status()
                    name = proc.name()
                
                # Update history
                self._history[category]["cpu"].append(cpu)
                self._history[category]["memory_mb"].append(mem_mb)
                
                # Build stats dict
                stats["details"][category] = {
                    "pid": proc.pid,
                    "name": name,
                    "cpu": round(cpu, 1),
                    "cpu_fmt": _format_cpu(round(cpu, 1)),
                    "memory_mb": round(mem_mb, 1),
                    "memory_fmt": _format_mem(round(mem_mb, 1)),
                    "threads": threads,
                    "status": status,
                    "history": {...}
                }
                
                # Aggregate totals
                stats["total"]["cpu"] += cpu
                stats["total"]["memory_mb"] += mem_mb
                stats["total"]["threads"] += threads
                
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                if category != "frontend":
                    self._processes.pop(category, None)  # Auto-cleanup
        
        # Aggregate totals and notify callbacks
        self._notify(stats)
        time.sleep(self._interval)
```

### Process Cleanup

**Line 138-140**: Automatic removal of dead processes
```python
except (psutil.NoSuchProcess, psutil.AccessDenied):
    if category != "frontend":
        self._processes.pop(category, None)
```

- Detects when a process dies (NoSuchProcess exception)
- Removes it from `_processes` dict
- Frontend process is **never** removed automatically
- Next iteration won't include dead process in metrics

### Process List Interface

```python
def stop_all_backends(self):
    """Clear all backend process monitoring"""
    keys = [k for k in self._processes.keys() if k != "frontend"]
    for k in keys:
        del self._processes[k]
        self._history.pop(k, None)

def start_monitoring(self, category: str, pid: int):
    """Register a new process for monitoring"""
    if self._add_process(category, pid):
        self._ensure_thread_running()
```

---

## 3. WALLPAPER CHANGE FLOW (controller.py)

### Application Entry Point

**File**: `py_GUI/ui/pages/wallpapers.py` line 769

```python
def apply_wallpaper(self, wp_id: str):
    self.controller.apply(wp_id, self.selected_screen)
    self.update_active_wallpaper_label()
```

### Controller Apply Method

**File**: `py_GUI/core/controller.py` lines 33-59

```python
def apply(self, wp_id: str, screen: Optional[str] = None, screens: Optional[List[str]] = None):
    """Apply wallpaper (Multi-monitor support)"""
    
    # Determine target screens
    target_screens = []
    if screens:
        target_screens = screens
    elif screen:
        target_screens = [screen]
    else:
        last = self.config.get("lastScreen")
        if not last or last == "None":
            last = "eDP-1"
        target_screens = [last]
    
    # Update config
    active_monitors = self.config.get("active_monitors", {})
    for s in target_screens:
        active_monitors[s] = wp_id
    self.config.set("active_monitors", active_monitors)
    self.config.set("lastWallpaper", wp_id)
    
    if len(target_screens) == 1:
        self.config.set("lastScreen", target_screens[0])
    
    # Restart with new configuration
    self.log_manager.add_info(f"Applying wallpaper {wp_id} to {target_screens}", "Controller")
    self.restart_wallpapers()  # ← KEY POINT
```

### Restart Wallpapers - Process List Update

**File**: `py_GUI/core/controller.py` lines 74-199

```python
def restart_wallpapers(self):
    """Restart the engine with current active_monitors configuration"""
    
    # STEP 1: Stop old process
    self.stop()  # ← Line 76
    
    # STEP 2: Validate screens
    active_monitors = self.config.get("active_monitors", {})
    connected_screens = self.screen_manager.get_screens()
    valid_monitors = {scr: wid for scr, wid in active_monitors.items() if scr in connected_screens}
    
    if len(valid_monitors) != len(active_monitors):
        self.log_manager.add_info(f"Removing disconnected screens from config", "Controller")
        self.config.set("active_monitors", valid_monitors)
        active_monitors = valid_monitors
    
    if not active_monitors:
        self.log_manager.add_info("No active wallpapers for connected screens.", "Controller")
        return
    
    # STEP 3: Build command
    cmd = ["linux-wallpaperengine"]
    for scr, wid in active_monitors.items():
        cmd.extend(["--screen-root", scr, "--bg", str(wid)])
    
    cmd.extend(["-f", str(self.config.get("fps", 30))])
    
    # ... add more parameters ...
    
    self._last_command = cmd
    self.log_manager.add_debug(f"Executing: {' '.join(cmd)}", "Controller")
    
    try:
        # STEP 4: Start new process
        log_path = os.path.join(CONFIG_DIR, "engine_last.log")
        self.engine_log = open(log_path, "w")
        
        self.current_proc = subprocess.Popen(  # ← Line 175
            cmd,
            stdout=self.engine_log,
            stderr=self.engine_log
        )
        
        import time
        time.sleep(0.5)
        if self.current_proc.poll() is not None:
            # Process died immediately
            self.engine_log.close()
            with open(log_path, "r") as f:
                output = f.read()
            error_msg = f"Process exited immediately!\nOutput:\n{output}"
            self.log_manager.add_error(error_msg, "Engine")
            self.show_toast("❌ Wallpaper engine failed to start - check logs")
            return
        
        self.log_manager.add_info("Engine started successfully", "Controller")
        
        # STEP 5: Update performance monitoring  ← Lines 195-198
        if self.current_proc and self.current_proc.pid:
            self.perf_monitor.stop_all_backends()  # ← Remove old monitoring
            self.perf_monitor.start_monitoring("backend", self.current_proc.pid)  # ← Add new
    
    except Exception as e:
        self.log_manager.add_error(f"Failed to start engine: {e}", "Controller")
        self.show_toast(f"❌ Failed to start engine: {e}")
```

### Stop Method - Process Cleanup

**File**: `py_GUI/core/controller.py` lines 270-291

```python
def stop(self):
    """Stop wallpaper"""
    self.log_manager.add_info("Stopping wallpaper", "Controller")
    
    # Remove from performance monitoring
    self.perf_monitor.stop_all_backends()  # ← Line 274
    
    if self.current_proc:
        self.current_proc.terminate()  # ← Send SIGTERM
        self.current_proc = None
        
        # Close log file handle if open
        if hasattr(self, 'engine_log') and self.engine_log and not self.engine_log.closed:
            try:
                self.engine_log.close()
            except:
                pass
    
    # Backup kill to ensure cleanup
    subprocess.run(
        ["pkill", "-f", "linux-wallpaperengine"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False
    )
```

---

## 4. COMPLETE WALLPAPER CHANGE TIMELINE

### Time-Based Sequence

```
T=0ms:      User clicks "Apply Wallpaper" in UI
            → wallpapers.py:769 calls apply_wallpaper()

T+0ms:      apply_wallpaper() calls controller.apply(wp_id, screen)
            → config updated with active_monitors[screen] = wp_id

T+1ms:      controller.apply() calls restart_wallpapers()
            
T+10ms:     ┌─── PROCESS KILLING PHASE ───┐
            │ stop() is called (line 76)
            │ perf_monitor.stop_all_backends() (line 274)
            │   - Removes all "backend*" entries from _processes dict
            │   - Clears _history for removed categories
            │   - MONITORING LOOP may be mid-update!
            │
            │ current_proc.terminate() sent (SIGTERM)
            │ pkill -f linux-wallpaperengine (backup)

T+50ms:     Old process receives SIGTERM
            Old process exits gracefully
            
T+100ms:    ┌─── PROCESS CREATION PHASE ───┐
            │ subprocess.Popen() creates NEW process
            │ Gets new PID (e.g., 12345)
            │ Stores in self.current_proc
            │ Redirects stdout/stderr to engine_last.log

T+600ms:    Check if process crashed (poll())
            If alive: continue to monitoring startup

T+700ms:    ┌─── MONITORING UPDATE PHASE ───┐
            │ perf_monitor.stop_all_backends() (line 197) [2nd time!]
            │   - No effect if already cleared
            │   - Defensive call
            │
            │ perf_monitor.start_monitoring("backend", new_pid)
            │   - Calls _add_process("backend", new_pid)
            │   - Searches child processes
            │   - Finds linux-wallpaperengine child
            │   - Creates deque history (60 slots)
            │   - Calls _ensure_thread_running()
            │     - If monitor loop not active: starts it

T+1000ms:   ┌─── PERFORMANCE MONITORING LOOP ───┐
            │ Wakes up every 1 second
            │ Iterates: for category, proc in list(_processes.items())
            │ If "backend" in dict:
            │   - Reads CPU, memory, threads
            │   - Appends to history deques
            │   - Sends stats via _notify() callback
            │ If process dead: removes from _processes

T+2000ms:   ┌─── TRAY POLL CYCLE ───┐
            │ Tray's _poll_state() runs (every 2 seconds)
            │ Scans /proc for linux-wallpaperengine in cmdline
            │ Sets self.is_running based on result
            │ Toggle button now knows new state
```

---

## 5. CRITICAL ISSUES & RACE CONDITIONS

### Issue 1: Monitoring Gap During Restart

**Problem**: Process can be briefly unmonitored

**Scenario**:
1. `T=10ms`: `stop_all_backends()` removes "backend" from `_processes`
2. `T=50ms`: Old process exits
3. `T=100ms`: New process starts with PID 12345
4. `T=700ms`: `start_monitoring()` adds "backend" back
5. **Gap**: Between T=100ms and T=700ms, the process is NOT in the monitoring dict
6. If monitoring loop runs during this gap, no stats collected for this process

**Impact**: Performance graph shows gap or drop to zero

### Issue 2: Double Cleanup Call

**Problem**: `stop_all_backends()` called twice

**Lines**:
- Line 274: Inside `stop()` method
- Line 197: Inside `restart_wallpapers()` after starting new process

**Effect**: Second call is redundant but harmless (dict already empty)

**Risk**: If timing changes, could remove monitoring before new process starts

### Issue 3: Tray/Monitor Desynchronization

**Timeline**:
```
T=0ms:      User applies wallpaper
T=50ms:     Old process killed → Tray process immediately dead
T=100ms:    New process started → But Tray doesn't know yet!
T=2000ms:   Tray poll runs → Detects new process
            ↓
            Gap of 1900ms where tray UI doesn't know process changed!
```

**Manifestation**:
- User applies wallpaper
- UI updates immediately (has new config)
- Tray still shows "stopped" for 2 seconds
- After 2 seconds, tray updates to "running"

### Issue 4: Process Search Strategy Mismatch

**Tray approach**:
```
Iterates /proc:
  Read /proc/{pid}/cmdline
  Search for string "linux-wallpaperengine"
  Ignore if cmdline contains "python" or "grep"
```

**Performance Monitor approach**:
```
Given parent PID:
  Search children with proc.children(recursive=True)
  Match child.name() == "linux-wallpaperengine"
  If no match: track parent
```

**Disagreement scenario**:
- If linux-wallpaperengine is renamed (unusual but possible)
- If it's a wrapper process with different name
- Tray might detect one but PerformanceMonitor another

### Issue 5: Threading Safety

**Location**: `py_GUI/core/performance.py` line 104

```python
for category, proc in list(self._processes.items()):  # Snapshot!
```

**What's protected**: The `.items()` call is snapshotted with `list()`
- Prevents RuntimeError if dict modified during iteration

**What's NOT protected**:
- `_processes.pop()` at line 140 (cleanup)
- `_add_process()` modifying `_processes` at line 66
- No mutex/Lock object visible

**Risk**: If another thread calls `start_monitoring()` while loop iterates, could skip that process in current cycle

### Issue 6: Process Stale Reference

**Scenario**:
1. `start_monitoring("backend", 12345)` called
2. Stores `psutil.Process(12345)` in `_processes["backend"]`
3. Next cycle (1 second later), process still in dict but might be dead
4. `proc.cpu_percent()` raises `NoSuchProcess`
5. Process is removed from dict
6. No more monitoring until new wallpaper applied

**Gap period**: 0-1 second between process death and removal

### Issue 7: Config/Monitoring Mismatch

**Sequence**:
```
1. apply() updates config with active_monitors[screen] = wp_id
2. stop() called → monitoring removed
3. restart_wallpapers() called → new process started
4. But what if start_monitoring() fails?
5. Config thinks wallpaper is running
6. Monitoring has no process
7. UI shows running, but PerformanceMonitor has no data
```

---

## 6. HOW PROCESS LIST IS UPDATED

### Entry Points

1. **During Wallpaper Application**:
   ```
   WallpapersPage.apply_wallpaper()
     → WallpaperController.apply()
       → WallpaperController.restart_wallpapers()
         → stop()
           → perf_monitor.stop_all_backends()
         → subprocess.Popen(cmd)
         → perf_monitor.start_monitoring("backend", new_pid)
   ```

2. **During Wallpaper Stop**:
   ```
   WallpapersPage.on_stop_clicked()
     → WallpaperController.stop_screen()
       → WallpaperController.restart_wallpapers()
         → [same as above]
   ```

3. **During Screenshot**:
   ```
   No direct interaction with process list
   Creates separate subprocess via take_screenshot()
   Does NOT add to monitoring
   ```

### Callback Notification

**PerformanceMonitor notifies via callbacks**:

```python
def _notify(self, stats: Dict):
    for cb in self._callbacks:
        try:
            cb(stats)
        except Exception as e:
            print(f"[PerformanceMonitor] Callback error: {e}")
```

**Who registers callbacks**:
- Performance page UI components listen for stats updates
- Receives updated metrics every 1 second
- Updates graphs and labels

### Frontend Process

**Special case** (line 39):
```python
self._add_process("frontend", psutil.Process().pid)
```

- Tracks the GUI process itself
- Never automatically removed (line 139: `if category != "frontend"`)
- Always monitored for comparison

---

## Summary Table

| Aspect | Tray | PerformanceMonitor | Controller |
|--------|------|-------------------|------------|
| **Update Interval** | 2 seconds | 1 second | On-demand |
| **Data Source** | `/proc` files | psutil library | subprocess |
| **Tracks** | Any instance | Specific PID | Specific PID |
| **State** | Boolean (running/stopped) | Detailed metrics | Process object |
| **Cleanup** | Manual polling | Auto on exception | Manual stop() |
| **Sync Method** | None | Callback events | Config updates |
| **Thread Safe** | Unknown | Snapshot iteration | Single-threaded |

---

## Recommendations for Debugging

1. **Monitor Process State**: Watch controller.py lines 76-198 during wallpaper changes
2. **Check Monitoring Dict**: Add logging to `_add_process()` and `stop_all_backends()`
3. **Profile Timing**: Measure delay between old process death and new process registration
4. **Trace Tray Polling**: Add logging to `_poll_state()` to see detection lag
5. **Add Synchronization**: Consider using threading.Lock for `_processes` dict access
6. **Reduce Polling**: Increase tray poll interval or use inotify on `/proc`
