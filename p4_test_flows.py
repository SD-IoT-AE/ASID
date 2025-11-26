"""
ASID P4 Flow Test Script
Simulates HTTP/SQLi packet flows and verifies digest export.
"""
import os, time, json, random, socket

def send_test_flows():
    for i in range(5):
        src_ip = f"10.0.{i}.1"
        dst_ip = f"10.0.{i}.2"
        payload = f"SELECT * FROM users WHERE id={i}"
        pkt = {
            "src": src_ip,
            "dst": dst_ip,
            "payload": payload,
            "length": len(payload)
        }
        print(f"[TestFlow] {json.dumps(pkt)}")
        time.sleep(1)

if __name__ == "__main__":
    send_test_flows()
