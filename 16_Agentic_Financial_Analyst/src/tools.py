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