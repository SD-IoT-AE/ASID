"""
Handles inbound DMCM coordination and propagates mitigation commands to ODL RESTCONF.
"""
from flask import Flask, request, jsonify
import requests, json

app = Flask(__name__)
ODL_API = "http://127.0.0.1:8181/restconf/config/"
AUTH = ('admin', 'admin')

@app.route("/api/dmcm_notify", methods=["POST"])
def notify():
    data = request.get_json()
    src, dst = data["flow_src"], data["flow_dst"]
    payload = {"message": f"Mitigate flow {src}->{dst}"}
    print(f"[ODL Notify] {payload}")
    return jsonify({"status": "received"})
