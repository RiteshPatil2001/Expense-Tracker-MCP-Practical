# 💰 Expense Tracker MCP Application

An AI-powered Expense Tracker built with **Python, Streamlit, LangChain, Groq, FastMCP, SQLite and the Model Context Protocol (MCP)**. Manage your expenses through plain conversation: the LangChain agent understands your request and calls the right MCP tool to get it done.

---

## 📖 About the Project

This project shows how to build an AI application on top of **MCP (Model Context Protocol)**. It has two parts:

- **Host:** the Streamlit chat UI, the LangChain agent, the Groq LLM and the MCP client.
- **Server:** a FastMCP server that exposes expense tools, business logic and SQLite database operations.

You don't need to start the MCP server yourself. When the Streamlit app starts, it **automatically launches the local MCP server over STDIO** and discovers its tools.

---

## ✨ Features

The app supports these operations:

1. Add a new expense
2. Edit an existing expense
3. List all expenses
4. Retrieve expenses within a date range
5. Generate category-wise expense summaries
6. Generate category-wise summaries within a date range
7. Delete an expense by its ID

### Additional Features

- Natural-language expense management with an AI agent
- Groq LLM integration
- MCP tools exposed through FastMCP
- Automatic local MCP server startup using STDIO
- SQLite database for persistent expense storage
- JSON-based expense category configuration
- Category validation to block unsupported categories
- Session-based conversation history
- Modular host and server architecture

---

## 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Primary programming language |
| **Streamlit** | Chat-based user interface |
| **LangChain** | AI agent creation and orchestration |
| **LangChain MCP Adapters** | Connects LangChain with MCP tools |
| **Groq** | LLM provider |
| **FastMCP** | MCP server and tool implementation |
| **SQLite** | Persistent expense storage |
| **JSON** | Allowed expense category configuration |
| **UV** | Python dependency and project management |

---

## 📂 Project Architecture

```text
expense-tracker-mcp/
│
├── .gitignore
├── README.md
│
├── host/
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── app.py
│   │
│   └── src/
│       └── expense_host/
│           ├── __init__.py
│           ├── agent.py
│           ├── chat_manager.py
│           ├── client.py
│           ├── llm.py
│           │
│           └── ui/
│               ├── __init__.py
│               ├── chat.py
│               └── components.py
│
└── server/
    ├── pyproject.toml
    ├── uv.lock
    ├── data/
    │   └── categories.json
    │
    └── src/
        └── expense_server/
            ├── __init__.py
            ├── main.py
            │
            ├── database/
            │   ├── __init__.py
            │   ├── connection.py
            │   ├── schema.py
            │   ├── queries.py
            │   └── category_config.py
            │
            ├── services/
            │   ├── __init__.py
            │   └── expense_service.py
            │
            └── tools/
                ├── __init__.py
                └── expense_tools.py
```

---

## ✅ Prerequisites

Install these before running the project.

### 1️⃣ Python

Install Python 3.12 or a version compatible with the project's `pyproject.toml` files. [Download Python](https://www.python.org/downloads/)

```powershell
python --version
```

### 2️⃣ UV

