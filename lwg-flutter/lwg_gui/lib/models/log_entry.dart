enum LogLevel { info, warn, error, debug }
enum LogSource { gui, core, engine, controller }

class LogEntry {
  final int id;
  final String timestamp;
  final LogLevel level;
  final LogSource source;
  final String message;

  const LogEntry({
    required this.id,
    required this.timestamp,
    required this.level,
    required this.source,
    required this.message,
  });
}