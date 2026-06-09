from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "API çalışıyor"

@app.route("/api")
def api():
    return jsonify({"status": "ok"})
