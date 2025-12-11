from app.workflow.nodes import (
    profile_data,
    identify_anomalies,
    generate_rules,
    apply_rules,
    check_loop_condition
)

from app.data.synthetic_data import generate_synthetic_data
from app.engine.graph import WorkflowGraph

def create_data_quality_workflow():
    data = generate_synthetic_data()

    state = {"data": data}

    nodes = {
        "profile": profile_data,
        "find_anomalies": identify_anomalies,
        "make_rules": generate_rules,
        "apply_rules": apply_rules,
        "check_loop": check_loop_condition
    }

    edges = {
        "profile": "find_anomalies",
        "find_anomalies": "make_rules",
        "make_rules": "apply_rules",
        "apply_rules": "check_loop",
        "check_loop": "find_anomalies"
    }

    graph = WorkflowGraph(nodes, edges, loop_node="check_loop")
    return graph, state
