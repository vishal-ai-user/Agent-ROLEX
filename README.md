# 🤖 ROLEX - AI Agent

**Rolex** is an interactive, tool-augmented AI Agent CLI powered by the **Groq API** and designed with a rich terminal interface using `rich`.

---

## ✨ Features

- **⚡ Fast Inference**: Built on top of Groq's high-speed LLM models.
- **🛠️ Agent Tools**:
  - **Live Web Search** (via `ddgs` DuckDuckGo search)
  - **File Operations** (Read, Write, List directory files)
  - **Terminal Execution** (Execute shell commands safely)
  - **Time & Memory Utilities** (Clear session memory, check system time)
- **🎨 Rich Terminal UI**: Interactive terminal interface displaying health status, live response styling, token usage counters, and panel views.
- **💬 Chat History & Memory**: Save session history or clear conversation context at any time.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.12+
- A [Groq API Key](https://console.groq.com/)

### 2. Installation

Clone the repository and navigate into the folder:
```bash
git clone https://github.com/vishal-ai-user/Agent-ROLEX.git
cd Agent-ROLEX
```

Install the dependencies:
```bash
pip install -r requirements.txt
```
*(Or if you use `uv`)*:
```bash
uv sync
```

### 3. Environment Setup

Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## 🏃 Usage

Run the agent script:
```bash
python Agent/agent.py
```

### 💡 Available Commands inside CLI
- `/clear` - Clear current conversation memory
- `/save` - Save current chat session to a markdown file
- `/exit` / `/quit` / `/bye` - Exit the agent CLI

---

## 📂 Project Structure

```text
.
├── Agent/
│   ├── agent.py       # Main AI Agent entry point & CLI logic
│   ├── memory.py      # Conversation state & prompt management
│   ├── tools.py       # Tool definitions (web search, files, shell execution)
│   └── chat_history/  # Saved session logs
├── .env.example       # Environment template
├── pyproject.toml     # Project dependencies & build config
├── requirements.txt   # Python package dependencies
└── README.md          # Project documentation
```

---

## 📜 License

Distributed under the MIT License.
