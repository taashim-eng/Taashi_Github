"""
Unit tests for The Wall Street Swarm.
Run with: python -m pytest tests/
"""
import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tools import FinancialTools, FinancialToolsError
from agents import ResearcherAgent, QuantAgent, WriterAgent, AgentError

class TestFinancialTools:
    """Test suite for FinancialTools."""
    
    @pytest.fixture
    def tools(self):
        """Create tools instance for testing."""
        return FinancialTools()
    
    def test_get_stock_price_valid(self, tools):
        """Test getting price for valid ticker."""
        result = tools.get_stock_price("NVDA")
        assert "NVDA" in result
        assert "$" in result
    
    def test_get_stock_price_invalid(self, tools):
        """Test getting price for invalid ticker."""
        with pytest.raises(FinancialToolsError):
            tools.get_stock_price("INVALID")
    
    def test_get_recent_news(self, tools):
        """Test getting news for valid ticker."""
        result = tools.get_recent_news("TSLA")
        assert isinstance(result, str)
        assert len(result) > 0

class TestAgents:
    """Test suite for Agents."""
    
    @pytest.fixture
    def tools(self):
        return FinancialTools()
    
    def test_researcher_agent(self, tools):
        """Test ResearcherAgent execution."""
        agent = ResearcherAgent("Test", "Researcher", tools)
        result = agent.execute("NVDA")
        
        assert "ticker" in result
        assert result["ticker"] == "NVDA"
        assert "raw_data" in result
    
    def test_quant_agent(self, tools):
        """Test QuantAgent execution."""
        agent = QuantAgent("Test", "Quant", tools)
        research_data = {
            "ticker": "NVDA",
            "raw_data": "NVDA Current Price: $890.00 (P/E: 95.2)"
        }
        
        result = agent.execute(research_data)
        assert "risk_assessment" in result
        assert result["risk_assessment"] in ["LOW", "MODERATE", "HIGH"]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])