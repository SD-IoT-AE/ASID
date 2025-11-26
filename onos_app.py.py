"""
ONOS Integration App for ASID Framework
Communicates with ONOS REST API to push flow rules for mitigation.
"""
import requests, json, time
from flask import Flask, request, jsonify

ONOS_REST = "http://127.0.0.1:8181/onos/v1/flows"
AUTH = ('onos', 'rocks')
app = Flask(__name__)

@app.route("/api/mitigation", methods=["POST"])
def onos_mitigation():
    payload = request.get_json()
    device = payload.get("switch", "of:0000000000000001")
    src = payload.get("flow_src")
    dst = payload.get("flow_dst")

    flow_rule = {
        "flows": [{
            "priority": 40000,
            "timeout": 30,
            "isPermanent": False,
            "deviceId": device,
            "treatment": {"instructions": [{"type": "DROP"}]},
            "selector": {
                "criteria": [
                    {"type": "ETH_SRC", "mac": src},
                    {"type": "ETH_DST", "mac": dst}
                ]
            }
        }]
    }

    resp = requests.post(ONOS_REST, auth=AUTH, headers={"Content-Type": "application/json"}, data=json.dumps(flow_rule))
    print(f"[ONOS] Mitigation response {resp.status_code}")
    return jsonify({"status": "mitigation pushed", "onos_status": resp.status_code})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006)
