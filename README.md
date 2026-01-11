# dbGPT 📈

An LLM-powered, database-aware assistant. dbGPT orchestrates a large language model (via Groq) with a simple database layer to answer user questions, generate insights, and produce helpful responses grounded in your data. The project is organized into small, focused modules for configuration, DB access, LLM interactions, orchestration, and response shaping.

---

## ✨ Features
- 🤖 LLM integration via Groq client wrapper
- 🗄️ Simple database access layer (extensible for your DB)
- 🎛️ Orchestration agent coordinating model calls and data lookups
- 📝 Response agent to format and refine model outputs for end users
- 🧩 Minimal, composable Python modules ready for extension

---

## 📁 Repository Structure
- `config.py` — Centralized configuration helpers (e.g., env vars, constants)
- `db.py` — Database access utilities (connect/query helpers)
- `groq_client.py` — Groq LLM client wrapper and helpers
- `orchestration_agent.py` — High-level coordinator between the LLM and DB
- `user_response_agent.py` — Post-processing and user-facing response builder
- `main.py` — Entrypoint to run the assistant/app
- `requirements.txt` — Python dependencies for this project

---

## ⚙️ Requirements
- Python 3.10+ (recommended 3.11+)
- macOS, Linux, or Windows (instructions below use macOS/Linux style)
- A Groq API key (if using Groq Cloud)

---

## 🚀 Quickstart

1) Clone and enter the project directory:
```bash
git clone <your-fork-or-repo-url>
cd dbGPT
```

2) Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
On Windows PowerShell:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3) Install dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4) Set environment variables (recommended) or update `config.py` defaults:
```bash
# Required for LLM calls via Groq
export GROQ_API_KEY="your_groq_api_key"

# Optional: point to your database (examples)
# export DATABASE_URL="sqlite:///./local.db"
# export DATABASE_URL="postgresql+psycopg2://user:pass@host:5432/dbname"
```
To persist these, add them to your shell profile or a `.env` file and load them in `config.py`.

5) Run the app:
```bash
python main.py
```

---

## 🛠️ Configuration
Configuration typically flows through `config.py` and environment variables so you can switch environments without code changes.

Common environment variables:
- `GROQ_API_KEY`: Your Groq Cloud API key.
- `DATABASE_URL` (optional): SQLAlchemy-style DB URL (e.g., SQLite, Postgres). If omitted, `db.py` may default to a local SQLite file or an in-memory DB, depending on your implementation.
- Any additional flags your agents or `main.py` read (e.g., model name, temperature, max tokens). If these exist, expose them in `config.py` and document defaults.

Tips:
- Keep secrets out of source control; use env vars or a local `.env` ignored by git.
- Validate required variables at startup to fail fast.

---

## 🔗 How It Works
- `groq_client.py` encapsulates LLM calls (authentication, parameters, and request/response handling).
- `db.py` exposes a minimal interface for connecting and running queries.
- `orchestration_agent.py` decides when to query the DB, when to ask the LLM, and how to combine results.
- `user_response_agent.py` shapes the final answer: formatting, safety, and helpful context.
- `main.py` wires these pieces together into a simple CLI/app flow.

This separation keeps each concern focused and easier to test/extend.

---

## 💡 Usage Examples
Run the entrypoint and interact via the terminal:
```bash
python main.py
```
Example flow you might implement or already have:
- Input: "What were this week’s top 5 customers by revenue?"
- Orchestrator retrieves relevant data from the DB via `db.py` and sends context to the LLM via `groq_client.py`.
- Response agent formats a concise, readable answer with an optional table or bullet points.

---

## 👩‍💻 Development
- Use a virtual environment and pin dependencies in `requirements.txt`.
- Prefer small, focused functions for agents and clients.
- Add type hints and docstrings for clarity.
- If you add new configuration, centralize defaults and parsing in `config.py`.

Suggested optional tools:
```bash
pip install ruff black mypy
ruff check .
black .
mypy .
```

---

## ✅ Testing
If tests are added later:
```bash
pip install pytest
pytest -q
```
Keep tests close to the modules they cover for discoverability.

---

## 🐛 Troubleshooting
- "Module not found": Ensure the virtual environment is active and `pip install -r requirements.txt` ran successfully.
- "Unauthorized"/401 from LLM API: Check `GROQ_API_KEY` and that your key is valid.
- DB connection errors: Verify `DATABASE_URL` format and network reachability.
- macOS SSL issues: Upgrade `pip` and `certifi` or install system certificates.

---

## 🗺️ Roadmap Ideas
- Add streaming responses and tool/function calling
- Support additional databases and ORM integration
- Add caching layer for repeated queries
- Web or chat UI wrapper over the CLI

---
