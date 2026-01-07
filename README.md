# LangChain Learning Tool

A hands-on learning project for exploring LangChain and LangGraph by building an AI agent with custom tools. This project demonstrates the integration of language models with specialized tools for mathematical and informational operations.


## Learning Objectives

This project helps you understand:
- **LangChain Fundamentals**: Core concepts of chains, agents, and tools
- **LangGraph Integration**: Building agents with stateful execution
- **Custom Tool Development**: Creating and integrating specialized tools
- **Agent Architecture**: ReAct (Reasoning and Acting) patterns
- **LLM Integration**: Working with Anthropic Claude models

## Features

- **Custom Tool Integration**: Implements specialized tools for mathematical operations
- **LangGraph Agent**: Uses LangGraph's `create_react_agent` for intelligent tool selection and execution
- **Multi-LLM Support**: Configured to work with Anthropic's Claude models
- **Extensible Architecture**: Easy to add new tools and capabilities

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd langchain-tool
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. Set up environment variables:
```bash
# Create a .env file with your API keys
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

## Usage

### Basic Usage

Run the main script to test the agent:

```bash
python main.py
```

The agent will process a sample query like:
```
"What is the population of Canada? Multiply it by 0.75"
```

### Example Queries

Try these different types of queries:

- Mathematical operations: `"add 10 and 20 and 30 then multiply the result by 2 then divide the result by 3"`
- Information retrieval: `"What is the population of Canada? Multiply it by 0.75"`
- Complex multi-step problems: `"Calculate the area of a circle with radius 5, then find 15% of that area"`

## Project Structure

```
├── main.py                 # Main entry point and demo
├── src/
│   ├── core/
│   │   ├── agent.py       # Agent implementation
│   │   ├── llm_client.py  # LLM client configuration
│   │   └── text_splitter.py
│   ├── tools/
│   │   └── tools.py       # Custom tool definitions
│   └── config/
├── pyproject.toml          # Project dependencies
├── .env                    # Environment variables (create this)
└── README.md              # This file
```

## Dependencies

Key dependencies include:
- `langchain>=0.3.0` - Core LangChain framework
- `langgraph>=0.1.0` - Agent orchestration
- `anthropic>=0.40.0` - Anthropic Claude integration
- `python-dotenv==1.0.0` - Environment variable management
- `wikipedia>=1.4.0` - Information retrieval tool

## Configuration

The agent uses the following configuration:

- **LLM**: Anthropic Claude models (configured via `ANTHROPIC_API_KEY`)
- **Agent Type**: ReAct (Reasoning and Acting) agent
- **Tools**: Custom mathematical and informational tools

## Development

### Learning Exercises

Try these challenges to deepen your understanding:

1. **Add a New Tool**: Create a tool for currency conversion or weather information
2. **Modify the Agent**: Change the system prompt to specialize in different domains
3. **Error Handling**: Add try-catch blocks for better error recovery
4. **Tool Chaining**: Create tools that depend on each other's outputs
5. **Memory Integration**: Add conversation memory to the agent

### Adding New Tools

1. Create new tool functions in `src/tools/tools.py`
2. Register them in the `CustomTool.get_tools()` method
3. The agent will automatically discover and use them

### Testing

Run the main script to test basic functionality:
```bash
python main.py
```

### Key Concepts to Explore

- **Agents vs Chains**: When to use each approach
- **Tool Selection**: How agents choose the right tool
- **State Management**: How LangGraph handles conversation state
- **Prompt Engineering**: Crafting effective system prompts
- **Tool Design**: Best practices for creating reusable tools

## License

This project is for educational purposes only. Feel free to use it for learning and experimentation.

## Contributing

This is a learning project - feel free to experiment, modify, and extend it as part of your LangChain learning journey!