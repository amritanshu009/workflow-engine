import random

def generate_synthetic_data(n_rows: int = 50):
    data = []
    for _ in range(n_rows):
        age = random.randint(-5, 90)
        income = float(f"{random.uniform(1000, 200000):.2f}")
        score = float(f"{random.uniform(-10, 150):.2f}")
        row = {"age": age, "income": income, "score": score}
        data.append(row)
    return data

