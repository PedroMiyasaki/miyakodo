import MetaTrader5 as mt5
import pandas as pd
import time
from datetime import datetime
import pytz
from pathlib import Path

from miyakodo.common.config import load_config
from miyakodo.loggers.intraday import setup_logger, log_save_stats

# Setup logger
logger = setup_logger()

def initialize_mt5():
    """Initialize MetaTrader5 connection"""
    if not mt5.initialize():
        logger.error(f"Failed to initialize MT5: {mt5.last_error()}")
        return False
    return True

def get_market_book(symbol):
    """Get market book data for a specified symbol"""
    if not mt5.symbol_select(symbol, True):
        logger.error(f"symbol_select() failed for {symbol}, error code = {mt5.last_error()}")
        return None
    
    book = mt5.market_book_get(symbol)
    if book is None:
        logger.error(f"market_book_get() failed for {symbol}, error code = {mt5.last_error()}")
        return None
    
    return book

def save_data(data, symbol, timestamp, config):
    """Save collected data to parquet file"""
    save_path = Path(config['data']['intraday']) / symbol
    save_path.mkdir(parents=True, exist_ok=True)
    
    # Create filename with date and hour
    filename = f"{symbol}_{timestamp.strftime('%Y%m%d_%H%M')}.parquet"
    filepath = save_path / filename
    
    df = pd.DataFrame(data)
    df.to_parquet(filepath)
    
    # Log save statistics
    log_save_stats(logger, symbol, len(data), timestamp)

def is_trading_hours(config):
    """Check if current time is within trading hours"""
    brt = pytz.timezone('America/Sao_Paulo')
    now = datetime.now(brt)
    
    start_time = datetime.strptime(config['pipelines']['intraday']['trading_hours']['start'], '%H:%M').time()
    end_time = datetime.strptime(config['pipelines']['intraday']['trading_hours']['end'], '%H:%M').time()
    
    return start_time <= now.time() <= end_time

def collect_data():
    """Main data collection loop"""
    config = load_config(Path(__file__).parent.parent.parent.parent.parent / 'configs' / 'config.yaml')
    symbols = config['pipelines']['intraday']['symbols']
    save_interval = config['pipelines']['intraday']['save_interval']
    collection_interval = config['pipelines']['intraday']['collection_interval_seconds']
    
    # Check if we're in trading hours
    if not is_trading_hours(config):
        brt = pytz.timezone('America/Sao_Paulo')
        now = datetime.now(brt)
        logger.info(f"Outside trading hours. Current time: {now.strftime('%H:%M')} BRT")
        return
    
    logger.info(f"Starting intraday data collection for symbols: {', '.join(symbols)}")
    
    if not initialize_mt5():
        return
    
    try:
        last_save_time = datetime.now()
        collected_data = {symbol: [] for symbol in symbols}
        collection_started = True
        
        while is_trading_hours(config):
            current_time = datetime.now()
            
            # Collect data for each symbol
            for symbol in symbols:
                book = get_market_book(symbol)
                if book:
                    data_point = {
                        'timestamp': current_time,
                        'symbol': symbol,
                        'book': book
                    }
                    collected_data[symbol].append(data_point)
            
            # Save data periodically
            if (current_time - last_save_time).total_seconds() >= save_interval * 60:
                for symbol in symbols:
                    if collected_data[symbol]:
                        save_data(collected_data[symbol], symbol, current_time, config)
                        collected_data[symbol] = []
                last_save_time = current_time
            
            time.sleep(collection_interval)  # Wait for configured interval before next collection
            
    except Exception as e:
        logger.error(f"Error in data collection: {str(e)}")
        
    finally:
        if collection_started:
            mt5.shutdown()
            logger.info("Intraday data collection finished")

if __name__ == "__main__":
    collect_data() 