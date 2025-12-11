"""
Financial tools module with enhanced error handling and type hints.
These tools provide deterministic access to market data.
"""
import json
import os
import logging
from typing import Dict, Any, Optional
from config import DATA_PATH, SUPPORTED_TICKERS

logger = logging.getLogger(__name__)

class FinancialToolsError(Exception):
    """Custom exception for financial tools errors."""
    pass

class FinancialTools:
    """
    Provides deterministic tools for accessing market data.
    Designed to be easily swapped with real API clients (Bloomberg, AlphaVantage).
    """
    
    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize the financial tools with market data.
        
        Args:
            data_path: Path to the market data JSON file
        """
        self.data_path = data_path or DATA_PATH
        self.db: Dict[str, Any] = {}
        self._load_data()
    
    def _load_data(self) -> None:
        """Load market data from JSON file."""
        try:
            if not os.path.exists(self.data_path):
                raise FileNotFoundError(f"Data file not found: {self.data_path}")
            
            with open(self.data_path, "r") as f:
                self.db = json.load(f)
            
            logger.info(f"Loaded market data for {len(self.db)} tickers")
        
        except FileNotFoundError as e:
            logger.error(f"Data file not found: {e}")
            raise FinancialToolsError(f"Failed to load data: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in data file: {e}")
            raise FinancialToolsError(f"Invalid data format: {e}")
    
    def get_stock_price(self, ticker: str) -> str:
        """
        Get current stock price and P/E ratio.
        
        Args:
            ticker: Stock ticker symbol (e.g., "TSLA")
        
        Returns:
            Formatted string with price and P/E ratio
        
        Raises:
            FinancialToolsError: If ticker not found
        """
        ticker = ticker.upper()
        
        if ticker not in SUPPORTED_TICKERS:
            logger.warning(f"Unsupported ticker requested: {ticker}")
        
        data = self.db.get(ticker)
        if not data:
            logger.error(f"Ticker not found in database: {ticker}")
            raise FinancialToolsError(f"Ticker {ticker} not found in database")
        
        logger.info(f"Retrieved price data for {ticker}")
        return f"{ticker} Current Price: ${data['price']} (P/E: {data['pe_ratio']})"
    
    def get_recent_news(self, ticker: str) -> str:
        """
        Get recent news headlines for a ticker.
        
        Args:
            ticker: Stock ticker symbol
        
        Returns:
            News headlines separated by " | "
        
        Raises:
            FinancialToolsError: If ticker not found
        """
        ticker = ticker.upper()
        data = self.db.get(ticker)
        
        if not data:
            logger.error(f"Ticker not found: {ticker}")
            raise FinancialToolsError(f"Ticker {ticker} not found")
        
        if "news" not in data or not data["news"]:
            logger.warning(f"No news available for {ticker}")
            return "No recent news available."
        
        logger.info(f"Retrieved {len(data['news'])} news items for {ticker}")
        return " | ".join(data['news'])
    
    def get_financial_metrics(self, ticker: str) -> Dict[str, Any]:
        """
        Get financial metrics for a ticker.
        
        Args:
            ticker: Stock ticker symbol
        
        Returns:
            Dictionary with financial metrics
        
        Raises:
            FinancialToolsError: If ticker not found or metrics unavailable
        """
        ticker = ticker.upper()
        data = self.db.get(ticker)
        
        if not data:
            logger.error(f"Ticker not found: {ticker}")
            raise FinancialToolsError(f"Ticker {ticker} not found")
        
        if "financials" not in data:
            logger.error(f"No financial metrics for {ticker}")
            raise FinancialToolsError(f"Financial metrics not available for {ticker}")
        
        logger.info(f"Retrieved financial metrics for {ticker}")
        return data['financials']