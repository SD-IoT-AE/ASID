"""
ASID Distributed Multi-Controller Mitigation Core (DMCM)
-------------------------------------------------------
Central coordination service that receives alerts from CAAWE detection module,
dispatches mitigation commands to RYU, ONOS, and OpenDaylight adapters,
and records global actions.
"""

from flask import Flask, request, jsonify
import requests, json, time, threading, os
from coordination_bus import CoordinationBus
from policy_engine import PolicyEngine

app = Flask(__name__)
bus = CoordinationBus()
policy = PolicyEngine()

LOG_FILE = "mitigation/logs/mitigation_log.json"

@app.route("/api/mitigation", methods=["POST"])
def receive_alert():
    data = request.get_json()
    flow_src = data.get("flow_src")
    flow_dst = data.get("flow_dst")
    timestamp = data.get("timestamp", time.time())

    decision = policy.evaluate(flow_src, flow_dst)
    if decision == "ALLOW":
        print(f"[DMCM] Flow {flow_src}->{flow_dst} allowed by policy.")
        return jsonify({"status": "allowed"}), 200

    # Otherwise, broadcast mitigation
    print(f"[DMCM] Mitigating flow {flow_src}->{flow_dst} across controllers...")
    bus.broadcast_mitigation(flow_src, flow_dst)

    # log event
    entry = {
        "flow_src": flow_src,
        "flow_dst": flow_dst,
        "timestamp": timestamp,
        "action": "MITIGATE"
    }
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return jsonify({"status": "mitigated", "flow": entry}), 200

def run_dmcm():
    app.run(host="0.0.0.0", port=5005)

if __name__ == "__main__":
    print("[DMCM] Distributed Mitigation Controller running on port 5005...")
    run_dmcm()
