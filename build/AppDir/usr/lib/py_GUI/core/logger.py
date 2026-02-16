from datetime import datetime
from typing import List, Dict

class LogManager:
    def __init__(self, max_entries: int = 500):
        self._logs: List[Dict] = []
        self._max_entries = max_entries
        self._callbacks: List[callable] = []

    def add(self, level: str, message: str, source: str = "GUI"):
        """Add a log entry"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "level": level,
            "source": source,
            "message": message
        }
        self._logs.append(log_entry)

        # Limit log size
        if len(self._logs) > self._max_entries:
            self._logs = self._logs[-self._max_entries:]

        # Notify listeners
        for callback in self._callbacks:
            try:
                callback(log_entry)
            except Exception as e:
                print(f"[LOG] Callback error: {e}")

    def add_debug(self, message: str, source: str = "GUI"):
        self.add("DEBUG", message, source)

    def add_info(self, message: str, source: str = "GUI"):
        self.add("INFO", message, source)

    def add_warning(self, message: str, source: str = "GUI"):
        self.add("WARNING", message, source)

    def add_error(self, message: str, source: str = "GUI"):
        self.add("ERROR", message, source)

    def get_logs(self) -> List[Dict]:
        """Get all logs"""
        return self._logs.copy()

    def clear(self):
        """Clear logs"""
        self._logs.clear()

    def register_callback(self, callback: callable):
        """Register log update callback"""
        self._callbacks.append(callback)
