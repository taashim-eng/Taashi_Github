"""
Agent implementations with enhanced error handling and logging.
Each agent represents a specialized role in the financial analysis workflow.
"""
import time
import logging
from typing import Dict, Any, Optional, Tuple
from config import AGENT_TIMEOUT, RISK_THRESHOLDS

logger = logging.getLogger(__name__)

class AgentError(Exception):
    """Custom exception for agent errors."""
    pass

class Agent:
    """
    Base class for all agents in the swarm.
    Provides common functionality for thinking and execution.
    """
    
    def __init__(self, name: str, role: str, tools: Optional[Any] = None):
        """
        Initialize an agent.
        
        Args:
            name: Agent's name (e.g., "Alice")
            role: Agent's role (e.g., "Senior Researcher")
            tools: Tools object for accessing market data
        """
        self.name = name
        self.role = role
        self.tools = tools
        logger.info(f"Initialized {self.name} ({self.role})")
    
    def think(self, prompt: Any) -> Any:
        """
        Main thinking method that simulates LLM reasoning.
        
        Args:
            prompt: Input data for the agent to process
        
        Returns:
            Agent's output after processing
        """
        logger.info(f"{self.name} ({self.role}): Starting analysis...")
        
        try:
            # Simulate API call latency
            time.sleep(1)
            result = self.execute(prompt)
            logger.info(f"{self.name}: Analysis complete")
            return result
        
        except Exception as e:
            logger.error(f"{self.name}: Error during execution - {e}")
            raise AgentError(f"{self.name} failed: {e}")
    
    def execute(self, prompt: Any) -> Any:
        """
        Execute agent-specific logic.
        Must be implemented by subclasses.
        """
        raise NotImplementedError(f"{self.__class__.__name__} must implement execute()")

class ResearcherAgent(Agent):
    """
    Researcher agent responsible for gathering market data.
    Acts as the "eyes" of the swarm.
    """
    
    def execute(self, ticker: str) -> Dict[str, Any]:
        """
        Fetch market data for the given ticker.
        
        Args:
            ticker: Stock ticker to research
        
        Returns:
            Dictionary with ticker and raw market data
        """
        logger.info(f"{self.name}: Fetching data for {ticker}")
        
        if not self.tools:
            raise AgentError(f"{self.name}: No tools available")
        
        try:
            price = self.tools.get_stock_price(ticker)
            news = self.tools.get_recent_news(ticker)
            
            result = {
                "ticker": ticker,
                "raw_data": f"{price}\nNews: {news}",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            logger.info(f"{self.name}: Successfully gathered data for {ticker}")
            return result
        
        except Exception as e:
            logger.error(f"{self.name}: Failed to fetch data - {e}")
            raise AgentError(f"Research failed for {ticker}: {e}")

class QuantAgent(Agent):
    """
    Quantitative analyst agent responsible for risk assessment.
    Acts as the "brain" for financial modeling.
    """
    
    def execute(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze research data and assess risk.
        
        Args:
            research_data: Output from ResearcherAgent
        
        Returns:
            Dictionary with risk assessment and analysis
        """
        ticker = research_data.get("ticker", "UNKNOWN")
        logger.info(f"{self.name}: Analyzing risk for {ticker}")
        
        if not self.tools:
            raise AgentError(f"{self.name}: No tools available")
        
        try:
            raw = research_data.get("raw_data", "")
            
            # Extract P/E ratio from raw data
            pe_ratio = self._extract_pe_ratio(raw)
            risk_level = self._calculate_risk(pe_ratio)
            
            metrics = self.tools.get_financial_metrics(ticker)
            
            result = {
                "ticker": ticker,
                "risk_assessment": risk_level,
                "pe_ratio": pe_ratio,
                "quantitative_analysis": f"Valuation is {risk_level}. P/E Ratio: {pe_ratio}. Metrics: {metrics}",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            logger.info(f"{self.name}: Risk assessment complete - {risk_level}")
            return result
        
        except Exception as e:
            logger.error(f"{self.name}: Analysis failed - {e}")
            raise AgentError(f"Quantitative analysis failed: {e}")
    
    def _extract_pe_ratio(self, raw_data: str) -> float:
        """Extract P/E ratio from raw data string."""
        try:
            # Simple parsing: look for "P/E: XX.X"
            if "P/E:" in raw_data:
                pe_str = raw_data.split("P/E:")[1].split(")")[0].strip()
                return float(pe_str)
            return 0.0
        except (ValueError, IndexError):
            logger.warning("Could not extract P/E ratio, using 0.0")
            return 0.0
    
    def _calculate_risk(self, pe_ratio: float) -> str:
        """Calculate risk level based on P/E ratio thresholds."""
        if pe_ratio >= RISK_THRESHOLDS["HIGH"]:
            return "HIGH"
        elif pe_ratio >= RISK_THRESHOLDS["MODERATE"]:
            return "MODERATE"
        else:
            return "LOW"

class WriterAgent(Agent):
    """
    Writer agent responsible for synthesizing final reports.
    Acts as the "voice" of the swarm.
    """
    
    def execute(self, analysis_data: Tuple[Dict[str, Any], Dict[str, Any]]) -> str:
        """
        Generate investment memo from research and quant analysis.
        
        Args:
            analysis_data: Tuple of (research_output, quant_output)
        
        Returns:
            Formatted investment memo
        """
        research, quant = analysis_data
        ticker = research.get("ticker", "UNKNOWN")
        
        logger.info(f"{self.name}: Drafting report for {ticker}")
        
        try:
            report = f"""
=== INVESTMENT MEMO: {ticker} ===
DATE: {time.strftime("%Y-%m-%d %H:%M:%S")}
ANALYST: {self.name} ({self.role})

1. MARKET SNAPSHOT
{research.get('raw_data', 'No data available')}

2. QUANTITATIVE ANALYSIS
Risk Level: {quant.get('risk_assessment', 'UNKNOWN')}
P/E Ratio: {quant.get('pe_ratio', 'N/A')}
{quant.get('quantitative_analysis', 'No analysis available')}

3. RECOMMENDATION
Based on the {quant.get('risk_assessment', 'UNKNOWN')} risk profile and current market conditions,
we recommend a {'HOLD' if quant.get('risk_assessment') == 'HIGH' else 'BUY'} strategy.

DISCLAIMER: This is a simulated analysis for demonstration purposes only.
Not financial advice. Consult a licensed financial advisor before investing.

---
Generated by The Wall Street Swarm v1.0
"""
            
            logger.info(f"{self.name}: Report draft complete")
            return report
        
        except Exception as e:
            logger.error(f"{self.name}: Report generation failed - {e}")
            raise AgentError(f"Report writing failed: {e}")