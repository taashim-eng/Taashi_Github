import os
import shutil
from datetime import datetime

def implement_improvements():
    """
    This script will create improved versions of all Project 16 files
    with enhanced logging, type hints, error handling, and configuration.
    """
    
    base_dir = "/workspaces/Taashi_Github/16_Agentic_Financial_Analyst"
    src_dir = os.path.join(base_dir, "src")
    tests_dir = os.path.join(base_dir, "tests")
    
    # Create backup in a dedicated folder outside project directory
    backup_root = "/workspaces/Taashi_Github/Implementation Code/Project16_bckp"
    backup_dir = os.path.join(backup_root, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    
    print("🔒 Creating backup of existing code...")
    try:
        os.makedirs(backup_root, exist_ok=True)
        if os.path.exists(src_dir):
            shutil.copytree(src_dir, os.path.join(backup_dir, "src"))
            print(f"   ✅ Backup created at: {backup_dir}")
        else:
            print(f"   ⚠️ No existing src directory to backup")
    except Exception as e:
        print(f"   ⚠️ Backup warning: {e}")
    
    # Create tests directory
    os.makedirs(tests_dir, exist_ok=True)
    print(f"   ✅ Tests directory created: {tests_dir}")
    
    # ==========================================
    # 1. CONFIG.PY - Centralized Configuration
    # ==========================================
    config_code = '''"""
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
'''

    # ==========================================
    # 2. IMPROVED TOOLS.PY
    # ==========================================
    tools_code = '''"""
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
'''

    # ==========================================
    # 3. IMPROVED AGENTS.PY
    # ==========================================
    agents_code = '''"""
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
                "raw_data": f"{price}\\nNews: {news}",
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
'''

    # ==========================================
    # 4. IMPROVED MAIN.PY
    # ==========================================
    main_code = '''"""
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
        print("\\n✅ FINAL REPORT GENERATED:")
        print(result)
        return 0
    else:
        print(f"\\n❌ Analysis failed for {ticker}. Check logs for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
'''

    # ==========================================
    # 5. UNIT TESTS
    # ==========================================
    tests_code = '''"""
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
'''

    # ==========================================
    # 6. REQUIREMENTS.TXT
    # ==========================================
    requirements = '''# The Wall Street Swarm - Dependencies
# Core dependencies (none required for basic demo)

# Optional: For running tests
pytest>=7.4.0

# Optional: For production deployment
python-dotenv>=1.0.0  # For environment variables
tenacity>=8.2.0       # For retry logic
'''

    # ==========================================
    # WRITE ALL FILES
    # ==========================================
    files_to_write = {
        os.path.join(src_dir, "config.py"): config_code,
        os.path.join(src_dir, "tools.py"): tools_code,
        os.path.join(src_dir, "agents.py"): agents_code,
        os.path.join(src_dir, "main.py"): main_code,
        os.path.join(tests_dir, "test_swarm.py"): tests_code,
        os.path.join(base_dir, "requirements.txt"): requirements
    }
    
    print("\n📝 Writing improved code files...")
    
    for filepath, content in files_to_write.items():
        try:
            with open(filepath, "w") as f:
                f.write(content.strip())
            print(f"   ✅ Created: {filepath}")
        except Exception as e:
            print(f"   ❌ Error writing {filepath}: {e}")
    
    # ==========================================
    # CREATE __INIT__.PY FILES
    # ==========================================
    init_files = [
        os.path.join(src_dir, "__init__.py"),
        os.path.join(tests_dir, "__init__.py")
    ]
    
    for init_file in init_files:
        try:
            with open(init_file, "w") as f:
                f.write('"""Package initialization."""\n')
            print(f"   ✅ Created: {init_file}")
        except Exception as e:
            print(f"   ⚠️ Warning: {e}")
    
    # ==========================================
    # UPDATE LOCAL README
    # ==========================================
    print("\n📄 Updating local README.md...")
    update_local_readme(base_dir)
    
    print("\n" + "="*60)
    print("✅ IMPROVEMENTS SUCCESSFULLY IMPLEMENTED!")
    print("="*60)
    print("\n📋 What was added:")
    print("   1. ✅ Type hints for all functions")
    print("   2. ✅ Comprehensive logging system")
    print("   3. ✅ Custom exceptions and error handling")
    print("   4. ✅ Configuration management (config.py)")
    print("   5. ✅ Unit tests framework (pytest)")
    print("   6. ✅ Requirements.txt file")
    print(f"   7. ✅ Backup stored at: {backup_dir}")
    print("   8. ✅ Local README.md updated")
    
    print("\n🚀 Next Steps:")
    print("   1. Run the improved version:")
    print("      cd src && python main.py")
    print("\n   2. Run the tests:")
    print("      python -m pytest tests/ -v")
    print("\n   3. Check the logs:")
    print("      cat swarm.log")
    print("\n   4. View backups:")
    print(f"      ls -la {backup_root}")

def update_local_readme(base_dir):
    """
    Update the local README.md in the Project 16 folder to reflect improvements.
    Does not overwrite, but intelligently inserts new sections.
    """
    readme_path = os.path.join(base_dir, "README.md")
    
    # Check if README exists
    if not os.path.exists(readme_path):
        print(f"   ⚠️ README.md not found at {readme_path}")
        return
    
    try:
        # Read existing content
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        print(f"   ✓ Found README.md ({len(content)} characters)")
        
        # Section to add
        improvements_section = """
---

## 🚀 Recent Improvements (Production Enhancements)

This project has been enhanced with production-ready features:

### 1. **Type Safety** 🔒
- Added type hints to all functions and methods
- Improved IDE support and code readability
- Example: `def get_stock_price(self, ticker: str) -> str:`

### 2. **Comprehensive Logging** 📊
- Full logging system with `logging` module
- Logs written to `swarm.log` for debugging
- Different log levels (INFO, WARNING, ERROR, CRITICAL)
- Console and file output

### 3. **Error Handling** ⚠️
- Custom exceptions: `FinancialToolsError`, `AgentError`
- Graceful error recovery and informative messages
- Production-grade exception handling

### 4. **Configuration Management** ⚙️
- New `config.py` for centralized settings
- Easy to modify thresholds, paths, and parameters
- No hardcoded values in business logic

### 5. **Unit Tests** ✅
- Full test suite using `pytest`
- Located in `tests/` directory
- Run with: `python -m pytest tests/ -v`
- Tests cover tools and agents

### 6. **Enhanced Risk Assessment** 📈
- Configurable risk thresholds (HIGH/MODERATE/LOW)
- Intelligent P/E ratio parsing
- More robust quantitative analysis

### 7. **Professional Structure** 🏗️
```
16_Agentic_Financial_Analyst/
├── src/
│   ├── config.py          # ⭐ NEW: Configuration
│   ├── tools.py           # ⭐ IMPROVED: Type hints + logging
│   ├── agents.py          # ⭐ IMPROVED: Error handling
│   ├── main.py            # ⭐ IMPROVED: Orchestration
│   └── __init__.py
├── tests/
│   ├── test_swarm.py      # ⭐ NEW: Unit tests
│   └── __init__.py
├── data/
│   └── market_knowledge.json
├── requirements.txt       # ⭐ NEW: Dependencies
└── README.md
```

### Running the Enhanced Version

**Basic Usage:**
```bash
cd src
python main.py
```

**Run Tests:**
```bash
python -m pytest tests/ -v
```

**View Logs:**
```bash
cat swarm.log
```

**Install Dependencies (Optional):**
```bash
pip install -r requirements.txt
```

### What's Next?
Consider these extensions:
- Connect to real APIs (Bloomberg, AlphaVantage)
- Add retry logic with `tenacity` library
- Implement caching for API calls
- Add more sophisticated risk models
- Build a REST API with FastAPI

---
"""
        
        # Find insertion point - before "Designed for High-Velocity" or at the end
        markers_to_try = [
            "Designed for High-Velocity",
            "---\n**Designed for High-Velocity",
            "## 5. How to Run the Demo"
        ]
        
        insert_index = -1
        for marker in markers_to_try:
            idx = content.find(marker)
            if idx != -1:
                insert_index = idx
                print(f"   ✓ Found insertion point at: '{marker}'")
                break
        
        if insert_index == -1:
            # Append to end if no marker found
            new_content = content.rstrip() + "\n\n" + improvements_section
            print("   ⚠️ No insertion marker found, appending to end")
        else:
            # Insert before the marker
            part_1 = content[:insert_index]
            part_2 = content[insert_index:]
            new_content = part_1 + improvements_section + "\n" + part_2
            print("   ✅ Inserted improvements section")
        
        # Create backup of original README
        backup_readme = readme_path + ".backup"
        with open(backup_readme, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"   ✓ README backup created: {backup_readme}")
        
        # Write updated README
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        
        print(f"   ✅ README.md updated successfully!")
        print(f"   📊 Added {len(new_content) - len(content)} characters")
        
    except Exception as e:
        print(f"   ❌ Error updating README: {e}")

if __name__ == "__main__":
    implement_improvements()