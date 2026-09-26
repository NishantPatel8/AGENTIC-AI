# AGENTIC-AI

A comprehensive repository for **Agentic AI & Multi-Agent Systems**, featuring end-to-end implementations of LLM-based autonomous agents, ReAct loops, Model Context Protocol (MCP) servers, LangChain/LangGraph workflows, multi-agent collaboration architectures, and interactive assistant systems.

---

## 📁 Repository Structure

```
AGENTIC-AI/
├── .vscode/                     # Workspace configurations (analysis extraPaths)
├── Assessment/                  # Production assessments & case studies
│   ├── Session A/               # Fine-tuning, complaint classifier, agent loop, MCP DB guard
│   ├── Session B/               # AI decision engine, memory strategies, order lifecycle
│   ├── Session C/               # Interactive food delivery assistant
│   └── Session D/               # ReAct customer support agent & bug fixes
│
└── Assignment/                  # Hands-on progressive assignments
    ├── Session 13/              # Advanced Agentic Concepts (Part 2)
    ├── Session 14/              # Introduction to Model Context Protocol (MCP)
    ├── Session 15/              # LangChain + LangGraph + MCP Integration
    ├── Session 16/              # Business MCP Server (Flask)
    ├── Session 17/              # Database MCP Server (SQLite)
    ├── Session 18/              # Multi-Client Protocol File Server (Sockets & Threading)
    ├── Session 19/              # Multi-Agent Architectures & Communication Workflows
    ├── Session 20/              # Agentic AI with LLMs (Part 3) - Multi-Agent Systems
    ├── Session 24/              # Personal Assistant Agent (Part 1: Tool Implementations)
    └── Session 25/              # Personal Assistant Agent (Part 2: Intent Engine & Streamlit UI)
```

---

## 🚀 Key Highlights

### 1. Model Context Protocol (MCP) & Servers
- **Session 14 - 18**: Complete progression from MCP fundamentals, LangGraph state graph integrations, and HTTP/Flask business servers to SQLite database handlers and threaded multi-client file transfer servers.

### 2. Autonomous Agents & ReAct Decision Loops
- **Session A - D & Session 19 - 20**: Implementation of Thought-Action-Observation loops, hierarchical supervisor-worker architectures, voting/consensus mechanisms, and resilient error recovery without infinite cycling.

### 3. Personal Assistant Agent (Sessions 24 & 25)
- **Session 24**: Live tool integrations including Open-Meteo weather API, safe recursive descent mathematical parser (no `eval`), CSV expense analytics, GNews headlines, and motivational quotes.
- **Session 25**: Full intent classification engine (`detect_intent`), dynamic tool routing (`select_tool`), rolling conversation memory, and an interactive Streamlit chat interface (`assistant_ui.py`).

---

## 🛠️ Getting Started

### Prerequisites
- Python 3.10+ (tested on Python 3.11 / 3.13)
- Git

### Installation
Clone the repository:
```bash
git clone https://github.com/NishantPatel8/AGENTIC-AI.git
cd AGENTIC-AI
```

Install common dependencies (or refer to individual session `requirements.txt`):
```bash
pip install streamlit requests pydantic langchain langgraph
```

### Running the Personal Assistant UI (Session 25)
```bash
cd "Assignment/Session 25"
streamlit run assistant_ui.py
```

### Running Tests
Unit tests are available in individual session directories. For example:
```bash
python "Assignment/Session 25/test_session25.py"
```

---

## 👤 Author
- **Nishant Patel** ([@NishantPatel8](https://github.com/NishantPatel8))