UV manages Python dependencies and virtual environments. Install it on Windows with PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify the installation (close and reopen the terminal first if the command isn't found):

```powershell
uv --version
```

📚 Docs: [UV Documentation](https://docs.astral.sh/uv/)

### 3️⃣ SQLite

No separate installation is needed. Python includes the `sqlite3` module in its standard library. To verify:

```powershell
python -c "import sqlite3; print(sqlite3.sqlite_version)"
```

### 4️⃣ Git

[Download Git](https://git-scm.com/downloads) to clone the repository.

---

## 🔑 Step 1: Get Your Groq API Key

You need one API key, and Groq has a free tier.

1. Go to the [Groq Console](https://console.groq.com/) and sign up or log in.
2. Open the [API Keys page](https://console.groq.com/keys).
3. Click **Create API Key**, give it a name, and click **Submit**.
4. **Copy the key immediately.** It is shown only once.

📚 Docs: [Groq Documentation](https://console.groq.com/docs)

---

## 📥 Step 2: Clone the Repository

Open PowerShell and go to the folder where you want to keep the project:

```powershell
cd "C:\Users\YourUsername\Desktop"
```

Clone the repository (replace `YOUR_GITHUB_REPOSITORY_URL` with your actual repo URL):

```powershell
git clone YOUR_GITHUB_REPOSITORY_URL
```

Go into the project folder:

```powershell
cd expense-tracker-mcp
```

---

## ⚙️ Step 3: Create the `.env` File

```powershell
Copy-Item .env
```

Open the new `.env` file and fill in your values:

```dotenv
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=your_groq_model_name

MCP_SERVER_DIR=server
DATABASE_PATH=server/data/expenses.db
CATEGORIES_FILE_PATH=server/data/categories.json
```

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Your Groq API key from Step 1 |
| `GROQ_MODEL` | The Groq model name the app should use. See the [Groq models list](https://console.groq.com/docs/models) |
| `MCP_SERVER_DIR` | Folder of the local MCP server |
| `DATABASE_PATH` | Where the SQLite database file is stored |
| `CATEGORIES_FILE_PATH` | Path to the JSON file with the allowed expense categories |

> ⚠️ **Keep `.env` private.** Never commit your real API key to GitHub. Make sure `.env` is listed in your `.gitignore`.

---

## 📦 Step 4: Install MCP Server Dependencies

From the repository root, run:

```powershell
uv sync --project server
```

This creates the server virtual environment and installs everything declared in `server/pyproject.toml`.

---

## 📦 Step 5: Install Host Dependencies

From the repository root, run:

```powershell
uv sync --project host
```

This creates the host virtual environment and installs everything declared in `host/pyproject.toml`, including Streamlit, LangChain, the LangChain Groq integration, and the LangChain MCP adapters.

> 💡 LangChain is already included in the host dependencies, so you don't need to install it separately.

---

## ▶️ Step 6: Run the Application

You **do not** need to start the MCP server manually or open a second terminal. The Streamlit host launches it automatically.

Go to the host folder:

```powershell
cd host
```

Start Streamlit:

```powershell
uv run streamlit run app.py
```

Streamlit will show a local URL, usually:

```text
http://localhost:8501
```

Open it in your browser and start chatting with your Expense Tracker.

---

## 💬 Example Queries

Try these in the chat interface.

| Action | Example prompt |
|--------|----------------|
| **Add an expense** | `I spent 500 on Food today.` |
| **Add with a date** | `Add an expense of 1200 for Shopping on 2026-11-20.` |
| **Edit an expense** | `Update expense ID 1 to 750.` |
| **List all expenses** | `Show me all my expenses.` |
| **Expenses by date range** | `Show my expenses between 2026-11-01 and 2026-11-23.` |
| **Category-wise summary** | `Give me a category-wise summary of my expenses.` |
| **Summary for a date range** | `Summarize my expenses by category between 2026-11-01 and 2026-11-23.` |
| **Delete an expense** | `Delete expense ID 2.` |

The agent may ask follow-up questions when something is missing, such as an expense ID or a date.

---

## 📚 Theory Notes: Understanding MCP

A separate theory-notes document is included in this repository. It covers:

- MCP (Model Context Protocol) fundamentals
- MCP architecture and its main components
- MCP client-server communication
- How MCP tools work
- How an AI application talks to an MCP server

Read it to understand the concepts behind the implementation, not just to run the app.

---

## 🧰 Troubleshooting

| Problem | Fix |
|---------|-----|
| `uv` is not recognized | Close and reopen PowerShell after installing UV, then run `uv --version` again |
| `Invalid API key` error | Re-check `GROQ_API_KEY` in `.env` and make sure there are no extra spaces |
| Model not found or not supported | Check `GROQ_MODEL` against the [Groq models list](https://console.groq.com/docs/models); models can be retired |
| `.env` not loading | Make sure the file is named exactly `.env` and sits in the project root, not inside `host/` or `server/` |
| Tools are not discovered or the server fails to start | Confirm you ran both `uv sync --project server` and `uv sync --project host`, and that `MCP_SERVER_DIR` is `server` |
| Port 8501 is already in use | Run `uv run streamlit run app.py --server.port 8502` |
| PowerShell blocks scripts | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then try again |

---

## 🤝 Contributing

Suggestions and improvements are welcome. Feel free to open an issue or submit a pull request.

## ⭐ Support

If this repo helped you, please give it a star on GitHub!

---

**Author:** [Ritesh Patil](https://github.com/RiteshPatil2001)

---

## 💾 Your Expense Records Are Persistent

**Even after starting a new session, clearing your chat, or restarting the application, your previously saved expense records are still available. All expense data is stored persistently in the local SQLite database.**
