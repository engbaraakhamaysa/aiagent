# AI Coding Agent

A Python-based AI coding agent that uses **LLM function calling** and an **agent loop** to inspect, modify, execute, and debug code autonomously.

The agent can interact with a local project through a controlled set of tools, allowing it to investigate problems, make code changes, run Python files, and verify its work.

---

## Overview

This project is a hands-on implementation of an AI coding agent.

Instead of simply generating an answer, the agent can interact with a real codebase:

```text
User Request
     ↓
    LLM
     ↓
  Tool Call
     ↓
Execute Tool
     ↓
 Tool Result
     ↓
    LLM
     ↓
  Tool Call
     ↓
     ...
     ↓
Final Response
```

The agent maintains the conversation history throughout the process, allowing the LLM to reason over previous actions and their results.

---

## Features

* LLM-powered coding agent
* Function/tool calling
* Multi-step agent loop
* Inspect files and directories
* Read file contents
* Create and modify files
* Execute Python files
* Autonomous bug fixing
* Run tests to verify changes
* Restricted working directory for file operations
* Maximum iteration limit to prevent infinite loops
* Verbose mode for debugging agent behavior

---

## Available Tools

The agent currently has four tools:

### `get_files_info`

Lists files and directories inside the allowed working directory.

It provides:

* File names
* File sizes
* Directory status

---

### `get_file_content`

Reads the contents of a file.

The tool also protects the working directory and limits the amount of content that can be read.

---

### `write_file`

Creates or modifies files inside the allowed working directory.

It can also create missing parent directories when necessary.

---

### `run_python_file`

Executes a Python file and returns:

* Standard output
* Standard error
* Process exit code

This allows the agent to test and verify its changes.

---

## Agent Loop

The core of the project is the agent loop.

The agent can perform up to **20 iterations**:

```python
for _ in range(20):
    # Send conversation to the LLM
    # Process tool calls
    # Execute tools
    # Add results to conversation
```

Each iteration follows the pattern:

```text
Think
 ↓
Act
 ↓
Observe
 ↓
Think Again
 ↓
Act
 ↓
Observe
 ↓
...
 ↓
Done
```

The loop stops when the LLM produces a final response without requesting additional tools.

A maximum iteration limit prevents the agent from running indefinitely.

---

## Conversation History

The `messages` list stores the complete conversation history.

The agent adds the assistant's response:

```python
message = response.choices[0].message
messages.append(message)
```

When a tool is executed, its result is also added:

```python
messages.append(result_message)
```

This allows the LLM to see:

1. What it previously requested.
2. What the tool returned.
3. What it should do next.

The conversation therefore becomes:

```text
User
 ↓
Assistant
 ↓
Tool
 ↓
Tool Result
 ↓
Assistant
 ↓
Tool
 ↓
Tool Result
 ↓
Assistant
 ↓
Final Response
```

---

## Autonomous Bug Fixing

One of the main demonstrations of the project is autonomous bug fixing.

A bug was intentionally introduced into the calculator application by changing the precedence of the `+` operator.

This caused:

```text
3 + 7 * 2
```

to incorrectly produce:

```text
20
```

instead of:

```text
17
```

The agent was then given:

```text
Fix the bug: 3 + 7 * 2 shouldn't be 20.
```

The agent independently:

1. Inspected the project.
2. Located the relevant calculator files.
3. Read the source code.
4. Identified the incorrect operator precedence.
5. Modified the source file.
6. Ran the Python application/tests.
7. Verified the corrected result.

The final result was:

```json
{
  "expression": "3 + 7 * 2",
  "result": 17
}
```

The calculator tests also passed successfully.

---

## Example Usage

### Ask the Agent to Explain Code

```bash
uv run main.py "Explain how the calculator renders the result to the console."
```

The agent can inspect the calculator source code and provide an explanation based on the actual files.

---

### Ask the Agent to Fix a Bug

```bash
uv run main.py "Fix the bug: 3 + 7 * 2 shouldn't be 20."
```

The agent can inspect the code, modify the necessary file, run tests, and verify the fix.

---

### Verbose Mode

Use `--verbose` to display additional information about the agent's execution:

```bash
uv run main.py --verbose "Explain how the calculator works."
```

Verbose mode can display tool calls and token usage, making it useful for debugging and understanding the agent's behavior.

---

## Project Structure

```text
aiagent/
│
├── calculator/
│   ├── main.py
│   ├── tests.py
│   ├── lorem.txt
│   └── pkg/
│       ├── calculator.py
│       └── render.py
│
├── functions/
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
│
├── main.py
├── prompts.py
├── call_function.py
├── test_get_files_info.py
├── test_get_file_content.py
├── test_write_file.py
├── test_run_python_file.py
│
├── .env
├── .gitignore
├── pyproject.toml
└── uv.lock
```

---

## Technologies

* **Python**
* **OpenAI Python SDK**
* **OpenRouter**
* **LLM Function Calling**
* **uv**
* **python-dotenv**
* **pytest / Python unittest**
* **Git & GitHub**

---

## Environment Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd aiagent
```

### 2. Install Dependencies

This project uses `uv` for Python dependency management.

```bash
uv sync
```

### 3. Configure Environment Variables

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_api_key
```

Never commit your API key to GitHub.

Make sure `.env` is included in `.gitignore`.

---

## Running the Agent

Run the agent with:

```bash
uv run main.py "Your task here"
```

Example:

```bash
uv run main.py "Explain how the calculator works."
```

---

## Running Tests

The project includes tests for the available tools.

Run the calculator tests with:

```bash
uv run calculator/tests.py
```

You can also run the individual tool tests:

```bash
uv run test_get_files_info.py
uv run test_get_file_content.py
uv run test_write_file.py
uv run test_run_python_file.py
```
