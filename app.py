from flask import Flask, render_template, request, jsonify
from datetime import date
import os, json
from pathlib import Path

app = Flask(__name__)
DATA_FILE = Path(os.environ.get("DATA_FILE", "selections.json"))

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/choose")
def choose():
    payload = request.get_json(silent=True) or {}
    chosen = payload.get("date", "")
    try:
        selected = date.fromisoformat(chosen)
    except (TypeError, ValueError):
        return jsonify(ok=False, message="Выбери дату из календаря 💜"), 400

    # This page is configured for November 20–30, 2026.
    if selected.year != 2026 or selected.month != 11 or not 20 <= selected.day <= 30:
        return jsonify(ok=False, message="Можно выбрать дату с 20 по 30 ноября."), 400

    record = {"date": chosen}
    try:
        existing = json.loads(DATA_FILE.read_text(encoding="utf-8")) if DATA_FILE.exists() else []
        if not isinstance(existing, list):
            existing = []
        existing.append(record)
        DATA_FILE.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        app.logger.exception("Could not save date selection")

    return jsonify(ok=True, message=f"Ура! Тогда наше свидание — {selected.day} ноября 💜")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)