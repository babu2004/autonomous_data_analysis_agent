# Autonomous Data Analysis Agent

An agentic AI system that analyzes CSV datasets using **LLM reasoning, native tool calling, Python/Pandas tools, and FastAPI**.

The user provides a dataset and a natural-language analytical goal. The agent determines which tools are required, executes them, observes their results, and produces a final answer.

---

## Problem

Analyzing a dataset often requires manually inspecting its structure, selecting the appropriate analysis, writing code, and interpreting the results.

This project explores how an AI agent can automate that workflow.

Instead of following a fixed analysis pipeline, the agent uses an LLM to decide which available tools are necessary based on the user's goal and the results returned by previous tools.

---

## Solution

The Autonomous Data Analysis Agent accepts:

* A CSV dataset
* A natural-language analysis goal

The agent then:

1. Understands the user's goal.
2. Decides which tool should be used.
3. Executes the selected tool.
4. Observes the result.
5. Decides whether another tool is required.
6. Produces a final answer.

The application exposes this workflow through a simple web interface powered by FastAPI.

---

## Key Features

* LLM-driven agent decision making
* Native LLM tool calling
* CSV dataset inspection
* Descriptive statistics
* Group-based data analysis
* Multi-step agent execution
* Tool execution and observation tracking
* Controlled tool execution through a registry
* FastAPI backend
* Simple browser-based frontend
* Automated tests
* LLM provider abstraction

---

## Architecture



<img width="1536" height="1024" alt="ChatGPT Image Sep 27, 2026, 07_12_47 PM" src="https://github.com/user-attachments/assets/c4e2149b-211a-4941-a057-77ce1cdf02eb" />



---

## Agent Workflow

The agent follows a tool-driven execution loop.

```text
User Goal
   │
   ▼
LLM
   │
   ├── Tool Call ──► Python Tool
   │                    │
   │                    ▼
   │               Tool Result
   │                    │
   └──── Observation ◄──┘
            │
            ▼
           LLM
            │
       ┌────┴────┐
       │         │
   More Tools   Finish
       │         │
       ▼         ▼
    Continue   Final Answer
```

### Example

User:

> Analyze this sales dataset and tell me which region generated the highest revenue.

The agent can autonomously decide:

```text
Step 1
inspect_dataset
        ↓
Observation
        ↓
Step 2
group_analysis
        ↓
Observation
        ↓
Final Answer
```

The tool sequence is selected by the LLM based on the goal and previous observations rather than being hardcoded into a fixed workflow.

---

## Available Tools

### 1. `inspect_dataset`

Inspects the CSV dataset and returns:

* Number of rows
* Column names
* Data types
* Missing values

Example:

```text
Rows: 6

Columns:
date
region
product
quantity
price
revenue
```

---

### 2. `dataset_statistics`

Calculates descriptive statistics for numeric columns using Pandas.

Currently includes:

* Count
* Mean
* Standard deviation
* Minimum
* 25th percentile
* Median
* 75th percentile
* Maximum

---

### 3. `group_analysis`

Groups the dataset using a selected column and calculates the sum of a selected numeric metric.

Example:

```text
group_by = region
metric = revenue
```

Result:

```text
West    → 400000
South   → 250000
North   → 100000
East    → 90000
```

---

## Native Tool Calling

The project uses the LLM's **native tool-calling interface**.

Instead of asking the model to generate a custom JSON protocol such as:

```text
{
    "action": "tool",
    "tool": "group_analysis"
}
```

the model produces a native tool call.

The application then:

1. Receives the tool call.
2. Extracts the tool name and arguments.
3. Looks up the tool in the registry.
4. Executes the corresponding Python function.
5. Sends the tool result back to the LLM.
6. Allows the LLM to decide the next action.

This keeps the LLM responsible for decision making while Python remains responsible for actual tool execution.

---

## Controlled Tool Execution

The LLM does not directly execute arbitrary Python code.

Tool execution is controlled through a registry:

```text
LLM
 │
 ▼
Tool Name + Arguments
 │
 ▼
Tool Registry
 │
 ▼
Approved Python Function
 │
 ▼
Tool Result
```

This allows the application to control which operations the agent can perform.

---

## Agent State

The agent maintains execution state including:

* User goal
* Plan
* Current step
* Number of steps
* Tool calls
* Tool observations
* Errors
* Final answer
* Execution status

Example:

```text
Steps: 2
Tool calls: 2
Errors: 0
Status: completed
```

This state allows the agent to maintain context across multiple tool executions.

---

## Example Execution

### Input

```text
Dataset:
data/sample_sales.csv

Goal:
Analyze this sales dataset and tell me which region generated the highest revenue.
```

### Agent Execution

```text
[PLAN]
1. Inspect the dataset
2. Analyze the relevant data
3. Generate the final findings

[STEP 1]
→ inspect_dataset

[OBSERVATION]
6 rows
6 columns
0 missing values

[STEP 2]
→ group_analysis

Arguments:
group_by = region
metric = revenue

[OBSERVATION]

West    → 400000
South   → 250000
North   → 100000
East    → 90000
```

