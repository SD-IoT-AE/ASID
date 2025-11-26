"""
Coordination Bus
----------------
Handles multi-controller communication and synchronization.
"""

import requests, json, threading

class CoordinationBus:
    def __init__(self):
        # Known controllers and their endpoints
        self.controllers = {
            "RYU": "http://127.0.0.1:5005/api/mitigation",
            "ONOS": "http://127.0.0.1:5006/api/mitigation",
            "ODL": "http://127.0.0.1:5007/api/mitigation"
        }

    def broadcast_mitigation(self, flow_src, flow_dst):
        payload = {"flow_src": flow_src, "flow_dst": flow_dst}
        threads = []
        for name, url in self.controllers.items():
            t = threading.Thread(target=self._send, args=(name, url, payload))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

    def _send(self, name, url, payload):
        try:
            r = requests.post(url, json=payload, timeout=1.0)
            print(f"[Bus] {name} -> {url}: {r.status_code}")
        except Exception as e:
            print(f"[Bus] {name} failed: {e}")
