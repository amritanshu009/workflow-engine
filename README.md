workflow-engine

A minimal workflow/graph engine built with FastAPI.
It supports nodes, branching, looping, and a simple tool registry — built for learning how workflow orchestration systems work internally.

🚀 Features

Node-based execution: Each node is a Python function that receives and modifies a shared state.

Graph structure: Define nodes, edges, a start node, branching logic, and optional loops.

Simple tool registry: Register Python functions as reusable “tools” for nodes.

FastAPI-powered API with Swagger docs at /docs.

📁 Project Structure
app/
│── main.py
│── engine/
│   └── graph.py
│── workflow/
│   ├── nodes.py
│   └── data_quality_workflow.py
└── data/
    └── synthetic_data.py

🛠 How It Works

You define a workflow graph using JSON.

Each node references a registered tool by name.

Tools modify the shared state dictionary.

The engine moves to the next node based on edges or conditional branching.

Optional looping continues until a state condition becomes true.

📦 Example: Create a Graph
{
  "nodes": {
    "extract": "detect_smells",
    "branch": "detect_smells",
    "done": "detect_smells"
  },
  "edges": {
    "extract": "branch",
    "branch": {
      "if": "issues > 2",
      "true": "done",
      "false": "done"
    },
    "done": null
  },
  "start": "extract",
  "loop_until": null
}

▶️ Example: Run the Graph
{
  "graph_id": "your-graph-id-here",
  "initial_state": {
    "code": "hello world"
  }
}


Response:

{
  "run_id": "...",
  "state": {
    "code": "hello world",
    "issues": 1
  },
  "log": [
    "→ running node 'extract' with tool 'detect_smells'",
    "→ running node 'branch' with tool 'detect_smells'",
    "branch: issues > 2 = False → done",
    "→ running node 'done' with tool 'detect_smells'"
  ],
  "done": true
}

🧪 API Endpoints
Method	Endpoint	Description
POST	/graph/create	Register a workflow graph
POST	/graph/run	Execute a graph with initial state
GET	/graph/state/{run_id}	Get final or in-progress workflow state

Swagger UI:

http://127.0.0.1:8000/docs

▶️ Run Locally
uvicorn app.main:app --reload

📜 License

MIT License
