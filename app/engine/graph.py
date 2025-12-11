from typing import Dict, Callable, Union

class WorkflowGraph:
    def __init__(self, nodes: Dict[str, Callable], edges: Dict[str, Union[str, dict]], start: str, loop_until: str = None):
        self.nodes = nodes
        self.edges = edges
        self.start = start
        self.loop_until = loop_until

    def run(self, state: dict):
        log = []
        current = self.start
        steps = 0
        MAX_STEPS = 100

        while current and steps < MAX_STEPS:
            steps += 1

            node_fn = self.nodes[current]
            out = node_fn(state)

            if out:
                state.update(out)

            log.append(f"ran: {current}, state={state}")

            if self.loop_until:
                cond_value = state.get(self.loop_until, False)
                if not cond_value:
                    log.append(f"loop: {self.loop_until} not satisfied → repeat")
                    continue
                else:
                    log.append(f"loop: {self.loop_until} satisfied → exit loop")

            edge = self.edges.get(current)

            if isinstance(edge, dict) and "if" in edge:
                condition = edge["if"]
                try:
                    result = eval(condition, {}, state)
                except:
                    result = False
                next_node = edge["true"] if result else edge["false"]
                log.append(f"branch: {condition} = {result} → {next_node}")
                current = next_node
                continue

            current = edge

        return state, log
