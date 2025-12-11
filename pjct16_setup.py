import os
import json
import random
import datetime

def setup_agentic_project():
    # 1. Define Paths
    base_dir = "/workspaces/Taashi_Github/16_Agentic_Financial_Analyst"
    data_dir = os.path.join(base_dir, "data")
    src_dir = os.path.join(base_dir, "src")
    
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(src_dir, exist_ok=True)
    print(f"✅ Directories Created: {base_dir}")

    # 2. Generate "Mock" Financial Data (The Knowledge Base)
    # This simulates what a tool like a Vector DB or API would return
    market_data = {
        "TSLA": {
            "price": 245.30,
            "pe_ratio": 70.5,
            "news": [
                "Tesla announces expansion of Gigafactory in Mexico.",
                "Analysts worry about EV demand softening in Q4.",
                "New battery technology promises 20% more range."
            ],
            "financials": {"revenue_growth": "15%", "operating_margin": "10%"}
        },
        "NVDA": {
            "price": 890.00,
            "pe_ratio": 95.2,
            "news": [
                "Nvidia reveals new Blackwell AI chip.",
                "Tech giants increase capex spend on AI infrastructure.",
                "Export restrictions to China may impact future revenue."
            ],
            "financials": {"revenue_growth": "260%", "operating_margin": "55%"}
        }
    }

    data_path = os.path.join(data_dir, "market_knowledge.json")
    with open(data_path, "w") as f:
        json.dump(market_data, f, indent=4)
    
    print(f"✅ Mock Market Data Generated: {data_path}")

if __name__ == "__main__":
    setup_agentic_project()