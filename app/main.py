from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Callable, Any, Optional, Union
import uuid

app = FastAPI()

# TOOL REGISTRY (like small helper functions that nodes can call)

TOOL_BOX: Dict[str, Callable] = {}

def register_tool(name: str):
    def wrap(fn):
        TOOL_BOX[name] = fn
        return fn
    return wrap

# example tool
@register_tool("detect_smells")
def detect_smells(state: dict):
    code = state.get("code", "")
    return {"issues": len(code) % 5}


# GRAPH + RUN STORAGE (in-memory)

GRAPHS = {}
RUNS = {}


# REQUEST MODELS

class GraphInput(BaseModel):
    nodes: Dict[str, str]
    edges: Dict[str, Union[str, dict]]
    start: str
    loop_until: Optional[str] = None


class RunInput(BaseModel):
    graph_id: str
    initial_state: dict


# CREATE A GRAPH

@app.post("/graph/create")
def create_graph(model: GraphInput):
    graph_id = str(uuid.uuid4())
    GRAPHS[graph_id] = model.dict()
    return {"graph_id": graph_id}


# INTERNAL GRAPH EXECUTION

def execute_node(node: str, graph: dict, state: dict, log: list):
    tool_name = graph["nodes"][node]
    tool_fn = TOOL_BOX.get(tool_name)

    if not tool_fn:
        raise RuntimeError(f"Tool '{tool_name}' is not registered.")

    log.append(f"→ running node '{node}' with tool '{tool_name}'")

    out = tool_fn(state)
    if out:
        state.update(out)

    log.append(f"state after {node}: {state}")
    return state


def run_graph(graph_id: str, initial_state: dict):
    graph = GRAPHS[graph_id]
    state = initial_state.copy()
    log = []
    node = graph["start"]
    steps = 0
    MAX_STEPS = 100

    while node and steps < MAX_STEPS:
        steps += 1
        state = execute_node(node, graph, state, log)

        loop_key = graph.get("loop_until")
        if loop_key:
            loop_value = state.get(loop_key, False)
            if not loop_value:
                log.append(f"loop: '{loop_key}' not true → repeat")
                continue
            else:
                log.append(f"loop: '{loop_key}' true → stop")

        edge = graph["edges"].get(node)
        if isinstance(edge, dict) and "if" in edge:
            condition = edge["if"]
            try:
                result = eval(condition, {}, state)
            except:
                result = False
            next_node = edge["true"] if result else edge["false"]
            log.append(f"branch: {condition} = {result} → {next_node}")
            node = next_node
            continue

        node = edge

    return state, log


# RUN GRAPH ENDPOINT

@app.post("/graph/run")
def run(model: RunInput):
    if model.graph_id not in GRAPHS:
        return {"error": "graph not found"}

    run_id = str(uuid.uuid4())
    RUNS[run_id] = {"state": {}, "log": [], "done": False}

    final_state, log = run_graph(model.graph_id, model.initial_state)

    RUNS[run_id] = {
        "state": final_state,
        "log": log,
        "done": True
    }

    return {
        "run_id": run_id,
        "state": final_state,
        "log": log,
        "done": True
    }


# GET STATE OF A RUN

@app.get("/graph/state/{run_id}")
def get_state(run_id: str):
    if run_id not in RUNS:
        return {"error": "run id not found"}
    return RUNS[run_id]

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)



