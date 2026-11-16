from flask import Flask, render_template, request, jsonify
from datetime import date
import json
import os
from pathlib import Path

app = Flask(__name__)
DATA_FILE = Path(os.environ.get("DATA_FILE", "selections.json"))
ALLOWED_PLANS = {"KFC", "Макдоналдс", "Закажем суши домой"}

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/choose")
def choose():
    payload = request.get_json(silent=True) or {}
    chosen = payload.get("date", "")
    plan = payload.get("plan", "")

    try:
        selected = date.fromisoformat(chosen)
    except (TypeError, ValueError):
        return jsonify(ok=False, message="Пожалуйста, выбери дату в календаре 💜"), 400

    if not (date(2026, 11, 26) <= selected <= date(2026, 12, 5)):
        return jsonify(ok=False, message="Дата должна быть с 26 ноября по 5 декабря 2026 года."), 400

    if plan not in ALLOWED_PLANS:
        return jsonify(ok=False, message="Выбери один из вариантов свидания 💜"), 400

    record = {"date": chosen, "plan": plan}
    try:
        existing = json.loads(DATA_FILE.read_text(encoding="utf-8")) if DATA_FILE.exists() else []
        if not isinstance(existing, list):
            existing = []
        existing.append(record)
        DATA_FILE.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        app.logger.exception("Could not save date and plan selection")

    return jsonify(ok=True, message="Твой выбор сохранён 💜")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
