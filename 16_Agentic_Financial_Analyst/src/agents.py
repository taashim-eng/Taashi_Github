import time

class Agent:
    def __init__(self, name, role, tools):
        self.name = name
        self.role = role
        self.tools = tools

    def think(self, prompt):
        # In a real app, this calls OpenAI/Anthropic API.
        # Here, we simulate the "Reasoning Trace" for the demo.
        print(f"\n🤖 [{self.name} ({self.role})]: Thinking...")
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
            "raw_data": f"{price}\nNews: {news}"
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
        report = f"""
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
        """
        return report