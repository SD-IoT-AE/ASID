"""
Local mitigation handler for RYU Controller.
Receives alerts from ASID DMCM and installs blocking rules.
"""
from flask import Flask, request, jsonify
from ryu.controller import ofp_event
import json, threading, requests

app = Flask(__name__)

@app.route("/api/mitigation", methods=["POST"])
def mitigation():
    data = request.get_json()
    print(f"[RYU Mitigation] Received: {data}")
    # Placeholder: integrate with actual RYU datapath commands or REST API
    return jsonify({"status": "rule installed", "flow": data}), 200

def run_server():
    app.run(host="0.0.0.0", port=5005)

if __name__ == "__main__":
    run_server()
