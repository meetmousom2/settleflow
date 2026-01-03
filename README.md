# ✈️ SettleFlow: Autonomous Claims Adjustment

**SettleFlow** is an agentic AI system designed to automate the lifecycle of travel insurance claims. Built with **LangGraph**, it uses a multi-agent "debate" architecture to ensure insurance decisions are fair, auditable, and strictly aligned with policy text.

## 🛠 Tech Stack
- **Orchestration:** [LangGraph](https://github.com/langchain-ai/langgraph) (Stateful Multi-Agent Workflows)
- **Environment & Pkg Manager:** [uv](https://github.com/astral-sh/uv) (Extremely fast Python tooling)
- **Validation:** [Pydantic v2](https://docs.pydantic.dev/) (Strict type safety for claim states)
- **Linting/Typing:** Ruff & Basedpyright
- **LLM Gateway:** LiteLLM (Supporting Gemini, DeepSeek, and local Ollama)

## 🧠 The Agentic Graph
SettleFlow operates as a state machine where a claim passes through three distinct specialized nodes:
1. **The Advocate:** Scans evidence (boarding passes, receipts) to find every possible reason to support the user's claim.
2. **The Auditor:** Acts as the "devil's advocate," identifying policy exclusions or missing documentation.
3. **The Judge:** Weighs the evidence from both agents to produce a final `ClaimDecision` (Approved/Rejected) with an exact dollar amount.

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed on your Mac.

### Installation
```bash
# Clone the repository
git clone https://github.com/meetmousom2/settleflow.git
cd settleflow

# Install dependencies and setup venv
uv sync

# Install pre-commit hooks
uv run pre-commit install
```

### Environment Setup
Create a `.env` file in the root directory:
```bash
GOOGLE_API_KEY=your_gemini_key_here
# Optional: For local testing with Ollama
# LITELLM_LOCAL_MODEL=ollama/deepseek-v3
```

## 🧪 Development
We enforce strict code quality using Ruff and Basedpyright.
```bash
# Format and Lint
uv run ruff format .
uv run ruff check --fix .

# Type Check
uv run basedpyright
```

## 📜 License
MIT
