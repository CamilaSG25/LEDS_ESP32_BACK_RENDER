from flask import Flask, request, jsonify
import json
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)

# CORS: permite que tu GitHub Pages lo consuma
CORS(app)

STATE_FILE = "state.json"

def default_state():
    return {
        "torreta1": "#000000",
        "torreta2": "#000000",
        "updated": ""
    }

def load_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)

        # Compatibilidad por si existe un state viejo
        if "torreta1" not in state:
            state["torreta1"] = "#000000"
        if "torreta2" not in state:
            state["torreta2"] = "#000000"
        if "updated" not in state:
            state["updated"] = ""

        return state
    except:
        return default_state()

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

    torreta1 = str(data.get("torreta1", "#000000")).upper()
    torreta2 = str(data.get("torreta2", "#000000")).upper()

    state = load_state()
    state["torreta1"] = torreta1
    state["torreta2"] = torreta2
    save_state(state)

    return jsonify({"ok": True, "state": state})

@app.route("/")
def root():
    return "OK Flask Render. Usa /api/state y /api/set"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render usa PORT
    app.run(host="0.0.0.0", port=port)