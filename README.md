# copilot-demo

A collection of Python demo scripts showcasing the **GitHub Copilot SDK** (`copilot` package). The demos progress from a simple "Hello World" interaction to streaming responses, custom tools, MCP (Model Context Protocol) integration, and a fully featured cooking AI agent.

## Prerequisites

- Python 3.10+
- A [GitHub Personal Access Token (PAT)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) with access to GitHub Copilot / GitHub Models

## Repository Structure

```
copilot-demo/
├── main.py            # Basic Copilot session — send a prompt and print the response
├── session_sub.py     # Subscribe to session events and receive the assistant's reply
├── sub_all.py         # Subscribe to all session events (idle, message, etc.)
├── stream.py          # Streaming response — print reply tokens as they arrive
├── weathermain.py     # Custom tool demo — query weather for two cities (non-interactive)
├── weather_agent.py   # Interactive weather assistant with streaming and custom tools
├── mcptest.py         # MCP integration — attach a GitHub MCP server to a session
├── mcptest2.py        # MCP connection test — verify tool calls reach the MCP server
└── cooking-agent/     # Full cooking AI agent (see cooking-agent/README.md)
```

## Demo Scripts

### `main.py` — Basic Session

The simplest possible demo. Creates a Copilot session, sends a single prompt, and prints the response.

```bash
python main.py
```

### `session_sub.py` — Event Subscription

Demonstrates subscribing to session events with a lambda, then sending a prompt and printing the response.

```bash
python session_sub.py
```

### `sub_all.py` — Full Event Handling

Shows how to handle every session event type (`SESSION_IDLE`, `ASSISTANT_MESSAGE`, and others).

```bash
python sub_all.py
```

### `stream.py` — Streaming Responses

Enables streaming mode and writes response tokens to stdout as they arrive, so the reply appears incrementally.

```bash
python stream.py
```

### `weathermain.py` — Custom Tools (Non-interactive)

Registers a `get_weather` tool that returns randomised weather data for any city. Sends a single pre-set prompt asking about the weather in Seattle and Tokyo.

```bash
python weathermain.py
```

### `weather_agent.py` — Interactive Weather Assistant

An interactive chat loop that uses the same `get_weather` tool with streaming enabled. Type any weather question; enter `exit` to quit.

```bash
python weather_agent.py
```

### `mcptest.py` — MCP Server Integration

Creates a session with the GitHub MCP server attached (`https://api.githubcopilot.com/mcp/`) and subscribes to all session events to observe MCP tool calls in real time.

```bash
python mcptest.py
```

### `mcptest2.py` — MCP Connection Test

Sends a prompt that instructs the model to perform exactly one MCP tool call and checks whether the response or the observed events confirm the call succeeded. Prints `MCP connection test: PASS` or `FAIL`.

```bash
python mcptest2.py
```

## Sub-project: Cooking AI Agent

See [`cooking-agent/README.md`](cooking-agent/README.md) for full setup and usage instructions.

The cooking agent is a self-contained AI assistant that can:

- Search a built-in recipe database
- Extract structured ingredient lists
- Suggest ingredient substitutions
- Convert between cooking measurement units

It can run as an interactive CLI or as an HTTP server compatible with the AI Toolkit Agent Inspector.

```bash
cd cooking-agent
pip install -r requirements.txt
python app.py --cli
```