### Final Answer

```text
The West region generated the highest revenue,
totaling $400,000.
```

---

## Web Interface

The project includes a simple browser interface where users can:

1. Upload a CSV dataset.
2. Enter an analysis goal.
3. Start the analysis.
4. View the agent's tool execution.
5. View the observations.
6. View the final answer.

Example workflow:

```text
Upload CSV
    ↓
Enter Goal
    ↓
Analyze Dataset
    ↓
Agent Execution
    ↓
Tool Observations
    ↓
Final Answer
```

---

## Tech Stack

| Component          | Technology            |
| ------------------ | --------------------- |
| Language           | Python                |
| LLM                | Groq API              |
| LLM Model          | `openai/gpt-oss-20b`  |
| LLM Client         | OpenAI Python SDK     |
| Data Processing    | Pandas                |
| API                | FastAPI               |
| Server             | Uvicorn               |
| Validation / State | Pydantic              |
| Configuration      | python-dotenv         |
| Testing            | Pytest                |
| Frontend           | HTML, CSS, JavaScript |
| Package Management | uv                    |

---

## Project Structure

```text
autonomous_data_analysis_agent/
│
├── agent/
│   ├── agent.py
│   └── state.py
│
├── api/
│   └── main.py
│
├── data/
│   └── sample_sales.csv
│
├── llm/
│   ├── provider.py
│   └── grok_provider.py
│
├── tools/
│   ├── csv_tools.py
│   ├── definitions.py
│   ├── executor.py
│   └── registry.py
│
├── tests/
│   ├── test_state.py
│   ├── test_tools.py
│   └── test_llm.py
│
├── static/
│   └── index.html
│
├── main.py
├── pyproject.toml
└── README.md
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/babu2004/autonomous_data_analysis_agent.git

cd autonomous_data_analysis_agent
```

### 2. Install dependencies

The project uses `uv`.

```bash
uv sync
```

### 3. Configure the LLM API

Create a `.env` file:

```env
XAI_API_KEY=your_groq_api_key
```

> Note: The variable name is retained from the provider implementation. The application connects to the Groq-compatible OpenAI API endpoint.

### 4. Run tests

```bash
uv run pytest
```

### 5. Run the CLI agent

```bash
uv run python main.py
```

### 6. Run the web application

```bash
uv run uvicorn api.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/app
```

---

## API

### `GET /`

Health check endpoint.

### `GET /app`

Serves the web interface.

### `POST /analyze`

Accepts:

* CSV file
* Natural-language analysis goal

Returns:

* Execution status
* Agent steps
* Tool calls
* Tool observations
* Errors
* Final answer

Example response structure:

```json
{
  "status": "completed",
  "goal": "Which region generated the highest revenue?",
  "steps": 2,
  "tool_calls": [],
  "observations": [],
  "errors": [],
  "final_answer": "The West region generated the highest revenue."
}
```

---

## Testing

The project includes tests for:

* Agent state models
* Tool execution
* Tool registry
* Tool error handling
* LLM provider connectivity

Run:

```bash
uv run pytest
```

---

## Design Decisions

### Why native tool calling?

Native tool calling allows the LLM to communicate tool requests through the model/API's supported tool interface rather than relying on a custom JSON parsing protocol.

This also makes the agent less dependent on a particular textual response format.

### Why a custom agent loop?

The project uses a lightweight custom loop instead of introducing a large orchestration framework.

This keeps the system:

* Easy to inspect
* Easy to test
* Easy to modify
* Focused on the core agentic workflow

### Why not execute arbitrary LLM-generated Python?

The LLM selects from explicitly registered tools.

Python code execution remains under application control.

---

## Limitations

The current version intentionally focuses on a small, reliable set of analysis capabilities.

Current limitations include:

* CSV input only
* Limited analysis tools
* No persistent dataset storage
* No user authentication
* No multi-user session management
* No visualization generation
* No database integration
* Analysis is limited by the capabilities of the available tools and LLM

---

## Future Improvements

Possible future extensions include:

* Automatic visualization generation
* More statistical analysis tools
* Anomaly detection
* Correlation analysis
* Time-series analysis
* Support for Excel and other data formats
* Data cleaning tools
* Persistent analysis sessions
* Streaming agent execution
* More advanced planning strategies
* Deployment to a cloud platform

---

## Project Goal

This project demonstrates how an LLM can be combined with deterministic software tools to create an autonomous data analysis workflow.

The key idea is:

> **Let the LLM decide what should happen next, while deterministic tools perform the actual computation.**

This separates reasoning from execution and provides a simple foundation for building more capable agentic systems.

---

## Author

**Ganesh Babu**

M.Sc Data Science
AI / ML & Agentic AI Developer

---

## License

This project was created as an original submission for the AI Agentic System Challenge.
