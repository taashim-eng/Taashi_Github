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

    print("\n✅ FINAL OUTPUT GENERATED:")
    print(final_report)

if __name__ == "__main__":
    # You can change this to 'TSLA' or 'NVDA' to test different data paths
    run_financial_swarm("NVDA")