"""
Intraday pipeline logger.
Handles all logging for the intraday data collection pipeline.
"""

import logging
from pathlib import Path
from datetime import datetime

def setup_logger(log_dir: str = "logs/intraday", log_level: int = logging.INFO) -> logging.Logger:
    """
    Set up logging configuration for the intraday pipeline.
    Args:
        log_dir (str): Directory for log files
        log_level (int): Logging level
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create log directory with date-based subdirectory
    today = datetime.now().strftime('%Y%m%d')
    log_path = Path(log_dir) / today
    log_path.mkdir(parents=True, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger('miyakodo.intraday')
    logger.setLevel(log_level)
    
    # Clear any existing handlers
    logger.handlers = []
    
    # File handler for daily log file
    file_handler = logging.FileHandler(log_path / 'intraday.log')
    file_handler.setLevel(log_level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # Formatter with detailed information
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def log_save_stats(logger: logging.Logger, symbol: str, records_saved: int, timestamp: datetime):
    """
    Log statistics about saved data.
    Args:
        logger: Logger instance
        symbol: Trading symbol
        records_saved: Number of records saved
        timestamp: Timestamp of the save operation
    """
    logger.info(
        f"Saved {records_saved} records for {symbol} at {timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    ) 