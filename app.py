from flask import Flask, render_template, jsonify, request
import pandas as pd
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# ================================
# HOME
# ================================
@app.route("/")
def home():
    return render_template("home.html")


# ================================
# 1. INVISIBLE WASTE
# ================================
@app.route("/waste")
def invisible_waste():
    csv_path = os.path.join(DATA_DIR, "production_data.csv")
    df = pd.read_csv(csv_path)

    df["invisible_waste_liters"] = (
        df["input_liters"]
        - df["output_liters"]
        - df["recorded_waste_liters"]
    )

    df["invisible_waste_percent"] = (
        df["invisible_waste_liters"] / df["input_liters"]
    ) * 100

    df["high_invisible_waste"] = df["invisible_waste_percent"] > 3.0
    df["invisible_waste_cost_rs"] = df["invisible_waste_liters"] * 12

    # KPI
    total_waste = round(df["invisible_waste_liters"].sum(), 2)
    total_cost = round(df["invisible_waste_cost_rs"].sum(), 2)
    high_batches = int(df["high_invisible_waste"].sum())

    # ---- CHART DATA (THIS WAS MISSING) ----
    machine_summary = df.groupby("machine")["invisible_waste_liters"].mean()
    shift_summary = df.groupby("shift")["invisible_waste_liters"].mean()

    return render_template(
        "invisible_waste.html",
        table_data=df.to_dict(orient="records"),
        total_waste=total_waste,
        total_cost=total_cost,
        high_batches=high_batches,

        machine_labels=machine_summary.index.tolist(),
        machine_values=machine_summary.values.tolist(),

        shift_labels=shift_summary.index.tolist(),
        shift_values=shift_summary.values.tolist(),

        trend_labels=df["batch_id"].tolist(),
        trend_values=df["invisible_waste_liters"].tolist(),
    )

# ================================
# 2. MACHINE HEALTH
# ================================
@app.route("/machines")
def machine_health():
    json_path = os.path.join(DATA_DIR, "machine_health.json")

    with open(json_path) as f:
        data = json.load(f)

    rows = []
    for machine, info in data["machines"].items():
        for b in info["batches"]:
            rows.append({
                "machine": machine,
                "input": b["input_liters"],
                "output": b["output_liters"],
                "waste": b["waste_liters"],
                "energy": b["energy_kwh"]
            })

    df = pd.DataFrame(rows)
    results = []

    for m, d in df.groupby("machine"):
        total_input = d["input"].sum()
        total_output = d["output"].sum()
        total_waste = d["waste"].sum()
        total_energy = d["energy"].sum()

        waste_ratio = total_waste / total_input
        efficiency = total_output / (total_input + total_energy)

        faulty = waste_ratio > 0.08 or efficiency < 0.85

        results.append({
            "name": m,
            "total_input": total_input,
            "total_output": total_output,
            "total_waste": total_waste,
            "waste_ratio": round(waste_ratio, 3),
            "energy_kwh": total_energy,
            "efficiency": round(efficiency, 3),
            "faulty": faulty,
            "action": "REPAIR" if faulty else "NONE"
        })

    return render_template("machine_health.html", machines=results)


# ================================
# 3. WATER NETWORK + LEAK
# ================================
NETWORK_FILE = os.path.join(DATA_DIR, "network.json")

class Pipe:
    def __init__(self, f, t, flow, p):
        self.from_node = f
        self.to_node = t
        self.flow = flow
        self.normal_pressure = p
        self.current_pressure = p

    def detect_leak(self):
        return self.current_pressure < 0.7 * self.normal_pressure


@app.route("/network")
def network_ui():
    return render_template("water_network.html")


@app.route("/network/load")
def load_network():
    if not os.path.exists(NETWORK_FILE):
        return jsonify({"nodes": [], "pipes": []})
    with open(NETWORK_FILE) as f:
        return jsonify(json.load(f))


@app.route("/network/save", methods=["POST"])
def save_network():
    data = request.json

    for p in data["pipes"]:
        pipe = Pipe(
            p["from"],
            p["to"],
            p["flow"],
            p["normal_pressure"]
        )
        pipe.current_pressure = p["current_pressure"]
        p["leak"] = pipe.detect_leak()

    with open(NETWORK_FILE, "w") as f:
        json.dump(data, f, indent=2)

    return jsonify({"status": "saved"})


# ================================
# RUN
# ================================
if __name__ == "__main__":
    app.run(debug=True)