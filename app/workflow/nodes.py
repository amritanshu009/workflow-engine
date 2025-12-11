from typing import Dict, List
import statistics

def profile_data(state: Dict):
    data = state["data"]
    summary = {}
    for col in data[0].keys():
        values = [row[col] for row in data if row[col] is not None]
        summary[col] = {
            "min": min(values),
            "max": max(values),
            "mean": statistics.mean(values)
        }
    state["profile"] = summary
    return state


def identify_anomalies(state: Dict):
    data = state["data"]
    anomalies = []
    for row in data:
        if row["age"] < 0:
            anomalies.append("age_negative")
        if row["score"] < 0:
            anomalies.append("score_negative")
        if row["income"] > 150000:
            anomalies.append("income_outlier")
    state["anomalies"] = anomalies
    return state


def generate_rules(state: Dict):
    rules = []
    for issue in state["anomalies"]:
        if issue == "age_negative":
            rules.append({"col": "age", "action": "set_zero"})
        elif issue == "score_negative":
            rules.append({"col": "score", "action": "set_zero"})
        elif issue == "income_outlier":
            rules.append({"col": "income", "action": "cap"})
    state["rules"] = rules
    return state


def apply_rules(state: Dict):
    rules = state["rules"]
    data = state["data"]
    for r in rules:
        col = r["col"]
        action = r["action"]
        for row in data:
            if action == "set_zero" and row[col] < 0:
                row[col] = 0
            elif action == "cap" and row[col] > 150000:
                row[col] = 150000
    state["data"] = data
    return state


def check_loop_condition(state: Dict):
    anomalies_left = len(state.get("anomalies", []))
    state["done"] = anomalies_left == 0
    return state
