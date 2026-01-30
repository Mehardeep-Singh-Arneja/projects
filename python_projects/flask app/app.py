from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    marks_text = data.get("marks_text", "")
    total_marks = data.get("total_marks")

    if not marks_text or not total_marks:
        return jsonify({"error": "Missing input"}), 400

    try:
        total_marks = float(total_marks)
    except ValueError:
        return jsonify({"error": "Invalid total marks"}), 400

    marks = []
    for line in marks_text.splitlines():
        try:
            marks.append(float(line.strip()))
        except ValueError:
            continue

    if not marks:
        return jsonify({"error": "No valid marks found"}), 400

    df = pd.DataFrame({"marks": marks})
    df["percent"] = (df["marks"] / total_marks) * 100

    result = {
        "total_students": int(len(df)),
        "highest_marks": float(df["marks"].max()),
        "lowest_marks": float(df["marks"].min()),
        "avg_marks": round(float(df["marks"].mean()), 2),
        "full_marks": int((df["percent"] == 100).sum()),

        "above_95": int((df["percent"] >= 95).sum()),
        "between_90_95": int(((df["percent"] >= 90) & (df["percent"] < 95)).sum()),
        "between_80_90": int(((df["percent"] >= 80) & (df["percent"] < 90)).sum()),
        "between_70_80": int(((df["percent"] >= 70) & (df["percent"] < 80)).sum()),
        "between_60_70": int(((df["percent"] >= 60) & (df["percent"] < 70)).sum()),
        "below_60": int((df["percent"] < 60).sum())
    }

    return jsonify(result)

app.run(debug=True)
