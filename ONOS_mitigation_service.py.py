"""
ONOS Mitigation Service Handler
Receives DMCM signals and triggers ONOS REST push.
"""
import requests, json
from flask import Flask, request, jsonify

app = Flask(__name__)
ONOS_API = "http://127.0.0.1:8181/onos/v1/flows"
AUTH = ('onos', 'rocks')

@app.route("/api/dmcm_notify", methods=["POST"])
def dmcm_notify():
    data = request.get_json()
    device = data.get("switch", "of:0000000000000001")
    src, dst = data.get("flow_src"), data.get("flow_dst")
    flow = {
        "flows": [{
            "deviceId": device,
            "isPermanent": False,
            "priority": 50000,
            "timeout": 40,
            "treatment": {"instructions": [{"type": "DROP"}]},
            "selector": {"criteria": [{"type": "ETH_SRC", "mac": src}, {"type": "ETH_DST", "mac": dst}]}
        }]
    }
    requests.post(ONOS_API, auth=AUTH, json=flow)
    return jsonify({"status": "pushed"}), 200

if __name__ == "__main__":
    app.run(port=5008)
