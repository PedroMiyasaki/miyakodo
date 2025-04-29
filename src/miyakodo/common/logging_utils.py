"""
Logging utilities module.
Provides standardized logging functionality.
"""

import logging
from pathlib import Path

def setup_logging(log_dir: str = "logs", log_level: int = logging.INFO) -> logging.Logger:
    """
    Set up standardized logging configuration.
    Args:
        log_dir (str): Directory for log files
        log_level (int): Logging level
    Returns:
        logging.Logger: Configured logger instance
    """
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    file_handler = logging.FileHandler(Path(log_dir) / 'miyakodo.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger 