# Project 16: The Wall Street Swarm (Multi-Agent System)

## 1. Problem Statement
**The Challenge:** High-value financial analysis requires synthesizing data from disparate sources (news, 10-K filings, real-time pricing). Human analysts spend 80% of their time gathering data and only 20% analyzing it.

**The Solution:** An **Agentic Workflow** where specialized AI agents (Researcher, Quant, Writer) collaborate autonomously. This "Swarm" architecture reduces report generation time from hours to seconds while maintaining consistency.

## 2. Value Proposition (Why this matters to FinTech)
* **Decoupled Reasoning:** By splitting "Research" (Retrieval) from "Analysis" (Reasoning), we reduce hallucinations common in single-prompt LLMs.
* **Tool Use (Function Calling):** Demonstrates how Agents interact with deterministic systems (Databases/APIs) to ground their answers in fact.
* **Auditability:** Every step of the reasoning chain (Research -> Quant -> Writer) is logged, a requirement for regulated financial industries.

## 3. Architecture Diagram
```mermaid
graph TD
    %% Definitions
    classDef user fill:#FFE6CC,stroke:#D79B00,stroke-width:2px;
    classDef agent fill:#DAE8FC,stroke:#6C8EBF,stroke-width:2px;
    classDef tool fill:#E1D5E7,stroke:#9673A6,stroke-width:2px;
    classDef artifact fill:#D5E8D4,stroke:#82B366,stroke-width:2px;

    User["Portfolio Manager<br/>(User)"]:::user

    subgraph The_Swarm ["The Agent Swarm"]
        Orchestrator["Workflow Orchestrator<br/>(Main Loop)"]:::agent
        
        Researcher["Agent A: Researcher<br/>(Fetch Context)"]:::agent
        Quant["Agent B: Quant<br/>(Risk Analysis)"]:::agent
        Writer["Agent C: VP Author<br/>(Synthesis)"]:::agent
    end

    subgraph Tools ["Deterministic Tools"]
        DB[("Market Knowledge Base<br/>(JSON/Vector DB)")]:::tool
        PriceAPI["Stock Price API"]:::tool
    end

    Report["Final Investment Memo<br/>(Markdown)"]:::artifact

    %% Flow
    User -->|"Analyze 'NVDA'"| Orchestrator
    Orchestrator -->|"1. Delegate"| Researcher
    
    Researcher -->|"Tool Call: Get News"| DB
    Researcher -->|"Tool Call: Get Price"| PriceAPI
    Researcher -->|"Raw Data"| Quant

    Quant -->|"2. Calculate Risk"| Writer
    Writer -->|"3. Draft Report"| Report

    linkStyle 0,1,2,3,4,5,6 stroke:#333,stroke-width:2px;
```

## 4. Design & Approach
* **Pattern:** Sequential Chain of Thought (CoT) handoffs.
* **State Management:** Data is passed as a structured dictionary context between agents.
* **Tools:** Custom Python classes mimic API endpoints (e.g., `get_stock_price`), designed to be easily swapped for real Bloomberg/AlphaVantage APIs in production.

## 5. How to Run the Demo
1. **Navigate to the Source Directory:**
```bash
cd src
```

2. **Run the Swarm:**
```bash
python main.py
```

3. **Expected Output:**
   * You will see the Researcher fetch live mock data.
   * The Quant will assess the P/E ratio and assign a risk level.
   * The Writer will output a formatted Investment Memo recommending a "HOLD" or "BUY" strategy.

---
**
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
I am currently considering these extensions:
- Connect to real APIs (Bloomberg, AlphaVantage)
- Add retry logic with `tenacity` library
- Implement caching for API calls
- Add more sophisticated risk models
- Build a REST API with FastAPI

---

Designed for High-Velocity FinTech Environments | Python 3.10+ | Zero External Dependencies**
