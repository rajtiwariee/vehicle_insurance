import logging
import logging.handlers
import os
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime
from from_root import from_root
# Global logger instance
_central_logger: Optional[logging.Logger] = None
_log_file_path: Optional[Path] = None


def setup_central_logger(
    log_file: str = "vehicle_insurance.log",
    log_level: str = "INFO",
    console_log_level: Optional[str] = None,
    file_log_level: Optional[str] = None,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    date_format: str = "%Y-%m-%d %H:%M:%S",
    settings=None,
    force_reinit: bool = False,
) -> logging.Logger:
    """
    Setup centralized logger that writes to a single file with rotation.

    Args:
        log_file: Name of the log file
        log_level: Default logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) - used when console/file levels not specified
        console_log_level: Logging level for console output (defaults to environment variable CONSOLE_LOG_LEVEL or WARNING)
        file_log_level: Logging level for file output (defaults to environment variable FILE_LOG_LEVEL or log_level)
        max_bytes: Maximum size of log file before rotation
        backup_count: Number of backup files to keep
        log_format: Format string for log messages
        date_format: Format string for timestamps
        settings: Settings instance to get log levels from
        force_reinit: Force reinitialization even if logger exists

    Returns:
        Configured logger instance
    """
    global _central_logger, _log_file_path

    if _central_logger is not None and not force_reinit:
        return _central_logger

    # If force_reinit, clear existing handlers
    if _central_logger is not None and force_reinit:
        for handler in _central_logger.handlers[:]:
            _central_logger.removeHandler(handler)
            handler.close()
        _central_logger = None

    # Determine log levels from settings, environment variables, or parameters
    if console_log_level is None:
        if settings is not None:
            console_log_level = settings.CONSOLE_LOG_LEVEL
        else:
            console_log_level = os.getenv("CONSOLE_LOG_LEVEL", "WARNING")
    if file_log_level is None:
        if settings is not None:
            file_log_level = settings.FILE_LOG_LEVEL
        else:
            file_log_level = os.getenv("FILE_LOG_LEVEL", log_level)

    # Create logs directory if it doesn't exist
    ROOT_DIR = Path(__file__).resolve().parent.parent
    log_dir = Path(f"{ROOT_DIR}/logs")
    log_dir.mkdir(exist_ok=True)

    # Set up log file path
    _log_file_path = log_dir / log_file

    # Create formatter
    formatter = logging.Formatter(log_format, date_format)

    # Create rotating file handler with specific log level
    file_handler = logging.handlers.RotatingFileHandler(
        _log_file_path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(getattr(logging, file_log_level.upper()))

    # Create console handler with specific log level
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(getattr(logging, console_log_level.upper()))

    # Create central logger - set to lowest level to allow handlers to filter
    _central_logger = logging.getLogger("cctv_analyzer")
    min_level = min(
        getattr(logging, console_log_level.upper()),
        getattr(logging, file_log_level.upper()),
    )
    _central_logger.setLevel(min_level)

    # Add handlers
    _central_logger.addHandler(file_handler)
    _central_logger.addHandler(console_handler)

    # Prevent propagation to avoid duplicate logs
    _central_logger.propagate = False

    return _central_logger


def get_logger(module_name: Optional[str] = None, settings=None) -> logging.Logger:
    """
    Get a logger instance for a specific module.

    Args:
        module_name: Name of the module (optional, will be auto-detected if None)

    Returns:
        Logger instance configured to write to the central log file
    """
    global _central_logger

    # Initialize central logger if not already done
    if _central_logger is None:
        setup_central_logger(settings=settings)

    # Get module name if not provided
    if module_name is None:
        import inspect

        frame = inspect.currentframe()
        try:
            # Go up the call stack to find the calling module
            while frame:
                frame = frame.f_back
                if frame and frame.f_globals.get("__name__") != __name__:
                    module_name = frame.f_globals.get("__name__", "unknown")
                    break
        finally:
            del frame

    # Create child logger for the module
    logger = _central_logger.getChild(module_name or "unknown")

    return logger


def get_log_file_path() -> Optional[Path]:
    """Get the path to the current log file."""
    return _log_file_path


def clear_logs() -> bool:
    """
    Clear all log files (main log and rotated backups).

    Returns:
        True if successful, False otherwise
    """
    global _log_file_path

    if _log_file_path is None:
        return False

    try:
        # Remove main log file
        if _log_file_path.exists():
            _log_file_path.unlink()

        # Remove rotated backup files
        for i in range(1, 6):  # Assuming backup_count=5
            backup_file = _log_file_path.with_suffix(f".{i}")
            if backup_file.exists():
                backup_file.unlink()

        return True
    except Exception as e:
        print(f"Error clearing logs: {e}")
        return False


def log_system_info():
    """Log system information for debugging purposes."""
    logger = get_logger("system_info")

    logger.info("=" * 50)
    logger.info("SYSTEM INFORMATION")
    logger.info("=" * 50)
    logger.info(f"Python Version: {sys.version}")
    logger.info(f"Platform: {sys.platform}")
    logger.info(f"Working Directory: {os.getcwd()}")
    logger.info(f"Log File: {get_log_file_path()}")
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    logger.info("=" * 50)


# Convenience function for quick logging
def log(level: str, message: str, module_name: Optional[str] = None):
    """
    Quick logging function for simple messages.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        message: Log message
        module_name: Optional module name
    """
    logger = get_logger(module_name)
    log_func = getattr(logger, level.lower())
    log_func(message)


def should_log(level: str, module_name: Optional[str] = None) -> bool:
    """
    Check if a given log level would be logged, useful for avoiding expensive
    log message construction when the message won't be output.

    Args:
        level: Log level to check (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        module_name: Optional module name

    Returns:
        True if the level would be logged, False otherwise
    """
    logger = get_logger(module_name)
    return logger.isEnabledFor(getattr(logging, level.upper()))


# Initialize logger when module is imported (will use environment variables as fallback)
if _central_logger is None:
    setup_central_logger()
