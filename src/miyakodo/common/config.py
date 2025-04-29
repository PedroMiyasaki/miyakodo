"""
Configuration management module.
Handles loading and managing configuration settings.
"""

import yaml
from pathlib import Path

def load_config(config_path: str) -> dict:
    """
    Load configuration from YAML file.
    Args:
        config_path (str): Path to configuration file
    Returns:
        dict: Configuration settings
    """
    with open(config_path, 'r') as f:
        return yaml.safe_load(f) 