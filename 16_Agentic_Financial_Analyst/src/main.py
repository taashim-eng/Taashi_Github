"""
Main orchestrator for The Wall Street Swarm.
Coordinates agent workflow and handles errors gracefully.
"""
import logging
import sys
from typing import Optional
from config import LOG_LEVEL, LOG_FORMAT, SUPPORTED_TICKERS
from tools import FinancialTools, FinancialToolsError
from agents import ResearcherAgent, QuantAgent, WriterAgent, AgentError

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('swarm.log')
    ]
)
logger = logging.getLogger(__name__)

class FinancialSwarm:
    """
    Orchestrates the multi-agent financial analysis workflow.
    """
    
    def __init__(self):
        """Initialize the swarm with tools and agents."""
        logger.info("Initializing Financial Swarm...")
        
        try:
            self.tools = FinancialTools()
            self.researcher = ResearcherAgent("Alice", "Senior Researcher", self.tools)
            self.quant = QuantAgent("Bob", "Quantitative Analyst", self.tools)
            self.writer = WriterAgent("Charlie", "Portfolio Manager", None)
            
            logger.info("Swarm initialization complete")
        
        except Exception as e:
            logger.critical(f"Failed to initialize swarm: {e}")
            raise
    
    def analyze(self, ticker: str) -> Optional[str]:
        """
        Run the complete analysis workflow for a ticker.
        
        Args:
            ticker: Stock ticker to analyze
        
        Returns:
            Final investment memo or None if analysis fails
        """
        ticker = ticker.upper()
        
        logger.info(f"="*60)
        logger.info(f"STARTING ANALYSIS FOR: {ticker}")
        logger.info(f"="*60)
        
        # Validate ticker
        if ticker not in SUPPORTED_TICKERS:
            logger.warning(f"Ticker {ticker} not in supported list: {SUPPORTED_TICKERS}")
        
        try:
            # Step 1: Research
            logger.info("Step 1/3: Research Phase")
            research_output = self.researcher.think(ticker)
            
            # Step 2: Quantitative Analysis
            logger.info("Step 2/3: Quantitative Analysis Phase")
            quant_output = self.quant.think(research_output)
            
            # Step 3: Report Writing
            logger.info("Step 3/3: Report Writing Phase")
            final_report = self.writer.think((research_output, quant_output))
            
            logger.info("Analysis workflow complete")
            return final_report
        
        except (FinancialToolsError, AgentError) as e:
            logger.error(f"Analysis failed for {ticker}: {e}")
            return None
        
        except Exception as e:
            logger.critical(f"Unexpected error during analysis: {e}")
            return None

def main():
    """Main entry point."""
    print("🚀 WALL STREET SWARM - Multi-Agent Financial Analysis System")
    print("="*60)
    
    # Initialize swarm
    try:
        swarm = FinancialSwarm()
    except Exception as e:
        print(f"❌ Failed to initialize swarm: {e}")
        return 1
    
    # Run analysis (you can change the ticker here)
    ticker = "NVDA"  # Change to TSLA, AAPL, etc.
    
    result = swarm.analyze(ticker)
    
    if result:
        print("\n✅ FINAL REPORT GENERATED:")
        print(result)
        return 0
    else:
        print(f"\n❌ Analysis failed for {ticker}. Check logs for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())