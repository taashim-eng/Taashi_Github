import os

base_dir = "/workspaces/Taashi_Github/16_Agentic_Financial_Analyst/src"

# ==========================================
# 1. TOOLS (The "Hands" of the Agents)
# ==========================================
tools_code = """
import json
import os

class FinancialTools:
    def __init__(self):
        # Load our mock database
        data_path = "../data/market_knowledge.json"
        with open(data_path, "r") as f:
            self.db = json.load(f)

    def get_stock_price(self, ticker):
        data = self.db.get(ticker)
        if data:
            return f"{ticker} Current Price: ${data['price']} (P/E: {data['pe_ratio']})"
        return "Ticker not found."

    def get_recent_news(self, ticker):
        data = self.db.get(ticker)
        if data:
            return " | ".join(data['news'])
        return "No news found."

    def get_financial_metrics(self, ticker):
        data = self.db.get(ticker)
        if data:
            return json.dumps(data['financials'])
        return "Metrics not found."
"""

# ==========================================
# 2. AGENTS (The "Brains")
# ==========================================
agents_code = """
import time

class Agent:
    def __init__(self, name, role, tools):
        self.name = name
        self.role = role
        self.tools = tools

    def think(self, prompt):
        # In a real app, this calls OpenAI/Anthropic API.
        # Here, we simulate the "Reasoning Trace" for the demo.
        print(f"\\n🤖 [{self.name} ({self.role})]: Thinking...")
        time.sleep(1) # Simulate latency
        return self.execute(prompt)

    def execute(self, prompt):
        raise NotImplementedError

class ResearcherAgent(Agent):
    def execute(self, ticker):
        print(f"   👉 Tools: Fetching News & Price for {ticker}...")
        price = self.tools.get_stock_price(ticker)
        news = self.tools.get_recent_news(ticker)
        return {
            "ticker": ticker,
            "raw_data": f"{price}\\nNews: {news}"
        }

class QuantAgent(Agent):
    def execute(self, research_data):
        print(f"   👉 Analysis: Calculating risk based on P/E and volatility...")
        raw = research_data["raw_data"]
        # Simple heuristic logic to mimic AI reasoning
        risk_level = "HIGH" if "95.2" in raw else "MODERATE"
        metrics = self.tools.get_financial_metrics(research_data['ticker'])
        
        return {
            "risk_assessment": risk_level,
            "quantitative_analysis": f"Valuation is {risk_level}. Key metrics: {metrics}"
        }

class WriterAgent(Agent):
    def execute(self, research, quant):
        print(f"   👉 Synthesis: Drafting Investment Memo...")
        # Simulating LLM generation
        report = f\"\"\"
        === INVESTMENT MEMO: {research['ticker']} ===
        DATE: {time.strftime("%Y-%m-%d")}
        
        1. MARKET SNAPSHOT
        {research['raw_data']}
        
        2. QUANTITATIVE ANALYSIS
        {quant['quantitative_analysis']}
        
        3. RECOMMENDATION
        Based on the {quant['risk_assessment']} risk profile and current news cycle,
        we recommend a HOLD strategy. The technology is promising, but valuation
        remains a key concern.
        \"\"\"
        return report
"""

# ==========================================
# 3. ORCHESTRATOR (The "Swarm Manager")
# ==========================================
main_code = """
from tools import FinancialTools
from agents import ResearcherAgent, QuantAgent, WriterAgent

def run_financial_swarm(ticker):
    print(f"🚀 STARTING FINANCIAL ANALYST SWARM FOR: {ticker}")
    print("==================================================")
    
    # 1. Initialize Tools
    tools = FinancialTools()

    # 2. Initialize Agents
    researcher = ResearcherAgent("Alice", "Senior Researcher", tools)
    quant = QuantAgent("Bob", "Quantitative Analyst", tools)
    writer = WriterAgent("Charlie", "Portfolio Manager", None)

    # 3. Step 1: Research
    research_output = researcher.think(ticker)
    
    # 4. Step 2: Risk Analysis (Quant)
    quant_output = quant.think(research_output)

    # 5. Step 3: Final Report (Writer)
    final_report = writer.think((research_output, quant_output))

    print("\\n✅ FINAL OUTPUT GENERATED:")
    print(final_report)

if __name__ == "__main__":
    # You can change this to 'TSLA' or 'NVDA' to test different data paths
    run_financial_swarm("NVDA")
"""

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content.strip())
    print(f"✅ Injected Code: {path}")

write_file(os.path.join(base_dir, "tools.py"), tools_code)
write_file(os.path.join(base_dir, "agents.py"), agents_code)
write_file(os.path.join(base_dir, "main.py"), main_code)