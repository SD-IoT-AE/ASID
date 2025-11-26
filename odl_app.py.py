"""
OpenDaylight (ODL) Controller App for ASID
Implements RESTCONF mitigation using ODL northbound API.
"""
from flask import Flask, request, jsonify
import requests, json

app = Flask(__name__)
ODL_URL = "http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/"
AUTH = ('admin', 'admin')

@app.route("/api/mitigation", methods=["POST"])
def mitigation():
    data = request.get_json()
    flow_name = f"asid_block_{data.get('flow_src')}_{data.get('flow_dst')}"
    flow_payload = {
        "flow": [{
            "id": flow_name,
            "priority": 40000,
            "hard-timeout": 60,
            "match": {"ethernet-match": {"ethernet-source": {"address": data.get("flow_src")},
                                         "ethernet-destination": {"address": data.get("flow_dst")}}},
            "instructions": {"instruction": [{"order": 0, "apply-actions": {"action": [{"order": 0, "drop-action": {}}]}}]}
        }]
    }

    r = requests.put(ODL_URL + flow_name, auth=AUTH,
                     headers={"Content-Type": "application/json"}, data=json.dumps(flow_payload))
    print(f"[ODL] Mitigation rule applied: {r.status_code}")
    return jsonify({"status": "ODL mitigation applied", "response": r.status_code})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5007)
