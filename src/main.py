"""
Main entry point for the Miyakodo application.
Provides manual pipeline triggering functionality.
"""

import argparse
from miyakodo.pipelines.daily import extract, transform, load, kpi, alert
from miyakodo.pipelines.weekly import extract as weekly_extract
from miyakodo.pipelines.weekly import transform as weekly_transform
from miyakodo.pipelines.weekly import load as weekly_load
from miyakodo.common.logging_utils import setup_logging

logger = setup_logging()

def run_daily_pipeline():
    """Run the daily pipeline."""
    logger.info("Starting daily pipeline")
    # Implementation here
    pass

def run_weekly_pipeline():
    """Run the weekly pipeline."""
    logger.info("Starting weekly pipeline")
    # Implementation here
    pass

def main():
    parser = argparse.ArgumentParser(description="Miyakodo Pipeline Runner")
    parser.add_argument("--pipeline", choices=["daily", "weekly"], required=True,
                      help="Pipeline to run")
    
    args = parser.parse_args()
    
    if args.pipeline == "daily":
        run_daily_pipeline()
    else:
        run_weekly_pipeline()

if __name__ == "__main__":
    main() 