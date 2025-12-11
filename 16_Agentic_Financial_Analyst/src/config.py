"""
Configuration file for The Wall Street Swarm.
Centralized settings for easy maintenance and deployment.
"""
import os
from typing import List

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")
DATA_PATH = os.path.join(DATA_DIR, "market_knowledge.json")

# Supported tickers
SUPPORTED_TICKERS: List[str] = ["TSLA", "NVDA", "AAPL", "MSFT", "GOOGL"]

# Risk assessment thresholds
RISK_THRESHOLDS = {
    "HIGH": 90.0,      # P/E ratio above this = HIGH risk
    "MODERATE": 50.0,  # P/E ratio between MODERATE and HIGH
    "LOW": 30.0        # P/E ratio below MODERATE
}

# Agent configuration
AGENT_TIMEOUT = 30  # seconds
MAX_RETRIES = 3

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"