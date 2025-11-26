"""
Collects P4 digest messages emitted by BMv2 switch.
Acts as a simple subscriber for ASID feature exports.
"""
import grpc, json, time
from concurrent import futures
from flask import Flask, request, jsonify

app = Flask(__name__)
digests = []

@app.route("/api/digest", methods=["POST"])
def receive_digest():
    data = request.get_json()
    digests.append(data)
    print(f"[P4 Digest] Received feature vector: {data}")
    return jsonify({"status": "received"})

if __name__ == "__main__":
    print("[Collector] Listening for P4 feature digests...")
    app.run(port=5050)
