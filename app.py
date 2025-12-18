from flask import Flask, render_template, jsonify, request
import json
from pathlib import Path

app = Flask(__name__)

DATA_DIR = Path(__file__).parent / "data"
PROJECTS_FILE = DATA_DIR / "projects.json"

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/api/projects")
def api_projects():
    if PROJECTS_FILE.exists():
        with open(PROJECTS_FILE, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    return jsonify([])

@app.post("/api/contact")
def api_contact():
    data = request.get_json(force=True)
    # Minimal server-side handling. In production, send email or store in DB.
    print("CONTACT MESSAGE:", data)  # Logged in console
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(debug=True)
