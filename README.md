# 🔍 Research Agent

A simple yet powerful AI research assistant that autonomously searches the web and synthesizes information to answer your questions. Built to demonstrate core AI agent concepts using OpenAI's GPT models and function calling.

## 🎯 What It Does

The Research Agent uses a **ReAct (Reasoning + Acting)** pattern to:
- Break down complex questions into searchable queries
- Autonomously perform web searches using available tools
- Analyze and synthesize information from multiple sources
- Provide well-sourced, comprehensive answers

## 🏗️ Architecture

```
User Question
     ↓
┌────────────────────────────────┐
│   Agent Reasoning Loop         │
│                                │
│  1. Think: "What do I need?"   │
│  2. Act: Call web_search tool  │
│  3. Observe: Read results      │
│  4. Repeat until sufficient    │
│  5. Answer: Synthesize info    │
└────────────────────────────────┘
     ↓
Final Answer with Sources
```

### Key Components

- **Agent Core** (`src/agent.py`): Implements the reasoning loop using OpenAI's chat completion API with function calling
- **Tool System** (`src/tools.py`): Extensible tool registry with web search capabilities
- **CLI Interface** (`src/main.py`): Interactive command-line interface for user interaction

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/research-agent.git
   cd research-agent
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

### Usage

Run the agent:
```bash
python run.py
```

Example interaction:
```
🤖 Research Agent
============================================================
Ask me anything and I'll research it for you!
Type 'quit' or 'exit' to stop.

💭 Your question: What are the latest developments in quantum computing?

--- Iteration 1 ---
🛠️  Agent is using 1 tool(s)...
   → web_search({'query': 'latest quantum computing developments 2025'})
   ✓ Got 1247 characters of results

--- Iteration 2 ---
✅ Agent has formulated final answer

============================================================
📝 Answer:
============================================================
Based on recent developments, quantum computing has seen several
breakthroughs in 2025...
[Sources cited from search results]
============================================================
```

## 🧠 How It Works

### The ReAct Pattern

The agent follows a continuous loop:

1. **Reasoning**: GPT analyzes the question and current context
2. **Action**: If more information is needed, GPT calls the web_search tool
3. **Observation**: Search results are added to the conversation context
4. **Iteration**: Steps 1-3 repeat until GPT has enough information
5. **Response**: GPT synthesizes findings into a final answer

### Function Calling

The agent uses OpenAI's function calling feature:

```python
# 1. Define tool schema (OpenAI's standard format)
{
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Search the web for information",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"]
        }
    }
}

# 2. GPT decides to call it
# 3. We execute it: tool_registry.execute("web_search", query="...")
# 4. Results go back to GPT
# 5. GPT uses results to formulate answer
```

## 🔧 Configuration

Edit `.env` to customize behavior:

```bash
# Model selection (gpt-4o-mini is fast and cheap for learning)
MODEL_NAME=gpt-4o-mini

# Maximum reasoning iterations before forcing an answer
MAX_ITERATIONS=5
```

## 📁 Project Structure

```
research-agent/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── agent.py             # Core agent logic and reasoning loop
│   ├── tools.py             # Tool definitions and registry
│   └── main.py              # CLI interface
├── tests/
│   └── test_example.py      # Example tests
├── run.py                   # Entry point script
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🎓 Learning Resources

This project demonstrates several key AI agent concepts:

- **Agentic AI**: Systems that can autonomously plan and execute actions
- **ReAct Pattern**: Reasoning and Acting in a loop
- **Function Calling**: Letting LLMs use external tools
- **Tool Abstraction**: Creating reusable, composable capabilities

### Extension Ideas

Want to learn more? Try adding:

1. **New Tools**: Calculator, weather API, file operations
2. **Memory System**: Persist findings across sessions
3. **Multi-step Planning**: Break complex queries into sub-questions
4. **Streaming Responses**: Show agent thinking in real-time
5. **Web Scraping**: Fetch and parse full articles, not just snippets

## 🛠️ Development

### Adding a New Tool

1. Create a tool class in `src/tools.py`:
   ```python
   class CalculatorTool(Tool):
       def __init__(self):
           super().__init__(
               name="calculator",
               description="Perform mathematical calculations"
           )

       def execute(self, expression: str) -> str:
           # Implementation here
           pass

       def to_function_schema(self) -> Dict[str, Any]:
           # Return OpenAI function schema
           pass
   ```

2. Register it in `create_default_registry()`:
   ```python
   def create_default_registry() -> ToolRegistry:
       registry = ToolRegistry()
       registry.register(WebSearchTool())
       registry.register(CalculatorTool())  # Add here
       return registry
   ```

3. The agent will automatically learn to use it!

### Running Tests

```bash
python -m pytest tests/
```

## 📝 License

MIT License - feel free to use this project for learning and portfolio purposes.

## 🙏 Acknowledgments

- Built with [OpenAI's GPT models](https://openai.com/)
- Uses [DuckDuckGo](https://duckduckgo.com/) for web search
- Inspired by the ReAct paper: [Yao et al., 2023](https://arxiv.org/abs/2210.03629)

## 📧 Contact

Built by [Your Name] - [Your GitHub Profile]

Questions? Open an issue or reach out!

---

⭐ If you found this helpful for learning about AI agents, please star the repo!
