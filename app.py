from flask import Flask, request, jsonify
import json
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)

# CORS: permite que tu GitHub Pages lo consuma
CORS(app)

STATE_FILE = "state.json"

def load_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"color": "#7682CF", "count": 3, "updated": ""}

def save_state(state):
    state["updated"] = datetime.now().isoformat(timespec="seconds")
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

@app.route("/api/state", methods=["GET"])
def api_state():
    return jsonify(load_state())

@app.route("/api/set", methods=["POST"])
def api_set():
    data = request.get_json(force=True)
    color = data.get("color", "#7682CF")
    count = int(data.get("count", 0))

    if count < 0: count = 0
    if count > 1000: count = 1000

    state = load_state()
    state["color"] = color
    state["count"] = count
    save_state(state)

    return jsonify({"ok": True, "state": state})

@app.route("/")
def root():
    return "OK Flask Render. Usa /api/state y /api/set"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render usa PORT
    app.run(host="0.0.0.0", port=port)